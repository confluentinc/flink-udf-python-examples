# PII Mask UDF

This example demonstrates a Python UDF that masks Personally Identifiable Information (PII) using Microsoft Presidio, the most widely used PII detection and masking library. The UDF can detect and mask various types of PII including names, email addresses, phone numbers, credit card numbers, Social Security Numbers, IP addresses, and more.

## Files

- `src/pii_mask/pii_mask.py` - The UDF implementation that masks PII using Presidio
- `pyproject.toml` - Project configuration and dependencies (includes Presidio libraries)
- `flink_sql_complete.sql` - Complete SQL statements to register the UDF and run an end-to-end pipeline with a Faker table

## Features

The UDF uses Microsoft Presidio to automatically detect and mask:
- **Names** (PERSON)
- **Email addresses** (EMAIL_ADDRESS)
- **Phone numbers** (PHONE_NUMBER)
- **Credit card numbers** (CREDIT_CARD)
- **Social Security Numbers** (US_SSN)
- **IP addresses** (IP_ADDRESS)
- **Dates of birth** (DATE_TIME)
- **And many more PII types**

## Building the Package

Before building, download the spaCy model and unzip it:

```bash
wget https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0.tar.gz
tar -xvf en_core_web_sm-3.8.0.tar.gz
```

Then build the package as usual. The model will be included in the Python environment when the package is installed.

## Usage

1. **Build and Upload**: Follow the instructions in the [project-level README](../../README.md) to build the artifact and upload it to Confluent Cloud.

2. **Run the Pipeline**: Execute the SQL statements in `flink_sql_complete.sql` in order:
   - Step 1: Register the UDF (replace `<artifact-id>` and `<version>` with your actual values)
   - Step 2: Create a source table using the Faker connector that generates fake PII data
   - Step 3: Create a destination table for storing masked data
   - Step 4: Test the UDF with a SELECT query to see masked results
   - Step 5: Insert transformed data with masked PII into the destination table

The pipeline will:
- Generate fake user data with various PII fields (names, emails, phone numbers, credit cards, addresses) using Flink's Faker connector
- Apply the `mask_pii` UDF to each PII field to detect and mask sensitive information
- Write the results (both original and masked) to a Confluent Flink Table (Kafka Topic)

## Example Output

The UDF will transform PII like:
- `"John Doe"` → `"**** ***"`
- `"john.doe@example.com"` → `"************@example.com"`
- `"555-123-4567"` → `"***-***-****"`
- `"4532-1234-5678-9010"` → `"****************"`

## Dependencies

This example uses:
- **presidio-analyzer**: For detecting PII entities in text
- **presidio-anonymizer**: For masking/anonymizing detected PII

