{{ config(materialized='view') }}

with source as (
    select title, state, date, vacancies
    from {{ source('dagster', 'job_market_occupations') }}
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

latest_vacancies as (
    select s.title as occupation_title, s.vacancies
    from source s
    cross join latest_date ld
    where s.date = ld.max_date
      and s.title != upper(s.title)
      and upper(s.state) = 'AUST'
      and s.vacancies is not null
),

prior_vacancies as (
    select s.title as occupation_title, s.vacancies as vacancies_12m_ago
    from source s
    cross join closest_prior_date cpd
    where s.date = cpd.prior_date
      and s.title != upper(s.title)
      and upper(s.state) = 'AUST'
      and s.vacancies is not null
)

select
    lv.occupation_title,
    lv.vacancies,
    pv.vacancies_12m_ago,
    case
        when pv.vacancies_12m_ago > 0
        then round((lv.vacancies - pv.vacancies_12m_ago) * 1.0 / pv.vacancies_12m_ago, 4)
        else null
    end as vacancy_growth_12m
from latest_vacancies lv
left join prior_vacancies pv on lv.occupation_title = pv.occupation_title
