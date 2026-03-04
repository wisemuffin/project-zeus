{{ config(materialized='view') }}

select
    uac_field_of_study as field_of_study,
    estimated_cpc_aud,
    estimated_cpl_aud,
    estimated_ctr_pct,
    source_note
from {{ source('dagster', 'ad_cost_benchmarks') }}
