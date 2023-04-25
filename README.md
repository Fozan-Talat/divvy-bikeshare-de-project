![](images/Divvy-bikes.jpg)
 
# Divvy Bikeshare Data Engineering Project 🚴‍♀️
This is an end to end data engineering project, This project uses [Chicago's Divvy bikeshare dataset](https://divvy-tripdata.s3.amazonaws.com/index.html), Divvy is the bicycle sharing system in the Chicago metropolitan area, currently serving the cities of Chicago and Evanston. The system is owned by the Chicago Department of Transportation and has been operated by Lyft since 2019.
## Problem Description
The purpose of this project is to make an end to end data pipeline which extracts the divvy data from the web https://divvy-tripdata.s3.amazonaws.com/index.html and Load this data in Google Cloud storage and Big Query , apply Kimbal Dimensional Modeling(Facts and Dimensions tables) to the data using dbt and build a Looker dashboard to 
vizualize
- Daily riders activity
- Trips per start stations
- Average trip duration
- Bike type distribution and Membership status distribution
- Rides per month and year
## Technology Stack 
The following technologies are used to build this project
- Google Cloud Storage (GCS) - as Data Lake <br>
- Google BigQuery - for Data Warehouse <br>
- Terraform - as Infrastructure-as-Code (IaC) tool <br>
- Prefect - for orchestration <br>
- dbt - for transformation and data modeling <br>
- Google Looker studio - for visualizations <br>
## Data Pipeline Architecture
![data-pipline](images/divvy.png)
## Data Dictionary
| Column | Description | 
|--------|-------------|
| r_id | Unique surrogate built using ride_id and started_at |
| ride_id | Unique ID Assigned to Each Divvy Trip |
| rideable_type | Type of bikes user can take out (Docked, Classic, Electric) |
| started_at  | Start of Trip Date and Time |
| ended_at | End of Trip Date and Time |
| start_station_name | Name of start station |
| start_station_id | Unique Identification Number of Station the Trip Started at |
| end_station_name | Name Assigned to Station the Trip Ended at |
| end_station_id | Unique Identification Number of Station the Trip Ended at|
| start_lat | Latitude of the Start Station|
|start_lng |Longitude of the Start Station|
|end_lat |Latitude of the End Station|
|end_lng |Longitude of the End Station|
|member_casual | Field with Two Values Indicating Whether the Rider has a Divvy Membership or Paid with Credit Card(Casual)|
## Dashboard
![](images/divvy-dash.gif)
