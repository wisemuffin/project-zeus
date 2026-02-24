{{ config(materialized='view') }}

with source as (
    select
        LGA_2024,
        TIME_PERIOD,
        OBS_VALUE as population
    from {{ source('dagster', 'abs_population_by_lga') }}
),

latest_year as (
    select max(TIME_PERIOD) as max_year from source
),

lga_ref as (
    select * from {{ ref('stg_lga_reference') }}
)

select
    r.state,
    sum(s.population) as youth_population_15_19
from source s
cross join latest_year ly
left join lga_ref r on CAST(s.LGA_2024 as VARCHAR) = r.lga_code
where s.TIME_PERIOD = ly.max_year
    and r.state is not null
group by r.state
