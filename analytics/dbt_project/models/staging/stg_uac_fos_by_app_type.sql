{{ config(materialized='view') }}

select
    applicant_type,
    field_of_study,
    share as preference_share
from {{ source('dagster', 'uac_fos_by_app_type') }}
