{{ config(materialized='view') }}

-- LGA-level youth population (15-19), keeping LGA granularity instead of
-- aggregating to state level like stg_youth_population_by_state.

with source as (
    select
        LGA_2024,
        TIME_PERIOD,
        OBS_VALUE as population
    from {{ source('dagster', 'abs_population_by_lga') }}
),

latest_year as (
    select max(TIME_PERIOD) as max_year from source
)

select
    s.LGA_2024 as lga_code,
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
    s.population as youth_population
from source s
cross join latest_year ly
where s.TIME_PERIOD = ly.max_year
    and case LEFT(CAST(s.LGA_2024 as VARCHAR), 1)
        when '1' then 'NSW'
        when '2' then 'VIC'
        when '3' then 'QLD'
        when '4' then 'SA'
        when '5' then 'WA'
        when '6' then 'TAS'
        when '7' then 'NT'
        when '8' then 'ACT'
        else null
    end is not null
