{{ config(materialized='view') }}

with source as (
    select * from {{ source('dagster', 'courseseeker_atar') }}
),

mapped as (
    select
        course_name,
        course_code_tac,
        admission_centre,
        institution_name,
        institution_code,
        study_area,
        study_area_primary,
        level_of_qualification,
        state,
        campus_name,
        duration,

        -- ATAR profile
        atar_collection_year,
        lowest_atar_unadjusted,
        lowest_atar_adjusted,
        median_atar_unadjusted,
        median_atar_adjusted,
        highest_atar_unadjusted,
        highest_atar_adjusted,

        -- Student profile
        pct_admitted_atar,
        pct_admitted_he,
        pct_admitted_vet,
        pct_admitted_other,
        pct_international,
        total_students,

        -- Map ASCED broad study area to UAC field of study
        case study_area
            when 'Natural and Physical Sciences' then 'Natural & Physical Sciences'
            when 'Information Technology' then 'Information Technology'
            when 'Engineering and Related Technologies' then 'Engineering & Related Technologies'
            when 'Architecture and Building' then 'Architecture & Building'
            when 'Agriculture, Environmental and Related Studies' then 'Agriculture, Environmental & Related Studies'
            when 'Health' then 'Health'
            when 'Education' then 'Education'
            when 'Management and Commerce' then 'Management & Commerce'
            when 'Society and Culture' then 'Society & Culture'
            when 'Creative Arts' then 'Creative Arts'
            when 'Food, Hospitality and Personal Services' then 'Food, Hospitality & Personal Services'
            else null
        end as uac_field_of_study

    from source
    where study_area is not null
)

select * from mapped
where uac_field_of_study is not null
