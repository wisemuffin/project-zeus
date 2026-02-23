{{ config(materialized='view') }}

-- UAC (NSW/ACT) — Female and Male only
select
    'NSW/ACT' as state,
    field_of_study,
    gender,
    preference_share
from {{ ref('stg_uac_fos_by_gender') }}

union all

-- VTAC (VIC) — Female and Male only (exclude Total)
select
    state,
    field_of_study,
    gender,
    preference_share
from {{ ref('stg_vtac_fos_preferences') }}
where gender != 'Total'
