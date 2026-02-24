{{ config(materialized='table') }}

-- Per-applicant-type field affinity with outcomes context.
-- Grain: (applicant_type, field_of_study).
-- Shows which segments over-index on which fields for targeted marketing.

with segments as (
    select * from {{ ref('stg_uac_fos_by_app_type') }}
),

-- Total preference shares across all applicants for affinity index calculation
total_prefs as (
    select
        field_of_study,
        preference_share as total_preference_share
    from segments
    where applicant_type = 'Total'
),

opportunity as (
    select * from {{ ref('opportunity_gap') }}
),

outcomes as (
    select
        field_of_study,
        ft_employment_rate,
        median_salary
    from {{ ref('graduate_outcomes_by_fos') }}
),

affinity as (
    select
        s.applicant_type,
        s.field_of_study,
        s.preference_share,
        tp.total_preference_share,
        case
            when tp.total_preference_share > 0
            then round(s.preference_share / tp.total_preference_share, 2)
            else null
        end as segment_affinity_index,
        og.opportunity_gap,
        og.vacancy_growth_12m,
        oc.ft_employment_rate,
        oc.median_salary,
        row_number() over (
            partition by s.applicant_type
            order by s.preference_share desc
        ) as segment_rank
    from segments s
    left join total_prefs tp on s.field_of_study = tp.field_of_study
    left join opportunity og on s.field_of_study = og.field_of_study
    left join outcomes oc on s.field_of_study = oc.field_of_study
    where s.applicant_type != 'Total'
)

select
    applicant_type,
    field_of_study,
    preference_share,
    segment_affinity_index,
    opportunity_gap,
    ft_employment_rate,
    median_salary,
    vacancy_growth_12m,
    segment_rank
from affinity
order by applicant_type, segment_rank
