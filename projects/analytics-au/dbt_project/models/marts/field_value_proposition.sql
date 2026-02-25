{{ config(materialized='table') }}

-- Composite ranking of each field by opportunity gap, employment rate, and salary.
-- Classifies fields into actionable tiers for marketing spend prioritisation.

with outcomes as (
    select * from {{ ref('graduate_outcomes_by_fos') }}
),

opportunity as (
    select * from {{ ref('opportunity_gap') }}
),

sector_medians as (
    select
        round(avg(ft_employment_rate), 1) as sector_ft_employment_rate,
        round(avg(median_salary), 0)::int as sector_median_salary
    from outcomes
),

combined as (
    select
        o.field_of_study,
        og.opportunity_gap,
        og.vacancy_share,
        og.preference_share,
        og.vacancy_growth_12m,
        o.ft_employment_rate,
        o.median_salary,
        o.median_salary_male,
        o.median_salary_female,
        o.salary_gender_gap,
        sm.sector_ft_employment_rate,
        sm.sector_median_salary,
        percent_rank() over (order by og.opportunity_gap nulls first) as opportunity_pctile,
        percent_rank() over (order by o.ft_employment_rate nulls first) as employment_pctile,
        percent_rank() over (order by o.median_salary nulls first) as salary_pctile
    from outcomes o
    left join opportunity og on o.field_of_study = og.field_of_study
    cross join sector_medians sm
),

scored as (
    select
        *,
        round((opportunity_pctile + employment_pctile + salary_pctile) / 3.0, 4) as value_score,
        case
            when opportunity_gap > 0
                and ft_employment_rate >= 80
                and median_salary >= sector_median_salary
                then 'No-brainer'
            when opportunity_gap > 0
                then 'High potential'
            when (opportunity_gap <= 0 or opportunity_gap is null)
                and ft_employment_rate >= 80
                and median_salary >= sector_median_salary
                then 'Proven outcomes'
            else 'Challenging'
        end as value_tier
    from combined
)

select
    field_of_study,
    opportunity_gap,
    row_number() over (order by opportunity_gap desc nulls last) as opportunity_rank,
    ft_employment_rate,
    median_salary,
    vacancy_growth_12m,
    value_score,
    value_tier,
    row_number() over (order by value_score desc) as value_rank,
    sector_ft_employment_rate,
    sector_median_salary,
    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id
from scored
order by value_score desc
