{{ config(materialized='table') }}

with vacancies as (
    select * from {{ ref('stg_job_vacancies_by_state_fos') }}
),

population as (
    select * from {{ ref('stg_youth_population_by_state') }}
),

state_totals as (
    select state, sum(vacancies) as state_total_vacancies
    from vacancies
    group by state
),

national as (
    select * from {{ ref('opportunity_gap') }}
),

enriched as (
    select
        v.state,
        v.field_of_study,
        v.vacancies,
        round(v.vacancies * 1.0 / st.state_total_vacancies, 4) as fos_share_in_state,
        n.vacancy_share as national_vacancy_share,
        round(
            (v.vacancies * 1.0 / st.state_total_vacancies) - n.vacancy_share, 4
        ) as state_vs_national_skew,
        v.vacancy_growth_12m,
        p.youth_population_15_19,
        round(v.vacancies * 1000.0 / p.youth_population_15_19, 1) as vacancies_per_1k_youth,
        n.opportunity_gap as national_opportunity_gap,
        n.opportunity_rank as national_opportunity_rank
    from vacancies v
    inner join state_totals st on v.state = st.state
    inner join population p on v.state = p.state
    inner join national n on v.field_of_study = n.field_of_study
)

select
    *,
    row_number() over (
        partition by state order by state_vs_national_skew desc
    ) as state_specialisation_rank,
    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id
from enriched
order by state, state_vs_national_skew desc
