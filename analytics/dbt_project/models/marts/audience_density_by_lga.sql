{{ config(materialized='table') }}

-- LGA-level youth population (15-19) with state context for hyper-local geo-targeting.
-- Identifies specific LGAs with highest youth concentration for local ad targeting.

with lga_population as (
    select * from {{ ref('stg_youth_population_by_lga') }}
),

with_state_totals as (
    select
        lga_code,
        lga_name,
        state,
        state_name,
        area_albers_sqkm,
        youth_population,
        sum(youth_population) over (partition by state) as state_total,
        row_number() over (
            partition by state
            order by youth_population desc
        ) as density_rank_in_state
    from lga_population
)

select
    lga_code,
    lga_name,
    state,
    state_name,
    area_albers_sqkm,
    youth_population,
    round(youth_population * 1.0 / area_albers_sqkm, 2) as youth_density_per_sqkm,
    state_total,
    round(youth_population * 1.0 / state_total, 4) as lga_share_of_state,
    density_rank_in_state,
    round(
        sum(youth_population) over (
            partition by state
            order by youth_population desc
            rows between unbounded preceding and current row
        ) * 1.0 / state_total, 4
    ) as cumulative_share
from with_state_totals
order by state, density_rank_in_state
