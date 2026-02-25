from datetime import timedelta

import dagster as dg

from analytics_au.defs.assets.abs_lga_reference import abs_lga_reference
from analytics_au.defs.assets.abs_population_by_lga import abs_population_by_lga
from analytics_au.defs.assets.cricos_courses import cricos_courses
from analytics_au.defs.assets.google_trends import google_trends
from analytics_au.defs.assets.google_trends_interest import google_trends_interest
from analytics_au.defs.assets.google_trends_interest_by_state import google_trends_interest_by_state
from analytics_au.defs.assets.google_trends_related_queries import google_trends_related_queries
from analytics_au.defs.assets.job_market import job_market
from analytics_au.defs.assets.job_market_occupations import job_market_occupations
from analytics_au.defs.assets.qilt_graduate_outcomes import qilt_graduate_outcomes
from analytics_au.defs.assets.qilt_institution_scores import qilt_institution_scores
from analytics_au.defs.assets.qilt_student_experience import qilt_student_experience
from analytics_au.defs.assets.uac_applicants_by_age import uac_applicants_by_age
from analytics_au.defs.assets.uac_applicants_by_gender import uac_applicants_by_gender
from analytics_au.defs.assets.uac_early_bird_closing_count import uac_early_bird_closing_count
from analytics_au.defs.assets.uac_fos_by_app_type import uac_fos_by_app_type
from analytics_au.defs.assets.uac_fos_by_gender import uac_fos_by_gender

# Google Trends: expect refresh every 6 hours, allow up to 12h staleness
realtime_freshness_checks = dg.build_last_update_freshness_checks(
    assets=[google_trends],
    lower_bound_delta=timedelta(hours=12),
    deadline_cron="0 */6 * * *",
    timezone="Australia/Sydney",
)

# Google Trends interest: monthly refresh, allow up to 45 days staleness
monthly_trends_freshness_checks = dg.build_last_update_freshness_checks(
    assets=[google_trends_interest],
    lower_bound_delta=timedelta(days=45),
    deadline_cron="0 9 5 * *",
    timezone="Australia/Sydney",
)

# Google Trends interest by state: same monthly cadence
monthly_trends_by_state_freshness_checks = dg.build_last_update_freshness_checks(
    assets=[google_trends_interest_by_state],
    lower_bound_delta=timedelta(days=45),
    deadline_cron="0 9 5 * *",
    timezone="Australia/Sydney",
)

# Google Trends related queries: same monthly cadence
monthly_trends_related_queries_freshness_checks = dg.build_last_update_freshness_checks(
    assets=[google_trends_related_queries],
    lower_bound_delta=timedelta(days=45),
    deadline_cron="0 9 5 * *",
    timezone="Australia/Sydney",
)

# Job market (IVI): published monthly, expect by the 20th of each month
monthly_freshness_checks = dg.build_last_update_freshness_checks(
    assets=[job_market, job_market_occupations],
    lower_bound_delta=timedelta(days=45),
    deadline_cron="0 9 20 * *",
    timezone="Australia/Sydney",
)

# CRICOS courses: weekly refresh, allow up to 14 days staleness
weekly_freshness_checks = dg.build_last_update_freshness_checks(
    assets=[cricos_courses],
    lower_bound_delta=timedelta(days=14),
    deadline_cron="0 9 * * 2",
    timezone="Australia/Sydney",
)

# QILT data: published annually ~September, check 1 Oct
annual_qilt_freshness_checks = dg.build_last_update_freshness_checks(
    assets=[qilt_graduate_outcomes, qilt_student_experience, qilt_institution_scores],
    lower_bound_delta=timedelta(days=400),
    deadline_cron="0 9 1 10 *",
    timezone="Australia/Sydney",
    severity=dg.AssetCheckSeverity.WARN,
)

# UAC + ABS: published annually ~October, check 1 Nov
annual_uac_freshness_checks = dg.build_last_update_freshness_checks(
    assets=[
        uac_applicants_by_age,
        uac_applicants_by_gender,
        uac_fos_by_app_type,
        uac_fos_by_gender,
        uac_early_bird_closing_count,
        abs_population_by_lga,
        abs_lga_reference,
    ],
    lower_bound_delta=timedelta(days=400),
    deadline_cron="0 9 1 11 *",
    timezone="Australia/Sydney",
    severity=dg.AssetCheckSeverity.WARN,
)
