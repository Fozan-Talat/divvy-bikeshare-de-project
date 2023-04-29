locals {
  data_lake_bucket = "divvy_data_lake"
}

variable "project" {
  description = "tidal-cipher-381616"
}

variable "region" {
  description = "Region for GCP resources.Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-west6"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "divvy_data_raw"
}

variable "DBT_DATASET" {
  description = "BigQuery Dataset that transformed data (from dbt) will be written to and connected to the presentation layer"
  type = string
  default = "divvy_data_dbt"
}
