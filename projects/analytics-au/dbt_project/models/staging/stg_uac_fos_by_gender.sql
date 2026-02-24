{{ config(materialized='view') }}

select
    case field_of_study
        when 'Engineering & Related Tech.' then 'Engineering & Related Technologies'
        when 'Agriculture & Environmental' then 'Agriculture, Environmental & Related Studies'
        else field_of_study
    end as field_of_study,
    gender,
    share as preference_share
from {{ source('dagster', 'uac_fos_by_gender') }}
