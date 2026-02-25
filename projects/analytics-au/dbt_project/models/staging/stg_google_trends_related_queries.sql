{{ config(materialized='view') }}

-- Staging view for Google Trends related queries (top and rising).
-- Filters out null queries. Join key is `university`
-- (matches qilt_institution_scores.institution).

select
    university,
    search_name,
    related_query,
    query_type,
    value
from {{ source('dagster', 'google_trends_related_queries') }}
where related_query is not null
