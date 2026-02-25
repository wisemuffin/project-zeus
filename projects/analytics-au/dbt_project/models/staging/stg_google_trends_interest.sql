{{ config(materialized='view') }}

-- Staging view for Google Trends university search interest.
-- Passes through with clean column types; join key is `university`
-- (matches qilt_institution_scores.institution).

select
    university,
    search_name,
    date,
    interest
from {{ source('dagster', 'google_trends_interest') }}
where interest is not null
