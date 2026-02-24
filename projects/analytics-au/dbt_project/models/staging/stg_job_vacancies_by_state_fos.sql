{{ config(materialized='view') }}

with source as (
    select title, state, date, vacancies
    from {{ source('dagster', 'job_market_occupations') }}
),

mapping as (
    select anzsco2_title, uac_field_of_study
    from {{ source('dagster', 'occupation_fos_mapping') }}
),

latest_date as (
    select max(date) as max_date from source
),

closest_prior_date as (
    select max(s.date) as prior_date
    from source s
    cross join latest_date ld
    where s.date <= ld.max_date - interval '12 months'
),

latest as (
    select
        s.state,
        m.uac_field_of_study as field_of_study,
        sum(s.vacancies) as vacancies
    from source s
    cross join latest_date ld
    inner join mapping m on s.title = m.anzsco2_title
    where s.date = ld.max_date
      and s.title != upper(s.title)
      and s.state != 'AUST'
      and s.vacancies is not null
    group by s.state, m.uac_field_of_study
),

prior as (
    select
        s.state,
        m.uac_field_of_study as field_of_study,
        sum(s.vacancies) as vacancies_12m_ago
    from source s
    cross join closest_prior_date cpd
    inner join mapping m on s.title = m.anzsco2_title
    where s.date = cpd.prior_date
      and s.title != upper(s.title)
      and s.state != 'AUST'
      and s.vacancies is not null
    group by s.state, m.uac_field_of_study
)

select
    l.state,
    l.field_of_study,
    l.vacancies,
    p.vacancies_12m_ago,
    case
        when p.vacancies_12m_ago > 0
        then round((l.vacancies - p.vacancies_12m_ago) * 1.0 / p.vacancies_12m_ago, 4)
        else null
    end as vacancy_growth_12m
from latest l
left join prior p on l.state = p.state and l.field_of_study = p.field_of_study
