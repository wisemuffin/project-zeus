{{ config(materialized='table') }}

-- ANZSCO2 occupation groups ranked by 12-month vacancy growth, mapped to UAC fields.
-- Identifies fast-growing occupations where messaging can highlight demand.

with vacancies as (
    select * from {{ ref('stg_job_vacancies_by_occupation') }}
),

mapping as (
    select anzsco2_title, uac_field_of_study
    from {{ source('dagster', 'occupation_fos_mapping') }}
),

opportunity as (
    select * from {{ ref('opportunity_gap') }}
),

mapped_vacancies as (
    select
        v.occupation_title,
        m.uac_field_of_study,
        v.vacancies,
        v.vacancies_12m_ago,
        v.vacancy_growth_12m
    from vacancies v
    inner join mapping m on v.occupation_title = m.anzsco2_title
)

select
    mv.occupation_title,
    mv.uac_field_of_study,
    mv.vacancies,
    mv.vacancies_12m_ago,
    mv.vacancy_growth_12m,
    og.opportunity_gap,
    og.opportunity_rank,
    og.preference_share,
    row_number() over (order by mv.vacancy_growth_12m desc nulls last) as growth_rank,
    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id
from mapped_vacancies mv
left join opportunity og on mv.uac_field_of_study = og.field_of_study
order by mv.vacancy_growth_12m desc nulls last
