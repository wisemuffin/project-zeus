{{ config(materialized='view') }}

-- Map QILT study areas (ASCED-based, 21 categories) to UAC broad fields of study
-- so graduate outcomes can join with UAC preference data and opportunity gap analysis.
-- Multiple QILT areas map to a single UAC field (e.g. Dentistry, Medicine, Nursing → Health).

with source as (
    select * from {{ source('dagster', 'qilt_graduate_outcomes') }}
),

mapped as (
    select
        study_area,
        ft_employment_rate,
        ft_employment_rate_prior,
        overall_employment_rate,
        overall_employment_rate_prior,
        lf_participation_rate,
        lf_participation_rate_prior,
        median_salary,
        median_salary_prior,
        median_salary_male,
        median_salary_female,
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
