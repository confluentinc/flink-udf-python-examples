-- Complete Flink SQL setup for Email Mask UDF
-- This file contains all necessary statements to:
-- 1. Register the UDF
-- 2. Create source table (Faker table with user data)
-- 3. Create destination table (for masked email data)
-- 4. Insert data using the UDF

-- ============================================================================
-- STEP 1: Register the UDF
-- ============================================================================
-- Run this first to register your UDF function
-- Replace <artifact-id> and <version> with actual values from upload
CREATE FUNCTION mask_email AS 'email_mask.email_mask.mask_email'
LANGUAGE PYTHON
USING JAR 'confluent-artifact://<artifact-id>/<version>';

-- ============================================================================
-- STEP 2: Create source table (Faker table)
-- ============================================================================
-- This table generates fake user data for testing
CREATE TABLE users (
    id INT,
    name STRING,
    email STRING,
    registration_time TIMESTAMP(3)
) WITH (
    'connector' = 'faker',
    'fields.id.expression' = '#{number.numberBetween ''1'',''100000''}',
    'fields.name.expression' = '#{Name.fullName}',
    'fields.email.expression' = '#{Internet.emailAddress}',
    'fields.registration_time.expression' = '#{date.past ''10'',''DAYS''}'
);

-- ============================================================================
-- STEP 3: Create destination table
-- ============================================================================
-- This table stores the transformed data with masked emails
-- Adjust the environment, cluster, and topic names as needed
CREATE TABLE `my-environment`.`my-cluster`.`users-masked` (
    id INT,
    name STRING,
    email STRING,
    masked_email STRING,
    registration_time TIMESTAMP(3)
);

-- ============================================================================
-- STEP 4: Test the UDF
-- ============================================================================
-- Simple SELECT to test the UDF masking
SELECT 
    id,
    name,
    email,
    mask_email(email) AS masked_email,
    registration_time
FROM users
LIMIT 10;

-- ============================================================================
-- STEP 5: Insert into output topic
-- ============================================================================
-- Transform data using the UDF and insert into destination table
INSERT INTO `my-environment`.`my-cluster`.`users-masked`
SELECT
    id,
    name,
    email,
    mask_email(email) AS masked_email,
    registration_time
FROM users;


