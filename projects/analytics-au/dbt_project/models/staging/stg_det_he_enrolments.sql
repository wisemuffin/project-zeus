{{ config(materialized='view') }}

-- Map DET Higher Education enrolment data from ASCED broad field names
-- to UAC field of study categories for joins with opportunity gap,
-- graduate outcomes, and preference data.

with source as (
    select * from {{ source('dagster', 'det_he_enrolments') }}
),

mapped as (
    select
        year,
        institution,
        state,
        case citizenship when 'Overseas' then 'International' else citizenship end as citizenship,
        commencing,
        broad_course_level,
        detailed_course_level,
        gender,
        mode_of_attendance,
        type_of_attendance,
        broad_field_of_education_primary,
        enrolment_count,

        case broad_field_of_education_primary
            when 'Natural and Physical Sciences' then 'Natural & Physical Sciences'
            when 'Information Technology' then 'Information Technology'
            when 'Engineering and Related Technologies' then 'Engineering & Related Technologies'
            when 'Architecture and Building' then 'Architecture & Building'
            when 'Agriculture Environmental and Related Studies' then 'Agriculture, Environmental & Related Studies'
            when 'Health' then 'Health'
            when 'Education' then 'Education'
            when 'Management and Commerce' then 'Management & Commerce'
            when 'Society and Culture' then 'Society & Culture'
            when 'Creative Arts' then 'Creative Arts'
            when 'Food Hospitality and Personal Services' then 'Food, Hospitality & Personal Services'
            else null
        end as uac_field_of_study

    from source
    where broad_field_of_education_primary is not null
      and broad_field_of_education_primary not in (
          'Mixed Field Programs', 'Mixed Field Programmes',
          'Non-Award course', 'Non-Award Courses',
          'Non-Award/Microcredentials', 'Not provided'
      )
)

select * from mapped
where uac_field_of_study is not null
