{{ config(materialized='view') }}

-- Rewritten from UNPIVOT to UNION ALL for dbt Fusion compatibility
-- (Fusion's SQL parser does not yet support DuckDB's UNPIVOT statement)

with source as (
    select * from {{ source('dagster', 'uac_early_bird_closing_count') }}
),

unpivoted as (
    select applicant_type, '2016–17' as intake_year_range, "2016–17" as applicant_count from source
    union all
    select applicant_type, '2017–18', "2017–18" from source
    union all
    select applicant_type, '2018–19', "2018–19" from source
    union all
    select applicant_type, '2019–20', "2019–20" from source
    union all
    select applicant_type, '2020–21', "2020–21" from source
    union all
    select applicant_type, '2021–22', "2021–22" from source
    union all
    select applicant_type, '2022–23', "2022–23" from source
    union all
    select applicant_type, '2023–24', "2023–24" from source
    union all
    select applicant_type, '2024–25', "2024–25" from source
    union all
    select applicant_type, '2025–26', "2025–26" from source
),

parsed as (
    select
        applicant_type,
        intake_year_range,
        CAST(LEFT(intake_year_range, 4) AS INTEGER) as intake_year,
        CAST(applicant_count AS INTEGER) as applicant_count
    from unpivoted
)

select
    applicant_type,
    intake_year_range,
    intake_year,
    applicant_count,
    LAG(applicant_count) OVER (PARTITION BY applicant_type ORDER BY intake_year) as prior_year_count,
    case
        when LAG(applicant_count) OVER (PARTITION BY applicant_type ORDER BY intake_year) > 0
        then round(
            (applicant_count - LAG(applicant_count) OVER (PARTITION BY applicant_type ORDER BY intake_year)) * 1.0
            / LAG(applicant_count) OVER (PARTITION BY applicant_type ORDER BY intake_year), 4
        )
        else null
    end as yoy_growth
from parsed
