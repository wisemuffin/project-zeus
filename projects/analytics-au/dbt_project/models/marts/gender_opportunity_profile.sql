{{ config(materialized='table') }}

-- Gender salary gap alongside preference shares and opportunity gap.
-- Classifies diversity opportunity for equity-focused marketing messaging.

with outcomes as (
    select * from {{ ref('graduate_outcomes_by_fos') }}
),

classified as (
    select
        field_of_study,
        median_salary,
        median_salary_female,
        median_salary_male,
        salary_gender_gap,
        case
            when median_salary > 0
            then round(salary_gender_gap * 1.0 / median_salary, 4)
            else null
        end as gender_gap_pct,
        female_preference_share,
        male_preference_share,
        round(0.5 - coalesce(female_preference_share, 0), 4) as female_underrepresentation,
        ft_employment_rate,
        opportunity_gap,
        opportunity_rank,
        vacancy_growth_12m,
        case
            when opportunity_gap > 0
                and (0.5 - coalesce(female_preference_share, 0)) > 0.10
                then 'High diversity opportunity'
            when (0.5 - coalesce(female_preference_share, 0)) > 0.10
                then 'Equity focus'
            when abs(0.5 - coalesce(female_preference_share, 0)) <= 0.10
                then 'Gender balanced'
            else 'Male underrepresented'
        end as diversity_opportunity
    from outcomes
)

select
    field_of_study,
    median_salary_female,
    median_salary_male,
    salary_gender_gap,
    gender_gap_pct,
    female_preference_share,
    male_preference_share,
    female_underrepresentation,
    opportunity_gap,
    opportunity_rank,
    ft_employment_rate,
    vacancy_growth_12m,
    diversity_opportunity,
    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id
from classified
order by opportunity_rank nulls last
