{{ config(materialized='table') }}

-- Institution × field enrolment profile from DET Higher Education data.
-- Grain: institution × uac_field_of_study (latest year snapshot).
-- Enriched with sector benchmarks and opportunity gap context.

with enrolments as (
    select * from {{ ref('stg_det_he_enrolments') }}
),

latest_year as (
    select max(year) as max_year from enrolments
),

-- Aggregate to institution × field for the latest year
inst_field as (
    select
        e.institution,
        e.uac_field_of_study,
        sum(e.enrolment_count) as total_enrolments,
        sum(case when e.citizenship = 'International' then e.enrolment_count else 0 end) as international_enrolments,
        sum(case when e.mode_of_attendance = 'External' then e.enrolment_count else 0 end) as external_enrolments,
        sum(case when e.gender = 'Female' then e.enrolment_count else 0 end) as female_enrolments,
        sum(case when e.commencing = 'Commencing' then e.enrolment_count else 0 end) as commencing_enrolments
    from enrolments e
    cross join latest_year ly
    where e.year = ly.max_year
    group by e.institution, e.uac_field_of_study
),

-- Sector-level benchmarks (all institutions aggregated)
sector as (
    select
        uac_field_of_study,
        sum(total_enrolments) as sector_total,
        sum(international_enrolments) as sector_international,
        sum(female_enrolments) as sector_female
    from inst_field
    group by uac_field_of_study
),

-- Join and compute metrics
enriched as (
    select
        i.institution,
        i.uac_field_of_study,
        i.total_enrolments,
        i.international_enrolments,
        i.external_enrolments,
        i.female_enrolments,
        i.commencing_enrolments,

        -- Institution-level shares
        round(i.international_enrolments * 1.0 / nullif(i.total_enrolments, 0), 4) as international_share,
        round(i.external_enrolments * 1.0 / nullif(i.total_enrolments, 0), 4) as external_share,
        round(i.female_enrolments * 1.0 / nullif(i.total_enrolments, 0), 4) as female_share,
        round(i.commencing_enrolments * 1.0 / nullif(i.total_enrolments, 0), 4) as commencing_share,

        -- Sector-level shares for comparison
        round(s.sector_international * 1.0 / nullif(s.sector_total, 0), 4) as sector_international_share,
        round(s.sector_female * 1.0 / nullif(s.sector_total, 0), 4) as sector_female_share,

        -- International index (>1.0 = over-indexed vs sector)
        round(
            (i.international_enrolments * 1.0 / nullif(i.total_enrolments, 0))
            / nullif(s.sector_international * 1.0 / nullif(s.sector_total, 0), 0),
            2
        ) as international_index,

        -- Rank fields within each institution by enrolment size
        row_number() over (
            partition by i.institution
            order by i.total_enrolments desc
        ) as field_rank_in_institution

    from inst_field i
    inner join sector s on i.uac_field_of_study = s.uac_field_of_study
),

-- Join with opportunity gap for demand context
with_opp as (
    select
        e.*,
        og.opportunity_gap,
        og.opportunity_rank
    from enriched e
    left join {{ ref('opportunity_gap') }} og
        on e.uac_field_of_study = og.field_of_study
)

select
    institution,
    uac_field_of_study,
    total_enrolments,
    international_enrolments,
    external_enrolments,
    female_enrolments,
    commencing_enrolments,
    international_share,
    sector_international_share,
    international_index,
    external_share,
    female_share,
    sector_female_share,
    commencing_share,
    field_rank_in_institution,
    opportunity_gap,
    opportunity_rank,
    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id
from with_opp
order by institution, field_rank_in_institution
