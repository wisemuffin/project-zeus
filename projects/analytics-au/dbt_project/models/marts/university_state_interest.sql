{{ config(materialized='table') }}

-- University × state search interest matrix with rankings and deviation from mean.
-- Grain: university × state (~336 rows). Enables geo-targeted campaign allocation
-- by showing which states each university is strongest/weakest in, and which
-- universities dominate search interest within each state.

with state_interest as (
    select * from {{ ref('stg_google_trends_interest_by_state') }}
),

uni_avg as (
    select
        university,
        avg(interest) as avg_interest
    from state_interest
    group by university
)

select
    si.university,
    si.state,
    si.state_name,
    si.interest,

    -- For each university: which states rank highest
    row_number() over (
        partition by si.university order by si.interest desc
    ) as state_rank_for_uni,

    -- For each state: which universities rank highest
    row_number() over (
        partition by si.state order by si.interest desc
    ) as uni_rank_in_state,

    -- Deviation from uni's mean across states
    round(si.interest - ua.avg_interest, 1) as interest_vs_uni_avg,

    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id

from state_interest si
left join uni_avg ua on ua.university = si.university
order by si.university, si.state
