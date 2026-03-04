SELECT 'qilt_gos' AS source_key,
       'QILT Graduate Outcomes Survey' AS source_label,
       MAX(survey_year)::VARCHAR AS data_period
FROM marts.graduate_outcomes_by_fos

UNION ALL
SELECT 'qilt_ses', 'QILT Student Experience Survey', '2024'

UNION ALL
SELECT 'qilt_ess', 'QILT Employer Satisfaction Survey', '2024'

UNION ALL
SELECT 'ivi', 'Internet Vacancy Index (IVI)',
       strftime(MAX(date), '%B %Y')
FROM public.job_market_occupations

UNION ALL
SELECT 'uac', 'UAC Preferences',
       MAX(latest_intake)
FROM marts.historical_demand_trends

UNION ALL
SELECT 'google_trends', 'Google Trends',
       strftime(MAX(published), '%d %b %Y')
FROM marts.trending_interests

UNION ALL
SELECT 'abs_population', 'ABS Population Estimates', '2023'

UNION ALL
SELECT 'ncver_vet', 'NCVER VET Students',
       MAX(latest_year)::VARCHAR
FROM marts.vet_competition_by_state

UNION ALL
SELECT 'cricos', 'CRICOS Course Register',
       strftime(MAX(_loaded_at), '%d %b %Y')
FROM marts.university_course_listings

UNION ALL
SELECT 'google_trends_brand', 'Google Trends (Brand)',
       strftime(MAX(_loaded_at), '%b %Y')
FROM marts.university_brand_awareness

UNION ALL
SELECT 'det_enrolments', 'DET Higher Education Enrolments', '2020'

UNION ALL
SELECT 'uac_state', 'UAC/VTAC/SATAC Preferences', '2024-25'

UNION ALL
SELECT 'wordstream', 'WordStream Ad Benchmarks', '2025'
