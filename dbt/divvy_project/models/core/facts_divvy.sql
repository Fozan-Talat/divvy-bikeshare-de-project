{{ 
    config(
        materialized='table',
        unique_key="ride_id",
        partition_by={
            "field": "started_at",
            "data_type": "timestamp",
            "granularity": "day",
        },
        cluster_by="start_station_name",
    ) 
}}

WITH divvy_data AS (
    SELECT 
        ride_id, 
        rideable_type,
        membership_status,
        start_station_name,
        end_station_name,
        started_at,
        ended_at,
        TIMESTAMP_DIFF(ended_at, started_at, MINUTE) AS duration_minutes
    FROM {{ ref('stg_divvy_data') }}
),
neighbourhoods AS (
    SELECT 
        station_id,
        station_name,
        CONCAT(CAST(lat AS STRING), ',', CAST(lng AS STRING)) AS location,
        primary_neighbourhood AS neighbourhood
    FROM {{ ref('dim_neighbourhoods') }}

)
SELECT 
    ride_id, 
    rideable_type,
    membership_status,
    start_station_info.station_id AS start_station_id,
    start_station_name,
    end_station_name,
    end_station_info.station_id AS end_station_id,
    started_at,
    ended_at,
    duration_minutes,
    start_station_info.neighbourhood AS start_neighbourhood,
    start_station_info.location AS start_location,
    end_station_info.neighbourhood AS end_neighbourhood,
    end_station_info.location AS end_location
FROM divvy_data 
INNER JOIN  neighbourhoods AS start_station_info
ON divvy_data.start_station_name = start_station_info.station_name
INNER JOIN neighbourhoods AS end_station_info
ON divvy_data.end_station_name = end_station_info.station_name
WHERE duration_minutes BETWEEN  1 AND 24 * 60 - 1