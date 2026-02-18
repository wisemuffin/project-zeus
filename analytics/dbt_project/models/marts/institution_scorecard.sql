{{ config(materialized='table') }}

-- Per-university scorecard combining SES satisfaction with GOS employment outcomes.
-- Computes sector averages and ranks each institution on overall quality and employment.

with scores as (
    select * from {{ source('dagster', 'qilt_institution_scores') }}
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

    -- Difference from sector average
    round(s.overall_quality - sa.avg_overall_quality, 1) as quality_vs_sector,
    round(s.ft_employment_rate - sa.avg_ft_employment_rate, 1) as employment_vs_sector,
    round(s.median_salary - sa.avg_median_salary, 0)::int as salary_vs_sector,

    -- Sector averages for reference
    sa.avg_overall_quality,
    sa.avg_ft_employment_rate,
    sa.avg_median_salary,

    -- Rankings
    row_number() over (order by s.overall_quality desc nulls last) as quality_rank,
    row_number() over (order by s.ft_employment_rate desc nulls last) as employment_rank,
    row_number() over (order by s.median_salary desc nulls last) as salary_rank

from scores s
cross join sector_avg sa
order by s.overall_quality desc nulls last
