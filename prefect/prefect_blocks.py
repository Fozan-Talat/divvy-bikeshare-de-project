from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect_dbt.cli import BigQueryTargetConfigs, DbtCliProfile, DbtCoreOperation

# This is an alternative to creating GCP blocks in the UI
# (1) insert your own GCS bucket name
# (2) insert your own service_account_file path or service_account_info dictionary from the json file
# IMPORTANT - do not store credentials in a publicly available repository!

your_GCS_bucket_name = "divvy_data_lake_tidal-cipher-381616"  # (1) insert your GCS bucket name
gcs_credentials_block_name = "divvy-creds"

credentials_block = GcpCredentials(
    service_account_info={
}  # (2)enter your credentials info here
)

credentials_block.save(f"{gcs_credentials_block_name}", overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("divvy-creds"),
    bucket="divvy_data_lake_tidal-cipher-381616",
)

bucket_block.save(f"{gcs_credentials_block_name}-bucket", overwrite=True)


credentials = GcpCredentials.load(gcs_credentials_block_name)
target_configs = BigQueryTargetConfigs(
    schema="divvy_data_dbt",
    credentials=credentials,
)
target_configs.save("divvy-dbt-target-config", overwrite=True)

dbt_cli_profile = DbtCliProfile(
    name="divvy-dbt-cli-profile",
    target="dev",
    target_configs=target_configs,
)
dbt_cli_profile.save("divvy-dbt-cli-profile", overwrite=True)