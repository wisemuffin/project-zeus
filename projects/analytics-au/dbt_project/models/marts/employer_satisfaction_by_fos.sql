{{ config(materialized='table') }}

-- Employer satisfaction by UAC field of study, enriched with opportunity gap
-- and graduate outcomes context. Provides employer-side proof points for
-- marketing messaging alongside graduate employment data.

with ess as (
    select * from {{ ref('stg_qilt_employer_satisfaction') }}
),

opportunity as (
    select * from {{ ref('opportunity_gap') }}
),

outcomes as (
    select * from {{ ref('graduate_outcomes_by_fos') }}
),

-- Sector averages for benchmarking
sector_avg as (
    select
        round(avg(overall_employer_satisfaction), 1) as avg_employer_satisfaction
    from ess
    where overall_employer_satisfaction is not null
)

select
    e.uac_field_of_study as field_of_study,

    -- ESS employer satisfaction scores
    e.foundation_skills,
    e.adaptive_skills,
    e.collaborative_skills,
    e.technical_skills,
    e.employability_skills,
    e.overall_employer_satisfaction,

    -- Difference from sector average
    round(e.overall_employer_satisfaction - sa.avg_employer_satisfaction, 1) as employer_sat_vs_sector,

    -- Graduate outcomes context
    o.ft_employment_rate,
    o.median_salary,

    -- Opportunity gap context
    og.opportunity_gap,
    og.opportunity_rank,

    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id

from ess e
cross join sector_avg sa
left join opportunity og on e.uac_field_of_study = og.field_of_study
left join outcomes o on e.uac_field_of_study = o.field_of_study
order by og.opportunity_rank nulls last
