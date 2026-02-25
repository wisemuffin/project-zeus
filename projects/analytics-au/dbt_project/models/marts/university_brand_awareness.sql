{{ config(materialized='table') }}

-- Per-university brand awareness analysis combining Google Trends search interest
-- (time series + geographic) with QILT institution scorecard quality metrics.
-- Key insight: interest-quality gap identifies universities that are under-searched
-- relative to their academic quality — prime candidates for marketing investment.

with time_series as (
    select * from {{ ref('stg_google_trends_interest') }}
),

-- Recent 12-month window for avg_interest_12m
recent_cutoff as (
    select max(date) - interval '12 months' as cutoff_date
    from time_series
),

interest_summary as (
    select
        ts.university,
        round(avg(ts.interest), 1) as avg_interest_all,
        max(ts.interest) as peak_interest,
        round(
            avg(case when ts.date >= rc.cutoff_date then ts.interest end),
            1
        ) as avg_interest_12m
    from time_series ts
    cross join recent_cutoff rc
    group by ts.university
),

interest_ranked as (
    select
        *,
        row_number() over (order by avg_interest_12m desc nulls last) as interest_rank
    from interest_summary
),

state_interest as (
    select * from {{ ref('stg_google_trends_interest_by_state') }}
),

-- Find each university's top state by interest
top_state as (
    select
        university,
        state as top_state,
        interest as top_state_interest,
        row_number() over (
            partition by university order by interest desc
        ) as rn
    from state_interest
),

top_state_picked as (
    select university, top_state, top_state_interest
    from top_state
    where rn = 1
),

scorecard as (
    select * from {{ ref('institution_scorecard') }}
)

select
    sc.institution as university,

    -- Search interest (time series)
    ir.avg_interest_12m,
    ir.avg_interest_all,
    ir.peak_interest,
    ir.interest_rank,

    -- Search interest (geographic)
    ts.top_state,
    ts.top_state_interest,

    -- Institution quality & outcomes
    sc.overall_quality,
    sc.ft_employment_rate,
    sc.median_salary,
    sc.quality_rank,
    sc.employment_rank,
    sc.salary_rank,

    -- Interest-quality gap: positive = under-searched relative to quality
    -- (marketing opportunity), negative = strong brand already
    sc.quality_rank - ir.interest_rank as interest_quality_gap,

    -- Awareness tier based on interest_rank terciles
    case
        when ir.interest_rank <= 14 then 'High'
        when ir.interest_rank <= 28 then 'Medium'
        else 'Low'
    end as awareness_tier,

    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id

from scorecard sc
left join interest_ranked ir on ir.university = sc.institution
left join top_state_picked ts on ts.university = sc.institution
order by ir.interest_rank asc nulls last
