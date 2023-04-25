import pandas as pd
import requests
import io
import zipfile
from google.cloud import storage
import datetime as dt
from pathlib import Path
from prefect import flow, task
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
# from prefect_dbt.cli import DbtCoreOperation, DbtCliProfile


@task(log_prints=True, name="Fetch divvy data", retries=3)
def download_file(url):
    print(f"Downloading data from {url}...")
    response = requests.get(url)
    return io.BytesIO(response.content)



@task(log_prints=True, name="Reading data as dataframe")
def read_csv(data):
    with zipfile.ZipFile(data, "r") as zip_ref:
        file_list = zip_ref.namelist()
        csv_files = [f for f in file_list if f.endswith('.csv')]
        if len(csv_files) == 0:
            raise ValueError("ZIP file does not contain a CSV file. Expected one CSV file.")
        
        df_list = []
        for csv_file in csv_files:
            with zip_ref.open(csv_file) as f:
                df = pd.read_csv(f, encoding='latin-1')
                df_list.append(df)
        df = max(df_list, key=len)
        return df

@task(log_prints=True, name="Writing to GCS bucket")
def write_gcs(df, filename, bucket_name):
    """Upload a pandas DataFrame as a parquet file to GCS"""
    gcs_bucket = GcsBucket.load("divvy-creds-bucket")
    gcs_bucket.upload_from_dataframe(df=df, to_path=filename, serialization_format='parquet_snappy',timeout=1000)

@task(log_prints=True, name="Extracting from GCS bucket")
def extract_from_gcs() -> pd.DataFrame:
    """Download and concatenate trip data from GCS"""
    gcs_path = "divvy-tripdata/"
    gcs_block = GcsBucket.load("divvy-creds-bucket")
    blobs=gcs_block.list_blobs("divvy-tripdata/")
    df_list = []
    for blob in blobs:
        if blob.name.endswith(".parquet.snappy"):
            df = pd.read_parquet(f"gcs://{blob.bucket.name}/{blob.name}")
            df_list.append(df)
    return pd.concat(df_list)


@task(log_prints=True, name="Transformaing Data")
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Data cleaning and transformation"""
    df = df.astype({
        "ride_id": "str",
        "rideable_type": "str",
        "started_at": "datetime64[ns]",
        "ended_at": "datetime64[ns]",
        "start_station_name": "str",
        "start_station_id": "str",
        "end_station_name": "str",
        "end_station_id": "str",
        "start_lat": "float64",
        "start_lng": "float64",
        "end_lat": "float64",
        "end_lng": "float64",
        "member_casual": "str"
    })
    return df

@task(log_prints=True, name="Writing to BQ table")
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("divvy-creds")

    df.to_gbq(
        destination_table="divvy_data_raw.divvy_default_data",
        project_id="tidal-cipher-381616",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )

# I tried to trigger dbt job from prefect but got some error
# thats why I commented this part of the code and ran it using cli
# If you want to try it out for yourself uncomment the below block run this script
#
# @task(log_prints=True, name="Runs dbt to transform the data and derive columns")
# def trigger_dbt_flow() -> object:
#     """Triggers the dbt dependency and build commands"""

#     dbt_cli_profile = DbtCliProfile.load("divvy-dbt-cli-profile")

#     with DbtCoreOperation(
#         commands=["dbt deps", "dbt build --var 'is_test_run: false'"],
#         project_dir="~/Downloads/de-zoomcamp-final-project/dbt/divvy_project/",
#         profiles_dir="~/Downloads/de-zoomcamp-final-project/dbt/divvy_project/",
#         dbt_cli_profile=dbt_cli_profile, 
#         overwrite_profiles=True,
#     ) as dbt_operation:
#         dbt_process = dbt_operation.trigger()
#         dbt_process.wait_for_completion()
#         result = dbt_process.fetch_result()
#     return result



@flow
def web_to_gcs_to_bq():
    bucket_name = "divvy_data_lake_tidal-cipher-381616"
    
    urls = [
        f"https://divvy-tripdata.s3.amazonaws.com/{yearmonth}-divvy-tripdata.zip"
        for year in range(2020, 2023)
        for yearmonth in [f"{year}{month:02d}" for month in range(4, 13)] + [f"{year+1}{month:02d}" for month in range(1, 3)]
    ]
    
    for url in urls:
        data = download_file(url)
        df = read_csv(data)
        filename = f"divvy-tripdata/{url.split('/')[-1].replace('.zip', '.parquet')}"
        write_gcs(df, filename, bucket_name)

    df = extract_from_gcs()
    df = transform(df)
    write_bq(df)
    #trigger_dbt_flow()
    

if __name__ == "__main__":
    web_to_gcs_to_bq()

