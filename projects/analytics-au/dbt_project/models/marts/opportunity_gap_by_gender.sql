{{ config(materialized='table') }}

with gender as (
    select * from {{ ref('stg_uac_fos_by_gender') }}
),

opportunity as (
    select * from {{ ref('opportunity_gap') }}
),

pivoted as (
    select
        g.field_of_study,
        max(case when g.gender = 'Female' then g.preference_share end) as female_preference_share,
        max(case when g.gender = 'Male' then g.preference_share end) as male_preference_share
    from gender g
    group by g.field_of_study
)

select
    o.field_of_study,
    o.opportunity_gap,
    o.opportunity_rank,
    o.vacancy_share,
    o.vacancy_growth_12m,
    p.female_preference_share,
    p.male_preference_share,
    round(p.female_preference_share - p.male_preference_share, 4) as gender_skew,
    case
        when p.female_preference_share > p.male_preference_share then 'Female'
        when p.male_preference_share > p.female_preference_share then 'Male'
        else 'Balanced'
    end as skew_direction,
    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id
from opportunity o
inner join pivoted p on o.field_of_study = p.field_of_study
order by o.opportunity_rank
