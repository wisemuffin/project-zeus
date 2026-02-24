{{ config(materialized='view') }}

with unpivoted as (
    UNPIVOT {{ source('dagster', 'uac_early_bird_closing_count') }}
    ON COLUMNS(* EXCLUDE (applicant_type))
    INTO NAME intake_year_range VALUE applicant_count
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
