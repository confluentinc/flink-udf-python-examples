variable "confluent_cloud_api_key" {
  description = "Confluent Cloud API Key (also referred as Cloud API ID). Can be set via TF_VAR_confluent_cloud_api_key environment variable."
  type        = string
  default     = null
}

variable "confluent_cloud_api_secret" {
  description = "Confluent Cloud API Secret. Can be set via TF_VAR_confluent_cloud_api_secret environment variable."
  type        = string
  sensitive   = true
  default     = null
}

variable "artifact_file" {
  description = "Path to .zip / .jar for Flink Artifact (relative to where terraform is run). Can be set via TF_VAR_artifact_file environment variable."
  type        = string
  # See "Create a User Defined Function for Flink SQL" here for more details
  # https://docs.confluent.io/cloud/current/flink/how-to-guides/create-udf.html#flink-sql-create-udf-upload-jar
  default = "../basic/dist/example_udf-0.1.0.zip"
}

variable "organization_id" {
  description = "The ID of Confluent Cloud organization (for example, foobar). You could find it on XYZ page. Can be set via TF_VAR_organization_id environment variable."
  type        = string
  default     = null
}

variable "environment_id" {
  description = "The ID of the managed environment on Confluent Cloud. Can be set via TF_VAR_environment_id environment variable."
  type        = string
  default     = null
}

# In Confluent Cloud, an environment is mapped to a Flink catalog.
# See https://docs.confluent.io/cloud/current/flink/index.html#metadata-mapping-between-ak-cluster-topics-schemas-and-af
# for more details.
variable "current_catalog" {
  description = "The display name of the managed environment on Confluent Cloud. Can be set via TF_VAR_current_catalog environment variable."
  type        = string
}

# In Confluent Cloud, a Kafka cluster is mapped to a Flink database.
# See https://docs.confluent.io/cloud/current/flink/index.html#metadata-mapping-between-ak-cluster-topics-schemas-and-af
# for more details.
variable "current_database" {
  description = "The display name of the managed Kafka Cluster on Confluent Cloud. Can be set via TF_VAR_current_database environment variable."
  type        = string
}

variable "flink_compute_pool_id" {
  description = "The ID of the managed Compute Pool on Confluent Cloud. Can be set via TF_VAR_flink_compute_pool_id environment variable."
  type        = string
}

variable "flink_rest_endpoint" {
  description = "The REST endpoint base domain for Flink API calls (e.g., 'devel.cpdev.cloud' or 'confluent.cloud'). The provider constructs the full URL as 'https://flink.{region}.{cloud}.{rest-endpoint}'. Do NOT include 'https://' prefix. Can be set via TF_VAR_flink_rest_endpoint environment variable."
  type        = string
  default     = null
}

variable "flink_api_key" {
  description = "Flink API Key (also referred as Flink API ID) that should be owned by a principal with a FlinkAdmin role (provided by Ops team). Can be set via TF_VAR_flink_api_key environment variable."
  type        = string
  default     = null
}

variable "flink_api_secret" {
  description = "Flink API Secret (provided by Ops team). Can be set via TF_VAR_flink_api_secret environment variable."
  type        = string
  sensitive   = true
  default     = null
}

variable "flink_principal_id" {
  description = "Principal ID (service account) that runs submitted Flink statements. Optional but required by provider when using Flink features. Example: 'sa-23kgz4'. Can be set via TF_VAR_flink_principal_id environment variable."
  type        = string
  default     = null
}

variable "confluent_endpoint" {
  description = "Confluent Cloud API endpoint. Defaults to production (https://api.confluent.cloud). Can be set via TF_VAR_confluent_endpoint environment variable. Used for different environments (devel/stag/provider)."
  type        = string
  default     = "https://api.confluent.cloud"
}

variable "cloud" {
  description = "The cloud provider for the Flink artifact (AWS, GCP, or AZURE). Can be set via TF_VAR_cloud environment variable."
  type        = string
  default     = "AWS"
}

variable "region" {
  description = "The cloud region for the Flink artifact (e.g., us-west-2, us-east-1). Can be set via TF_VAR_region environment variable."
  type        = string
  default     = "us-west-2"
}
