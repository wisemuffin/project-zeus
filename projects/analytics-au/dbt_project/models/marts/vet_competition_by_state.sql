{{ config(materialized='table') }}

-- VET competition context by state.
-- Grain: state (8 rows).
-- Combines NCVER VET student data with youth population and HE demand context.
-- Note: staging data has male/female rows only — totals are summed here.

with vet as (
    select * from {{ ref('stg_ncver_vet_students') }}
),

-- Compute totals by summing male + female per state per year
vet_totals as (
    select
        state,
        year,
        sum(students) as students
    from vet
    group by state, year
),

max_year as (
    select max(year) as yr from vet_totals
),

-- Latest year total by state
vet_latest as (
    select
        vt.state,
        vt.year as latest_year,
        vt.students
    from vet_totals vt
    cross join max_year my
    where vt.year = my.yr
),

-- Prior year for YoY growth
vet_prior as (
    select
        vt.state,
        vt.students as prior_students
    from vet_totals vt
    cross join max_year my
    where vt.year = my.yr - 1
),

-- 5 years ago for CAGR
vet_5yr_ago as (
    select
        vt.state,
        vt.students as base_students
    from vet_totals vt
    cross join max_year my
    where vt.year = my.yr - 5
),

-- Peak year by state
vet_peak as (
    select
        state,
        max(students) as peak_students
    from vet_totals
    group by state
),

-- Female count in latest year
vet_female as (
    select
        v.state,
        v.students as female_students
    from vet v
    cross join max_year my
    where v.gender = 'female'
      and v.year = my.yr
),

population as (
    select * from {{ ref('stg_youth_population_by_state') }}
),

he_demand as (
    select * from {{ ref('state_demand_index') }}
),

joined as (
    select
        vl.state,
        vl.latest_year,
        vl.students as vet_students,
        round(vl.students * 1000.0 / p.youth_population_15_19, 1) as vet_students_per_1k_youth,

        -- YoY growth
        round(
            (vl.students - vp.prior_students) * 1.0 / nullif(vp.prior_students, 0),
            4
        ) as vet_yoy_growth,

        -- 5-year CAGR
        case
            when v5.base_students > 0 and vl.students > 0
            then round(
                power(vl.students * 1.0 / v5.base_students, 1.0 / 5) - 1,
                4
            )
            else null
        end as vet_cagr_5yr,

        -- Recovery ratio
        round(vl.students * 1.0 / nullif(vpk.peak_students, 0), 4) as vet_recovery_ratio,

        -- Female share
        round(vf.female_students * 1.0 / nullif(vl.students, 0), 4) as vet_female_share,

        -- Trend direction
        case
            when (vl.students - vp.prior_students) * 1.0 / nullif(vp.prior_students, 0) > 0.01 then 'Growing'
            when (vl.students - vp.prior_students) * 1.0 / nullif(vp.prior_students, 0) < -0.01 then 'Declining'
            else 'Stable'
        end as vet_trend_direction,

        -- HE context from state_demand_index
        hd.graduate_vacancies_per_1k_youth,
        hd.graduate_vacancy_growth_12m,
        hd.demand_rank as he_demand_rank,

        p.youth_population_15_19

    from vet_latest vl
    inner join population p on vl.state = p.state
    left join vet_prior vp on vl.state = vp.state
    left join vet_5yr_ago v5 on vl.state = v5.state
    left join vet_peak vpk on vl.state = vpk.state
    left join vet_female vf on vl.state = vf.state
    left join he_demand hd on vl.state = hd.state
)

select
    state,
    latest_year,
    vet_students,
    youth_population_15_19,
    vet_students_per_1k_youth,
    graduate_vacancies_per_1k_youth,
    vet_yoy_growth,
    vet_cagr_5yr,
    vet_recovery_ratio,
    vet_female_share,
    vet_trend_direction,
    graduate_vacancy_growth_12m,
    he_demand_rank,
    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id
from joined
order by vet_students_per_1k_youth desc
