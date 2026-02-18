{{ config(materialized='view') }}

-- Map QILT study areas to UAC fields of study for SES satisfaction data.
-- Same mapping as stg_qilt_graduate_outcomes.

with source as (
    select * from {{ source('dagster', 'qilt_student_experience') }}
),

mapped as (
    select
        study_area,
        skills_development,
        peer_engagement,
        teaching_quality,
        student_support,
        learning_resources,
        overall_quality,
        case study_area
            when 'Agriculture and environmental studies'
                then 'Agriculture, Environmental & Related Studies'
            when 'Architecture and built environment'
                then 'Architecture & Building'
            when 'Business and management'
                then 'Management & Commerce'
            when 'Communications'
                then 'Society & Culture'
            when 'Computing and information systems'
                then 'Information Technology'
            when 'Creative arts'
                then 'Creative Arts'
            when 'Dentistry'
                then 'Health'
            when 'Engineering'
                then 'Engineering & Related Technologies'
            when 'Health services and support'
                then 'Health'
            when 'Humanities, culture and social sciences'
                then 'Society & Culture'
            when 'Law and paralegal studies'
                then 'Society & Culture'
            when 'Medicine'
                then 'Health'
            when 'Nursing'
                then 'Health'
            when 'Pharmacy'
                then 'Health'
            when 'Psychology'
                then 'Society & Culture'
            when 'Rehabilitation'
                then 'Health'
            when 'Science and mathematics'
                then 'Natural & Physical Sciences'
            when 'Social work'
                then 'Society & Culture'
            when 'Teacher education'
                then 'Education'
            when 'Tourism, hospitality, personal services, sport and recreation'
                then 'Food, Hospitality & Personal Services'
            when 'Veterinary science'
                then 'Natural & Physical Sciences'
        end as uac_field_of_study
    from source
)

select * from mapped
