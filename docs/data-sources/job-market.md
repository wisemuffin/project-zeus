# Job Market Data (Internet Vacancy Index)

Monthly Internet Vacancy Index (IVI) from Jobs and Skills Australia. Two assets cover this data:

- **`job_market`** — vacancies by ANZSCO skill level and state
- **`job_market_occupations`** — vacancies by ANZSCO2 occupation group and state

URL follows a publication-lag pattern: data for month X published in folder `{X+1}`.

For full documentation see the asset docstrings:
- `analytics/src/analytics/defs/assets/job_market.py`
- `analytics/src/analytics/defs/assets/job_market_occupations.py`
