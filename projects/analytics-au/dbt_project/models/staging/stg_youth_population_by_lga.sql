{{ config(materialized='view') }}

-- LGA-level youth population (15-19), keeping LGA granularity instead of
-- aggregating to state level like stg_youth_population_by_state.

with source as (
    select
        LGA_2024,
        TIME_PERIOD,
        CAST(OBS_VALUE AS INTEGER) as population
    from {{ source('dagster', 'abs_population_by_lga') }}
),

latest_year as (
    select max(TIME_PERIOD) as max_year from source
),

lga_ref as (
    select * from {{ ref('stg_lga_reference') }}
)

select
    s.LGA_2024 as lga_code,
    r.lga_name,
    r.state,
    r.state_name,
    r.area_albers_sqkm,
    s.population as youth_population
from source s
cross join latest_year ly
left join lga_ref r on CAST(s.LGA_2024 as VARCHAR) = r.lga_code
where s.TIME_PERIOD = ly.max_year
    and r.state is not null
