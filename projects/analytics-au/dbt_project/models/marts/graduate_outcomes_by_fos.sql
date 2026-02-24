{{ config(materialized='table') }}

-- Graduate outcomes enriched with opportunity gap context.
-- Multiple QILT study areas map to a single UAC field (e.g. 6 QILT areas → Health),
-- so we aggregate with weighted-style averages at the UAC field level, then join
-- the opportunity gap and gender preference data for a unified marketing view.

with outcomes as (
    select * from {{ ref('stg_qilt_graduate_outcomes') }}
),

-- Aggregate QILT study areas up to UAC field level.
-- Use simple averages since QILT doesn't publish respondent counts per study area
-- in the report tables (only percentages).
outcomes_by_fos as (
    select
        uac_field_of_study as field_of_study,
        count(*) as qilt_areas_count,
        round(avg(ft_employment_rate), 1) as ft_employment_rate,
        round(avg(ft_employment_rate_prior), 1) as ft_employment_rate_prior,
        round(avg(overall_employment_rate), 1) as overall_employment_rate,
        round(avg(median_salary), 0)::int as median_salary,
        round(avg(median_salary_prior), 0)::int as median_salary_prior,
        round(avg(median_salary_male), 0)::int as median_salary_male,
        round(avg(median_salary_female), 0)::int as median_salary_female
    from outcomes
    group by uac_field_of_study
),

opportunity as (
    select * from {{ ref('opportunity_gap') }}
),

gender as (
    select * from {{ ref('stg_uac_fos_by_gender') }}
),

gender_pivoted as (
    select
        field_of_study,
        max(case when gender = 'Female' then preference_share end) as female_preference_share,
        max(case when gender = 'Male' then preference_share end) as male_preference_share
    from gender
    group by field_of_study
)

select
    oc.field_of_study,

    -- Graduate outcomes (QILT GOS)
    oc.ft_employment_rate,
    oc.ft_employment_rate_prior,
    oc.overall_employment_rate,
    oc.median_salary,
    oc.median_salary_prior,
    oc.median_salary_male,
    oc.median_salary_female,
    round((oc.median_salary - oc.median_salary_prior) * 100.0
        / oc.median_salary_prior, 1) as salary_growth_pct,

    -- Opportunity gap context (IVI + UAC)
    og.opportunity_gap,
    og.opportunity_rank,
    og.vacancy_share,
    og.preference_share,
    og.vacancy_growth_12m,

    -- Gender preferences (UAC)
    gp.female_preference_share,
    gp.male_preference_share,
    round(oc.median_salary_male - oc.median_salary_female, 0)::int as salary_gender_gap,

    -- Composite marketing signals
    case
        when og.opportunity_gap > 0 and oc.ft_employment_rate >= 75
            then 'Strong — high demand, strong outcomes'
        when og.opportunity_gap > 0 and oc.ft_employment_rate < 75
            then 'Demand — high demand, moderate outcomes'
        when og.opportunity_gap <= 0 and oc.ft_employment_rate >= 80
            then 'Outcomes — saturated but graduates do well'
        when og.opportunity_gap is null
            then 'Unmapped'
        else 'Challenging — low demand, weaker outcomes'
    end as marketing_signal,

    oc.qilt_areas_count

from outcomes_by_fos oc
left join opportunity og on oc.field_of_study = og.field_of_study
left join gender_pivoted gp on oc.field_of_study = gp.field_of_study
order by og.opportunity_rank nulls last
