{{ config(materialized='table') }}

-- ROI-adjusted field recommendations combining opportunity gap, graduate
-- outcomes, and ad cost benchmarks. Identifies which fields offer the best
-- return on ad spend — high demand gap with lower CPC.

with costs as (
    select * from {{ ref('stg_ad_cost_benchmarks') }}
),

opportunity as (
    select * from {{ ref('opportunity_gap') }}
),

outcomes as (
    select * from {{ ref('graduate_outcomes_by_fos') }}
),

median_cpc as (
    select percentile_cont(0.5) within group (order by estimated_cpc_aud) as median_val
    from costs
)

select
    c.field_of_study,

    -- Ad cost benchmarks
    c.estimated_cpc_aud,
    c.estimated_cpl_aud,
    c.estimated_ctr_pct,

    -- Opportunity gap context
    og.opportunity_gap,
    og.opportunity_rank,

    -- Graduate outcomes context
    o.ft_employment_rate,
    o.median_salary,

    -- ROI metrics
    round(coalesce(og.opportunity_gap, 0) / nullif(c.estimated_cpc_aud, 0), 6) as gap_per_cpc_dollar,
    round(coalesce(o.median_salary, 0) * coalesce(o.ft_employment_rate, 0) / 100.0, 0)::int as outcome_value_proxy,

    -- ROI tier classification
    case
        when og.opportunity_gap > 0 and c.estimated_cpc_aud < mc.median_val
            then 'High ROI'
        when og.opportunity_gap > 0 and c.estimated_cpc_aud >= mc.median_val
            then 'Strong demand'
        when coalesce(og.opportunity_gap, 0) <= 0 and c.estimated_cpc_aud < mc.median_val
            then 'Low cost'
        else 'Challenging'
    end as roi_tier,

    row_number() over (
        order by coalesce(og.opportunity_gap, 0) / nullif(c.estimated_cpc_aud, 0) desc
    ) as roi_rank,

    c.source_note,

    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id

from costs c
cross join median_cpc mc
left join opportunity og on c.field_of_study = og.field_of_study
left join outcomes o on c.field_of_study = o.field_of_study
order by gap_per_cpc_dollar desc
