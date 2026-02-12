# PII Mask UDF

This example demonstrates a Python UDF that anonymizes Personally
Identifiable Information (PII) in text using regex-based detection.

The UDF detects and masks:
- Email addresses
- Phone numbers
- Social Security Numbers (SSN)
- Credit card numbers
- IP addresses
- Dates of birth
- ZIP codes

## Files

- `src/pii_mask/pii_mask.py` - The UDF implementation that masks PII
- `src/pii_mask/__init__.py` - Package exports
- `pyproject.toml` - Project configuration and dependencies

## Dependencies

This UDF uses [datafog](https://pypi.org/project/datafog/) for regex-based
PII detection. No private dependencies or ML models are required.

## Build and Deploy

### 1. Build the UDF Package

```bash
cd pii_mask
uv build --sdist
cd dist && zip -j pii_mask-0.1.0.zip pii_mask-0.1.0.tar.gz
```

### 2. Upload the Artifact

```bash
confluent flink artifact create pii-mask \
  --artifact-file dist/pii_mask-0.1.0.zip \
  --cloud aws \
  --region us-east-1 \
  --environment <your-environment-id> \
  --runtime-language python \
  --description "UDF to mask PII (emails, phones, SSNs, credit cards, IPs) in text"
```

Note the artifact ID and version from the output (e.g., `cfa-68xgq6/ver-08jxkp`).

### 3. Register the Function

```bash
confluent flink statement create \
  --sql "CREATE FUNCTION mask_pii AS 'pii_mask.pii_mask.mask_pii' LANGUAGE PYTHON USING JAR 'confluent-artifact://<artifact-id>/<version-id>';" \
  --compute-pool <your-compute-pool> \
  --environment <your-environment-id> \
  --database <your-kafka-cluster-id>
```

## Testing with Faker Data

### 1. Create a Faker Table

```bash
confluent flink statement create \
  --sql "CREATE TABLE game_telemetry_raw (
  event_id STRING,
  event_time TIMESTAMP(3),
  player_id STRING,
  player_name STRING,
  player_email STRING,
  player_ip STRING,
  player_phone STRING,
  game_session_id STRING,
  event_type STRING,
  level_id INT,
  score INT,
  health INT
) WITH (
  'connector' = 'faker',
  'rows-per-second' = '5',
  'fields.event_id.expression' = '#{Internet.uuid}',
  'fields.event_time.expression' = '#{date.past ''30'',''SECONDS''}',
  'fields.player_id.expression' = '#{regexify ''player_[a-z0-9]{8}''}',
  'fields.player_name.expression' = '#{Name.fullName}',
  'fields.player_email.expression' = '#{Internet.emailAddress}',
  'fields.player_ip.expression' = '#{Internet.ipV4Address}',
  'fields.player_phone.expression' = '#{PhoneNumber.cellPhone}',
  'fields.game_session_id.expression' = '#{Internet.uuid}',
  'fields.event_type.expression' = '#{Options.option ''MOVE'',''JUMP'',''ATTACK'',''COLLECT'',''CHAT'',''DEATH''}',
  'fields.level_id.expression' = '#{number.numberBetween ''1'',''50''}',
  'fields.score.expression' = '#{number.numberBetween ''0'',''100000''}',
  'fields.health.expression' = '#{number.numberBetween ''0'',''100''}'
);" \
  --compute-pool <your-compute-pool> \
  --environment <your-environment-id> \
  --database <your-kafka-cluster-id> \
  --wait
```

### 2. Test the UDF

Open the Flink SQL shell:

```bash
confluent flink shell --compute-pool <your-compute-pool> --environment <your-environment-id>
```

Set the database and run the query:

```sql
USE <your-kafka-cluster-id>;

SELECT
  event_id,
  event_time,
  player_id,
  mask_pii(player_name) AS player_name_masked,
  mask_pii(player_email) AS player_email_masked,
  mask_pii(player_ip) AS player_ip_masked,
  mask_pii(player_phone) AS player_phone_masked,
  event_type,
  level_id,
  score,
  health
FROM game_telemetry_raw;
```

### Expected Output

| Field | Result |
|-------|--------|
| `player_email_masked` | `****` |
| `player_ip_masked` | `****` |
| `player_phone_masked` | `****` |
| `player_name_masked` | Original (regex doesn't detect names) |

Press `Ctrl+C` to stop the streaming query.

## Limitations

The regex-based PII detection does not detect:
- Person names
- Organization names
- Addresses (street names)
- Other context-dependent PII

For ML-based entity detection (including names), consider using the
`datafog[nlp-advanced]` extra with GLiNER, though this significantly
increases the package size (~400MB for torch + transformers).
