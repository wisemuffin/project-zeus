{{ config(materialized='view') }}

with source as (
    select * from {{ source('dagster', 'qilt_employer_satisfaction_by_field') }}
),

mapped as (
    select
        broad_field_of_education,
        foundation_skills,
        adaptive_skills,
        collaborative_skills,
        technical_skills,
        employability_skills,
        overall_employer_satisfaction,

        -- Map ESS broad field names (lowercase with &) to UAC field of study
        case broad_field_of_education
            when 'Natural & physical sciences' then 'Natural & Physical Sciences'
            when 'Information technology' then 'Information Technology'
            when 'Engineering & related technologies' then 'Engineering & Related Technologies'
            when 'Architecture & building' then 'Architecture & Building'
            when 'Agriculture, environmental & related studies' then 'Agriculture, Environmental & Related Studies'
            when 'Health' then 'Health'
            when 'Education' then 'Education'
            when 'Management & commerce' then 'Management & Commerce'
            when 'Society & culture' then 'Society & Culture'
            when 'Creative arts' then 'Creative Arts'
            when 'Food, hospitality & personal services' then 'Food, Hospitality & Personal Services'
            else null
        end as uac_field_of_study

    from source
    where broad_field_of_education is not null
      and broad_field_of_education != 'Total'
)

select * from mapped
where uac_field_of_study is not null
