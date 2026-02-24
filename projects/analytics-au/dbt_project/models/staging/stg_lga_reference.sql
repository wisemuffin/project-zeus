{{ config(materialized='view') }}

-- LGA reference data: names, state mapping, and land area from ABS ASGS 2024.
-- Provides the canonical LGA-to-state lookup and area for density calculations.

select
    lga_code_2024 as lga_code,
    lga_name_2024 as lga_name,
    state_code_2021 as state_code,
    state_name_2021 as state_name,
    case state_code_2021
        when '1' then 'NSW'
        when '2' then 'VIC'
        when '3' then 'QLD'
        when '4' then 'SA'
        when '5' then 'WA'
        when '6' then 'TAS'
        when '7' then 'NT'
        when '8' then 'ACT'
        when '9' then 'OT'
        else null
    end as state,
    area_albers_sqkm
from {{ source('dagster', 'abs_lga_reference') }}
