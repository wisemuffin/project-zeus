{{ config(materialized='table') }}

with trends as (
    select * from {{ ref('stg_google_trends') }}
),

opportunity as (
    select * from {{ ref('opportunity_gap') }}
)

select
    t.trend,
    t.traffic,
    t.published,
    t.top_article_headline,
    t.top_article_source,
    t.top_article_url,
    t.explore_link,
    t.matched_field_of_study,
    o.opportunity_gap,
    o.opportunity_rank,
    o.vacancy_growth_12m,
    case
        when o.opportunity_gap > 0 then 'High opportunity — align ad creative with this trend'
        when o.opportunity_gap is not null then 'Low opportunity — deprioritise'
        when t.matched_field_of_study is null then 'Unclassified — review manually'
        else 'Unmapped field'
    end as marketing_signal,
    current_timestamp as _loaded_at,
    '{{ var("dagster_run_id", "manual") }}' as _dagster_run_id
from trends t
left join opportunity o on t.matched_field_of_study = o.field_of_study
order by t.published desc
