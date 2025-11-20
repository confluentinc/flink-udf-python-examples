-- Complete Flink SQL setup for PII Masking UDF
-- This file contains all necessary statements to:
-- 1. Register the UDF
-- 2. Create source table (Faker table with PII data)
-- 3. Create destination table (for masked PII data)
-- 4. Insert data using the UDF

-- ============================================================================
-- STEP 1: Register the UDF
-- ============================================================================
-- Run this first to register your UDF function
-- Replace <artifact-id> and <version> with actual values from upload
CREATE FUNCTION mask_pii AS 'pii_mask.pii_mask.anonymize'
LANGUAGE PYTHON
USING JAR 'confluent-artifact://<artifact-id>/<version>';

-- ============================================================================
-- STEP 2: Create source table (Faker table)
-- ============================================================================
-- This table generates fake user data with various PII fields for testing
CREATE TABLE users_with_pii (
    id INT,
    email STRING,
    credit_card STRING,
    registration_time TIMESTAMP(3)
) WITH (
    'connector' = 'faker',
    'fields.id.expression' = '#{number.numberBetween ''1'',''100000''}',
    'fields.email.expression' = '#{Internet.emailAddress}',
    'fields.credit_card.expression' = '#{Finance.creditCard}',
    'fields.registration_time.expression' = '#{date.past ''10'',''DAYS''}'
);

-- ============================================================================
-- STEP 3: Create destination table
-- ============================================================================
-- This table stores the transformed data with masked PII
-- Adjust the environment, cluster, and topic names as needed
CREATE TABLE .`users-pii-masked` (
    id INT,
    email STRING,
    masked_email STRING,
    credit_card STRING,
    masked_credit_card STRING,
    registration_time TIMESTAMP(3)
);

-- ============================================================================
-- STEP 4: Test the UDF
-- ============================================================================
-- Simple SELECT to test the UDF masking on various PII fields
SELECT 
    id,
    name,
    anonymize(name) AS masked_name
    email,
    anonymize(email) AS masked_email,
    credit_card,
    anonymize(credit_card) AS masked_credit_card,
    registration_time,
FROM users_with_pii
LIMIT 10;

-- ============================================================================
-- STEP 5: Insert into output topic
-- ============================================================================
-- Transform data using the UDF to mask all PII fields and insert into destination table
INSERT INTO `users-pii-masked`
SELECT
    id,
    email,
    anonymize(email) AS masked_email,
    credit_card,
    anonymize(credit_card) AS masked_credit_card,
    registration_time,
FROM users_with_pii;

