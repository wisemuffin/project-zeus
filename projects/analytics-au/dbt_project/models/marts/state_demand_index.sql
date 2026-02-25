{{ config(materialized='table') }}

with vacancies as (
    select * from {{ ref('stg_job_vacancies_by_state') }}
),

population as (
    select * from {{ ref('stg_youth_population_by_state') }}
),

joined as (
    select
        v.state,
        v.graduate_vacancies,
        v.total_vacancies,
        p.youth_population_15_19,
        round(v.graduate_vacancies * 1000.0 / p.youth_population_15_19, 1) as graduate_vacancies_per_1k_youth,
        round(v.total_vacancies * 1000.0 / p.youth_population_15_19, 1) as total_vacancies_per_1k_youth,
        round(v.graduate_vacancies * 1.0 / v.total_vacancies, 4) as graduate_share_of_vacancies,
        v.graduate_vacancy_growth_12m,
        v.total_vacancy_growth_12m
    from vacancies v
    inner join population p on v.state = p.state
)

select
    *,
    row_number() over (order by graduate_vacancies_per_1k_youth desc) as demand_rank,
    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id
from joined
order by graduate_vacancies_per_1k_youth desc
