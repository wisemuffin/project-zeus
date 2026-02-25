---
title: Historical Demand Trends
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-amber-100 text-amber-800">NSW/ACT</span>

10-year **University Admissions Centre (UAC)** applicant volumes by segment. Tracks year-over-year growth, compound annual growth rate (CAGR), and recovery from peak volumes. Use this to allocate marketing budget toward growing segments and identify declining ones that need repositioning. See the [Historical Demand Trends insight](/insights/historical-demand-trends) for segment-level marketing angles and budget implications.

```sql trends
select * from zeus.historical_demand_trends order by latest_count desc
```

```sql growing
select count(*) as total from zeus.historical_demand_trends where trend_direction = 'Growing'
```

```sql declining
select count(*) as total from zeus.historical_demand_trends where trend_direction = 'Declining'
```

```sql fastest_growing
select applicant_type, latest_yoy_growth
from zeus.historical_demand_trends
where latest_yoy_growth = (select max(latest_yoy_growth) from zeus.historical_demand_trends)
```

<BigValue
    data={growing}
    value=total
    title="Growing Segments"
/>
<BigValue
    data={declining}
    value=total
    title="Declining Segments"
/>
<BigValue
    data={fastest_growing}
    value=applicant_type
    title="Fastest Growing Segment"
    description="Highest YoY growth"
/>

## Latest Year-over-Year Growth

How each applicant segment changed in the most recent intake cycle.

```sql yoy_chart
select
    applicant_type,
    latest_yoy_growth,
    trend_direction
from zeus.historical_demand_trends
order by latest_yoy_growth desc
```

<BarChart
    data={yoy_chart}
    x=applicant_type
    y=latest_yoy_growth
    title="Year-over-Year Growth by Segment"
    yAxisTitle="YoY Growth"
    yFmt=pct1
    sort=false
/>

## Recovery from Peak

How close each segment is to its historical peak applicant count. A recovery ratio of 1.0 means the segment is at or above its all-time high.

```sql recovery_chart
select
    applicant_type,
    recovery_ratio,
    peak_intake,
    latest_count,
    peak_count
from zeus.historical_demand_trends
order by recovery_ratio desc
```

<BarChart
    data={recovery_chart}
    x=applicant_type
    y=recovery_ratio
    title="Recovery Ratio (Current vs Peak)"
    yAxisTitle="Recovery Ratio"
    yFmt=num2
    sort=false
/>

## Long-Term Growth (CAGR)

Compound annual growth rate over the full 10-year window. Positive CAGR indicates sustained structural growth; negative signals a long-term declining segment.

```sql cagr_chart
select
    applicant_type,
    cagr,
    trend_direction
from zeus.historical_demand_trends
order by cagr desc
```

<BarChart
    data={cagr_chart}
    x=applicant_type
    y=cagr
    title="10-Year Compound Annual Growth Rate"
    yAxisTitle="CAGR"
    yFmt=pct2
    sort=false
/>

## Full Detail

```sql detail_table
select * from zeus.historical_demand_trends order by latest_count desc
```

<DataTable
    data={detail_table}
    rowShading=true
    search=true
>
    <Column id=applicant_type title="Segment" />
    <Column id=latest_intake title="Latest Intake" />
    <Column id=latest_count title="Latest Count" fmt=num0 />
    <Column id=latest_yoy_growth title="YoY Growth" fmt=pct1 contentType=colorscale />
    <Column id=peak_count title="Peak Count" fmt=num0 />
    <Column id=peak_intake title="Peak Intake" />
    <Column id=recovery_ratio title="Recovery Ratio" fmt=num2 />
    <Column id=cagr title="CAGR" fmt=pct2 contentType=colorscale />
    <Column id=trend_direction title="Trend" />
</DataTable>

<Details title="Data Sources">

- **UAC Early Bird Closing Count** — University Admissions Centre. Annual applicant counts by segment, covering intake years 2016-17 to 2025-26. NSW/ACT applicants only.
- **Note:** early bird figures are point-in-time snapshots taken at the early bird closing date, not final application numbers. Actual enrolments may differ.

</Details>
