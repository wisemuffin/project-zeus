{{ config(materialized='table') }}

with yearly as (
    select * from {{ ref('stg_uac_demand_by_year') }}
),

latest as (
    select max(intake_year) as max_year from yearly
),

earliest as (
    select min(intake_year) as min_year from yearly
),

summary as (
    select
        y.applicant_type,

        -- latest year
        max(case when y.intake_year = l.max_year then y.intake_year_range end) as latest_intake,
        max(case when y.intake_year = l.max_year then y.applicant_count end) as latest_count,
        max(case when y.intake_year = l.max_year then y.yoy_growth end) as latest_yoy_growth,

        -- peak
        max(y.applicant_count) as peak_count,
        max(case when y.applicant_count = (
            select max(y2.applicant_count) from yearly y2 where y2.applicant_type = y.applicant_type
        ) then y.intake_year_range end) as peak_intake,

        -- earliest and latest for CAGR
        max(case when y.intake_year = e.min_year then y.applicant_count end) as earliest_count,
        max(case when y.intake_year = l.max_year then y.applicant_count end) as latest_count_for_cagr,
        l.max_year - e.min_year as year_span

    from yearly y
    cross join latest l
    cross join earliest e
    group by y.applicant_type, l.max_year, e.min_year
),

with_cagr as (
    select
        *,
        case
            when earliest_count > 0 and year_span > 0
            then round(
                (POWER(latest_count_for_cagr * 1.0 / earliest_count, 1.0 / year_span) - 1), 4
            )
            else null
        end as cagr,
        case
            when latest_yoy_growth > 0 then 'Growing'
            when latest_yoy_growth < 0 then 'Declining'
            else 'Flat'
        end as trend_direction,
        round(latest_count * 1.0 / peak_count, 4) as recovery_ratio
    from summary
)

select
    applicant_type,
    latest_intake,
    latest_count,
    latest_yoy_growth,
    peak_count,
    peak_intake,
    recovery_ratio,
    cagr,
    trend_direction,
    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id
from with_cagr
order by latest_count desc
