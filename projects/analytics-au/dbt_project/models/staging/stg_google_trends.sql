{{ config(materialized='view') }}

select
    trend,
    traffic,
    published,
    top_article_headline,
    top_article_source,
    top_article_url,
    explore_link,
    case
        when regexp_matches(lower(trend), '(health|medical|nurse|doctor|hospital|pharma|mental health|aged care|dental|physio)')
            then 'Health'
        when regexp_matches(lower(trend), '(software|cyber|ai |data|tech|coding|computer|hack|app |digital|cloud|atlassian|google|microsoft|apple|openai|anthropic|claude|chatgpt|nvidia)')
            then 'Information Technology'
        when regexp_matches(lower(trend), '(business|finance|bank|economy|market|trade|invest|stock|share price|accounting|tax|nab |cba |anz )')
            then 'Management & Commerce'
        when regexp_matches(lower(trend), '(teacher|school|education|university|student|hsc|atar|exam)')
            then 'Education'
        when regexp_matches(lower(trend), '(engineer|construction|mining|manufacturing)')
            then 'Engineering & Related Technologies'
        when regexp_matches(lower(trend), '(architect|building|property|housing|real estate)')
            then 'Architecture & Building'
        when regexp_matches(lower(trend), '(science|climate|research|physics|chemistry|biology|space|nasa)')
            then 'Natural & Physical Sciences'
        when regexp_matches(lower(trend), '(art |music|film|movie|album|concert|tickets|festival|gallery|design|creative)')
            then 'Creative Arts'
        when regexp_matches(lower(trend), '(law|court|politic|social|rights|parliament|election|crime|police|justice)')
            then 'Society & Culture'
        else null
    end as matched_field_of_study
from {{ source('dagster', 'google_trends') }}
