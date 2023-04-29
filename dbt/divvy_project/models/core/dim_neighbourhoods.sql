{{ config(materialized='table') }}

select *
from {{ ref('divvy_stations_lookup') }}
