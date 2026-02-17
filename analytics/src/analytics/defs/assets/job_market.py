import dagster as dg


@dg.asset(
    group_name="job_market",
    tags={"source": "job_market", "domain": "employment"},
)
def job_market(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    """Job market demand data from Seek and government skills datasets.

    Tracks in-demand occupations and skills to understand which career
    pathways and corresponding university courses align with labour market needs.
    """
    raise NotImplementedError("Job market data source not yet implemented")
