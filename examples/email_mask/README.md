# Email Mask UDF

This example demonstrates a Python UDF that masks email addresses by hashing the local part (before the `@` symbol) using SHA256, while preserving the domain.

## Files

- `src/email_mask/email_mask.py` - The UDF implementation that masks email addresses
- `pyproject.toml` - Project configuration and dependencies
- `flink_sql_complete.sql` - Complete SQL statements to register the UDF and run an end-to-end pipeline

## Usage

1. **Build and Upload**: Follow the instructions in the [project-level README](../../README.md) to build the artifact and upload it to Confluent Cloud.

2. **Run the Pipeline**: Execute the SQL statements in `flink_sql_complete.sql` in order:
   - Step 1: Register the UDF (replace `<artifact-id>` and `<version>` with your actual values)
   - Step 2: Create a source table using the Faker connector
   - Step 3: Create a destination table
   - Step 4: Test the UDF with a SELECT query
   - Step 5: Insert transformed data into the destination table

The pipeline will generate fake user data, mask email addresses using the UDF, and write the results to a Confluent Flink Table (Kafka Topic).

