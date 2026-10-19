terraform {
  required_providers {
    confluent = {
      source  = "confluentinc/confluent"
      version = "2.54.0"
    }
  }
}

provider "confluent" {
  cloud_api_key         = var.confluent_cloud_api_key
  cloud_api_secret      = var.confluent_cloud_api_secret
  endpoint              = var.confluent_endpoint    # optionally use TF_VAR_confluent_endpoint env var
  organization_id       = var.organization_id       # optionally use CONFLUENT_ORGANIZATION_ID env var
  environment_id        = var.environment_id        # optionally use CONFLUENT_ENVIRONMENT_ID env var
  flink_compute_pool_id = var.flink_compute_pool_id # optionally use FLINK_COMPUTE_POOL_ID env var
  flink_rest_endpoint   = var.flink_rest_endpoint   # optionally use FLINK_REST_ENDPOINT env var
  flink_api_key         = var.flink_api_key         # optionally use FLINK_API_KEY env var
  flink_api_secret      = var.flink_api_secret      # optionally use FLINK_API_SECRET env var
  flink_principal_id    = var.flink_principal_id    # optionally use FLINK_PRINCIPAL_ID env var
}

resource "confluent_flink_artifact" "main" {
  environment {
    id = var.environment_id
  }
  region             = var.region
  cloud              = var.cloud
  display_name       = "example-udf"
  content_format     = "ZIP"
  documentation_link = "https://github.com/confluentinc/flink-udf-python-examples"
  runtime_language   = "Python"
  artifact_file      = var.artifact_file
}

locals {
  plugin_id  = confluent_flink_artifact.main.id
  version_id = confluent_flink_artifact.main.versions[0].version
}

resource "confluent_flink_statement" "create-int-add" {
  statement = "CREATE FUNCTION int_add AS 'example_udf.scalar.int_add' USING JAR 'confluent-artifact://${local.plugin_id}/${local.version_id}';"
  properties = {
    "sql.current-catalog"  = var.current_catalog
    "sql.current-database" = var.current_database
  }
}

resource "confluent_flink_statement" "create-str-concat" {
  statement = "CREATE FUNCTION str_concat AS 'example_udf.scalar.str_concat' USING JAR 'confluent-artifact://${local.plugin_id}/${local.version_id}';"
  properties = {
    "sql.current-catalog"  = var.current_catalog
    "sql.current-database" = var.current_database
  }
}