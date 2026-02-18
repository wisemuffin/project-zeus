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

mapped as (
    select
        case LEFT(CAST(s.LGA_2024 as VARCHAR), 1)
            when '1' then 'NSW'
            when '2' then 'VIC'
            when '3' then 'QLD'
            when '4' then 'SA'
            when '5' then 'WA'
            when '6' then 'TAS'
            when '7' then 'NT'
            when '8' then 'ACT'
            else null
        end as state,
        s.population
    from source s
    cross join latest_year ly
    where s.TIME_PERIOD = ly.max_year
)

select
    state,
    sum(population) as youth_population_15_19
from mapped
where state is not null
group by state
