{{ config(materialized='table') }}

with mapping as (
    select anzsco2_title, uac_field_of_study
    from {{ source('dagster', 'occupation_fos_mapping') }}
),

vacancies as (
    select * from {{ ref('stg_job_vacancies_by_occupation') }}
),

preferences as (
    select * from {{ ref('stg_uac_fos_preferences') }}
),

vacancies_by_fos as (
    select
        m.uac_field_of_study as field_of_study,
        sum(v.vacancies) as total_vacancies,
        sum(v.vacancies_12m_ago) as total_vacancies_12m_ago,
        case
            when sum(v.vacancies_12m_ago) > 0
            then round(
                (sum(v.vacancies) - sum(v.vacancies_12m_ago)) * 1.0
                / sum(v.vacancies_12m_ago), 4
            )
            else null
        end as vacancy_growth_12m
    from mapping m
    inner join vacancies v on m.anzsco2_title = v.occupation_title
    group by m.uac_field_of_study
),

total_mapped as (
    select sum(total_vacancies) as grand_total from vacancies_by_fos
),

gap_analysis as (
    select
        vf.field_of_study,
        vf.total_vacancies,
        round(vf.total_vacancies * 1.0 / tm.grand_total, 4) as vacancy_share,
        p.preference_share,
        round(
            (vf.total_vacancies * 1.0 / tm.grand_total) - p.preference_share, 4
        ) as opportunity_gap,
        vf.vacancy_growth_12m
    from vacancies_by_fos vf
    cross join total_mapped tm
    left join preferences p on vf.field_of_study = p.field_of_study
)

select
    field_of_study,
    total_vacancies,
    vacancy_share,
    preference_share,
    opportunity_gap,
    vacancy_growth_12m,
    row_number() over (order by opportunity_gap desc) as opportunity_rank
from gap_analysis
order by opportunity_gap desc
