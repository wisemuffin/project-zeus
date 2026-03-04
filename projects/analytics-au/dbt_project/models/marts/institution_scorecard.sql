{{ config(materialized='table') }}

-- Per-university scorecard combining SES satisfaction with GOS employment outcomes.
-- Computes sector averages and ranks each institution on overall quality and employment.

with scores as (
    select * from {{ source('dagster', 'qilt_institution_scores') }}
),

ess as (
    select * from {{ source('dagster', 'qilt_employer_satisfaction_by_institution') }}
),

sector_avg as (
    select
        round(avg(overall_quality), 1) as avg_overall_quality,
        round(avg(teaching_quality), 1) as avg_teaching_quality,
        round(avg(skills_development), 1) as avg_skills_development,
        round(avg(student_support), 1) as avg_student_support,
        round(avg(learning_resources), 1) as avg_learning_resources,
        round(avg(ft_employment_rate), 1) as avg_ft_employment_rate,
        round(avg(median_salary), 0)::int as avg_median_salary
    from scores
    where overall_quality is not null
),

ess_sector_avg as (
    select
        round(avg(overall_employer_satisfaction), 1) as avg_employer_satisfaction
    from ess
    where overall_employer_satisfaction is not null
)

select
    s.institution,

    -- SES satisfaction indicators
    s.overall_quality,
    s.teaching_quality,
    s.skills_development,
    s.student_support,
    s.learning_resources,
    s.peer_engagement,

    -- GOS employment outcomes
    s.ft_employment_rate,
    s.median_salary,

    -- ESS employer satisfaction
    e.overall_employer_satisfaction,
    round(e.overall_employer_satisfaction - ea.avg_employer_satisfaction, 1) as employer_sat_vs_sector,
    row_number() over (order by e.overall_employer_satisfaction desc nulls last) as employer_sat_rank,

    -- Difference from sector average
    round(s.overall_quality - sa.avg_overall_quality, 1) as quality_vs_sector,
    round(s.ft_employment_rate - sa.avg_ft_employment_rate, 1) as employment_vs_sector,
    round(s.median_salary - sa.avg_median_salary, 0)::int as salary_vs_sector,

    -- Sector averages for reference
    sa.avg_overall_quality,
    sa.avg_ft_employment_rate,
    sa.avg_median_salary,
    ea.avg_employer_satisfaction,

    -- Rankings
    row_number() over (order by s.overall_quality desc nulls last) as quality_rank,
    row_number() over (order by s.ft_employment_rate desc nulls last) as employment_rank,
    row_number() over (order by s.median_salary desc nulls last) as salary_rank,

    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id

from scores s
cross join sector_avg sa
cross join ess_sector_avg ea
left join ess e on s.institution = e.institution
order by s.overall_quality desc nulls last
