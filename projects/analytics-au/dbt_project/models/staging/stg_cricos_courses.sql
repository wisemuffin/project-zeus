{{ config(materialized='view') }}

-- Map CRICOS ASCED broad field codes to UAC field of study categories
-- so course listings can join with opportunity gap and graduate outcomes analysis.
-- The broad_field column contains strings like "09 - Society and Culture";
-- we extract the 2-digit code to map deterministically.

with source as (
    select * from {{ source('dagster', 'cricos_courses') }}
),

mapped as (
    select
        cricos_provider_code,
        institution_name,
        institution_type,
        cricos_course_code,
        course_name,
        course_level,
        broad_field,
        narrow_field,
        duration_weeks,
        estimated_total_cost,
        location_state,
        location_city,

        -- Extract 2-digit ASCED code from broad_field (e.g. "09 - Society and Culture" → "09")
        left(trim(broad_field), 2) as asced_broad_code,

        case left(trim(broad_field), 2)
            when '01' then 'Natural & Physical Sciences'
            when '02' then 'Information Technology'
            when '03' then 'Engineering & Related Technologies'
            when '04' then 'Architecture & Building'
            when '05' then 'Agriculture, Environmental & Related Studies'
            when '06' then 'Health'
            when '07' then 'Education'
            when '08' then 'Management & Commerce'
            when '09' then 'Society & Culture'
            when '10' then 'Creative Arts'
            when '11' then 'Food, Hospitality & Personal Services'
            -- 12 (Mixed Field Programmes) excluded — no UAC equivalent
            else null
        end as uac_field_of_study

    from source
)

select * from mapped
where uac_field_of_study is not null
