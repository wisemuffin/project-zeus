{{ config(materialized='view') }}

with source as (
    select state, skill_level, date, vacancies
    from {{ source('dagster', 'job_market') }}
    where state != 'AUST'
      and skill_level > 0
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
        sum(case when s.skill_level in (1, 2) then s.vacancies else 0 end) as graduate_vacancies,
        sum(s.vacancies) as total_vacancies
    from source s
    cross join latest_date ld
    where s.date = ld.max_date
    group by s.state
),

prior as (
    select
        s.state,
        sum(case when s.skill_level in (1, 2) then s.vacancies else 0 end) as graduate_vacancies_12m_ago,
        sum(s.vacancies) as total_vacancies_12m_ago
    from source s
    cross join closest_prior_date cpd
    where s.date = cpd.prior_date
    group by s.state
)

select
    l.state,
    l.graduate_vacancies,
    l.total_vacancies,
    p.graduate_vacancies_12m_ago,
    case
        when p.graduate_vacancies_12m_ago > 0
        then round((l.graduate_vacancies - p.graduate_vacancies_12m_ago) * 1.0
             / p.graduate_vacancies_12m_ago, 4)
        else null
    end as graduate_vacancy_growth_12m,
    case
        when p.total_vacancies_12m_ago > 0
        then round((l.total_vacancies - p.total_vacancies_12m_ago) * 1.0
             / p.total_vacancies_12m_ago, 4)
        else null
    end as total_vacancy_growth_12m
from latest l
left join prior p on l.state = p.state
