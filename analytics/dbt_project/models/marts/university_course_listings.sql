{{ config(materialized='table') }}

-- Program-level marketing recommendations: CRICOS courses enriched with
-- opportunity gap and graduate outcomes data. Enables "University X offers
-- 3 Engineering programs in NSW — a field with +12% opportunity gap and
-- 85% FT employment" style recommendations.

with courses as (
    select * from {{ ref('stg_cricos_courses') }}
),

opportunity as (
    select * from {{ ref('opportunity_gap') }}
),

outcomes as (
    select * from {{ ref('graduate_outcomes_by_fos') }}
),

-- Count how many courses each institution offers per field
institution_field_counts as (
    select
        cricos_provider_code,
        uac_field_of_study,
        count(distinct cricos_course_code) as course_count_in_field
    from courses
    group by cricos_provider_code, uac_field_of_study
)

select
    -- Institution
    c.institution_name,
    c.institution_type,
    c.cricos_provider_code,

    -- Course
    c.course_name,
    c.course_level,
    c.narrow_field,
    c.duration_weeks,
    c.estimated_total_cost,

    -- Location
    c.location_state,
    c.location_city,

    -- Field context (from opportunity gap)
    c.uac_field_of_study,
    og.opportunity_gap,
    og.opportunity_rank,
    og.vacancy_growth_12m,

    -- Graduate outcomes (from QILT GOS)
    oc.ft_employment_rate,
    oc.median_salary,
    oc.marketing_signal,

    -- Derived: institution breadth in this field
    ifc.course_count_in_field

from courses c
left join opportunity og
    on c.uac_field_of_study = og.field_of_study
left join outcomes oc
    on c.uac_field_of_study = oc.field_of_study
left join institution_field_counts ifc
    on c.cricos_provider_code = ifc.cricos_provider_code
    and c.uac_field_of_study = ifc.uac_field_of_study

order by og.opportunity_rank nulls last, c.institution_name, c.course_name
