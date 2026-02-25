{{ config(materialized='view') }}

-- Staging view for Google Trends state-level university search interest.
-- Maps full state names from Google Trends to project-standard 2-letter codes.
-- Join key is `university` (matches qilt_institution_scores.institution).

select
    university,
    search_name,
    state_name,
    case state_name
        when 'New South Wales' then 'NSW'
        when 'Victoria' then 'VIC'
        when 'Queensland' then 'QLD'
        when 'South Australia' then 'SA'
        when 'Western Australia' then 'WA'
        when 'Tasmania' then 'TAS'
        when 'Northern Territory' then 'NT'
        when 'Australian Capital Territory' then 'ACT'
    end as state,
    interest
from {{ source('dagster', 'google_trends_interest_by_state') }}
where interest is not null
