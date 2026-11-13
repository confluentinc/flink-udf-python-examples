# Terraform Configuration

This Terraform setup automates deploying the basic example UDF (`int_add`, `str_concat`) to Confluent Cloud Flink.

## What It Does

1. **Uploads the UDF artifact** — Creates a `confluent_flink_artifact` resource that uploads the built Python zip file to Confluent Cloud
2. **Registers the function** — Creates a `confluent_flink_statement` that runs `CREATE FUNCTION` to make the UDF available in Flink SQL

## Prerequisites

- Terraform installed
- A built artifact zip file at `../basic/dist/example_udf-0.1.0.zip` (run `uv build` first in the basic directory if the dist does not exist). Refer to the README in the basic directory for more information.
- Confluent Cloud credentials with appropriate permissions
- An existing Flink compute pool in Confluent Cloud

## Required Variables

Set these via environment variables (`TF_VAR_<name>`) or a `terraform.tfvars` file:

| Variable | Description |
|----------|-------------|
| `confluent_cloud_api_key` | Cloud API Key |
| `confluent_cloud_api_secret` | Cloud API Secret |
| `organization_id` | Confluent Cloud organization ID |
| `environment_id` | Environment ID where the UDF will be deployed |
| `flink_compute_pool_id` | Flink compute pool ID |
| `flink_api_key` | Flink API Key (must have FlinkAdmin role) |
| `flink_api_secret` | Flink API Secret |
| `flink_principal_id` | Service account principal ID (e.g., `sa-23kgz4`) |
| `current_catalog` | Environment display name (maps to Flink catalog) |
| `current_database` | Kafka cluster display name (maps to Flink database) |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `confluent_endpoint` | `https://api.confluent.cloud` | API endpoint (for non-production environments) |
| `flink_rest_endpoint` | `null` | Flink REST endpoint base domain |
| `artifact_file` | `../basic/dist/example_udf-0.1.0.zip` | Path to the built artifact |
| `cloud` | `AWS` | Cloud provider (`AWS`, `GCP`, or `AZURE`) |
| `region` | `us-west-2` | Cloud region (e.g., `us-west-2`, `us-east-1`) |

## Usage

```bash
# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Deploy the UDF
terraform apply

# Remove the UDF
terraform destroy
```

### Example with Environment Variables

```bash
export TF_VAR_confluent_cloud_api_key="your-key"
export TF_VAR_confluent_cloud_api_secret="your-secret"
export TF_VAR_organization_id="org-abc123"
export TF_VAR_environment_id="env-xyz789"
export TF_VAR_flink_compute_pool_id="lfcp-123456"
export TF_VAR_flink_api_key="flink-key"
export TF_VAR_flink_api_secret="flink-secret"
export TF_VAR_flink_principal_id="sa-12345"
export TF_VAR_current_catalog="my-environment"
export TF_VAR_current_database="my-cluster"

terraform apply
```

## Resources Created

- **`confluent_flink_artifact.main`** — The uploaded Python UDF artifact
- **`confluent_flink_statement.create-int-add`** — Registers the `int_add` function
- **`confluent_flink_statement.create-str-concat`** — Registers the `str_concat` function

After successful deployment, the functions are available in Flink SQL:

```sql
SELECT int_add(1, 2);        -- returns 3
SELECT str_concat('a', 'b'); -- returns 'ab'
```
