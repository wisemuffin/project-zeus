import dagster as dg


@dg.asset(
    group_name="uac_data",
    tags={"source": "uac", "domain": "preferences"},
)
def uac_preferences(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    """UAC application preference data.

    University Admissions Centre (UAC) data on course preferences submitted by
    prospective students. Provides insight into which courses and institutions
    are most popular among Year 12 applicants.
    """
    raise NotImplementedError("UAC preferences data source not yet implemented")
