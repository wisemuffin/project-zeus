{{ config(materialized='table') }}

-- QILT Student Experience Survey satisfaction aggregated to UAC field level,
-- joined with opportunity gap and graduate outcomes for messaging proof points.

with ses as (
    select * from {{ ref('stg_qilt_student_experience') }}
),

-- Aggregate QILT study areas up to UAC field level (same pattern as graduate_outcomes_by_fos)
ses_by_fos as (
    select
        uac_field_of_study as field_of_study,
        count(*) as qilt_areas_count,
        round(avg(teaching_quality), 1) as teaching_quality,
        round(avg(skills_development), 1) as skills_development,
        round(avg(student_support), 1) as student_support,
        round(avg(learning_resources), 1) as learning_resources,
        round(avg(peer_engagement), 1) as peer_engagement,
        round(avg(overall_quality), 1) as overall_quality
    from ses
    where uac_field_of_study is not null
    group by uac_field_of_study
),

sector_averages as (
    select
        round(avg(overall_quality), 1) as sector_overall_quality
    from ses_by_fos
),

opportunity as (
    select * from {{ ref('opportunity_gap') }}
),

outcomes as (
    select
        field_of_study,
        ft_employment_rate,
        median_salary
    from {{ ref('graduate_outcomes_by_fos') }}
)

select
    s.field_of_study,
    s.teaching_quality,
    s.skills_development,
    s.student_support,
    s.learning_resources,
    s.peer_engagement,
    s.overall_quality,
    round(s.overall_quality - sa.sector_overall_quality, 1) as quality_vs_sector,
    oc.ft_employment_rate,
    oc.median_salary,
    og.opportunity_gap,
    og.opportunity_rank,
    og.vacancy_growth_12m,
    s.qilt_areas_count,
    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id
from ses_by_fos s
cross join sector_averages sa
left join opportunity og on s.field_of_study = og.field_of_study
left join outcomes oc on s.field_of_study = oc.field_of_study
order by og.opportunity_rank nulls last
