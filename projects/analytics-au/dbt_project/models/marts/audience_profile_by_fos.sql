{{ config(materialized='table') }}

with app_type as (
    select * from {{ ref('stg_uac_fos_by_app_type') }}
),

gender as (
    select * from {{ ref('stg_uac_fos_by_gender') }}
),

opportunity as (
    select * from {{ ref('opportunity_gap') }}
),

app_type_pivoted as (
    select
        field_of_study,
        max(case when applicant_type = 'Total' then preference_share end) as total_preference_share,
        max(case when applicant_type = 'NSW' then preference_share end) as nsw_preference_share,
        max(case when applicant_type = 'ACT' then preference_share end) as act_preference_share,
        max(case when applicant_type = 'Interstate & IB' then preference_share end) as interstate_preference_share,
        max(case when applicant_type = 'Non-Year 12' then preference_share end) as non_yr12_preference_share
    from app_type
    group by field_of_study
),

gender_pivoted as (
    select
        field_of_study,
        max(case when gender = 'Female' then preference_share end) as female_preference_share,
        max(case when gender = 'Male' then preference_share end) as male_preference_share
    from gender
    group by field_of_study
),

profiles as (
    select
        a.field_of_study,

        -- opportunity context
        o.opportunity_gap,
        o.opportunity_rank,
        o.vacancy_share,

        -- gender targeting
        g.female_preference_share,
        g.male_preference_share,
        case
            when g.female_preference_share > g.male_preference_share then 'Female'
            when g.male_preference_share > g.female_preference_share then 'Male'
            else 'Balanced'
        end as gender_skew,

        -- age proxy: mature learner affinity
        -- ratio > 1 means Non-Year 12 (mature) students over-index on this FOS
        a.non_yr12_preference_share,
        a.total_preference_share,
        case
            when a.total_preference_share > 0
            then round(a.non_yr12_preference_share / a.total_preference_share, 2)
            else null
        end as mature_learner_index,

        -- geographic origin
        a.nsw_preference_share,
        a.act_preference_share,
        a.interstate_preference_share,
        case
            when a.nsw_preference_share > 0
            then round(a.interstate_preference_share / a.nsw_preference_share, 2)
            else null
        end as interstate_draw_ratio

    from app_type_pivoted a
    left join gender_pivoted g on a.field_of_study = g.field_of_study
    left join opportunity o on a.field_of_study = o.field_of_study
)

select
    *,
    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id
from profiles
order by opportunity_rank nulls last
