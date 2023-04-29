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

with divvy_data as (
    select *
    from {{ source('staging','divvy_default_data')}}
    where ride_id is not null
)

SELECT 
    -- ride info
    {{ dbt_utils.surrogate_key(['ride_id', 'started_at']) }} as r_id,
    CAST(ride_id AS STRING) AS ride_id,
    CAST(rideable_type AS STRING) AS rideable_type,
    CAST(member_casual AS STRING) AS membership_status,

    -- Timestamp
    CAST(started_at AS TIMESTAMP) AS started_at, 
    CAST(ended_at AS TIMESTAMP) AS ended_at,

    -- station info
    CAST(start_station_name AS STRING) AS start_station_name,
    CAST(start_station_id AS STRING) AS start_station_id,
    CAST(end_station_name AS STRING) AS end_station_name,
    CAST(end_station_id AS STRING) AS end_station_id,

    -- Station info: geo-spatial convert to geospatial in google-studio
    CAST(start_lat AS NUMERIC) AS start_lat, 
    CAST(start_lng AS NUMERIC) AS start_lng, 
    CAST(end_lat AS NUMERIC) AS end_lat, 
    CAST(end_lng AS NUMERIC) AS end_lng 

FROM divvy_data

-- dbt build --select stg_divvy_data.sql --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
