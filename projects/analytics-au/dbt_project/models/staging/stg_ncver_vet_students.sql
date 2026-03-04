{{ config(materialized='view') }}

-- Clean NCVER VET students data for analysis.
-- Only includes male/female gender rows (no "other" — very small, only from 2019).
-- Excludes the national total row since state-level data can be summed as needed.

with source as (
    select * from {{ source('dagster', 'ncver_vet_students') }}
)

select
    year,
    state,
    gender,
    students_thousands,
    students
from source
where gender in ('male', 'female')
  and state <> 'National'
