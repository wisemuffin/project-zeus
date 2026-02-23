{{ config(materialized='view') }}

select
    'SA/NT' as state,
    case field_of_study
        when 'Agriculture, Environmental and Related Studies'
            then 'Agriculture, Environmental & Related Studies'
        when 'Engineering and Related Technologies'
            then 'Engineering & Related Technologies'
        when 'Natural and Physical Sciences'
            then 'Natural & Physical Sciences'
        else field_of_study
    end as field_of_study,
    gender,
    preference_share,
    first_preferences
from {{ source('dagster', 'satac_fos_preferences') }}
where field_of_study != 'Mixed Field Programmes'
