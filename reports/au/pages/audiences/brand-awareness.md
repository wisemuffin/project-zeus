---
title: Brand Awareness
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-emerald-100 text-emerald-800">State-level</span>

University brand awareness analysis combining **Google Trends** search interest (time series, geographic, and related queries) with **QILT** institution quality metrics. Identifies universities that are under-searched relative to their academic quality — prime candidates for marketing investment.

```sql uni_count
select count(*) as total from zeus.university_brand_awareness
```

```sql top_opportunity
select university, interest_quality_gap
from zeus.university_brand_awareness
where interest_quality_gap = (select max(interest_quality_gap) from zeus.university_brand_awareness)
```

```sql top_brand
select university, avg_interest_12m
from zeus.university_brand_awareness
where interest_rank = 1
```

<BigValue
    data={uni_count}
    value=total
    title="Universities Analysed"
/>
<BigValue
    data={top_opportunity}
    value=university
    title="Top Marketing Opportunity"
    description="Biggest interest-quality gap"
/>
<BigValue
    data={top_brand}
    value=university
    title="Top Brand"
    description="Highest search interest"
/>

## Interest Rank vs Quality Rank

Universities below the diagonal are under-searched relative to their quality ranking — the strongest marketing opportunities. Those above the diagonal already have strong brand recognition relative to quality.

```sql scatter_data
select
    university,
    interest_rank,
    quality_rank,
    awareness_tier,
    interest_quality_gap,
    avg_interest_12m,
    overall_quality,
    interest_trend
from zeus.university_brand_awareness
where interest_rank is not null and quality_rank is not null
```

<ScatterPlot
    data={scatter_data}
    x=interest_rank
    y=quality_rank
    tooltipTitle=university
    xAxisTitle="Interest Rank (1 = most searched)"
    yAxisTitle="Quality Rank (1 = highest quality)"
    title="Brand Awareness vs Academic Quality"
    pointSize=10
/>

## State Interest Map

Select a university to see its geographic search interest across Australian states. Higher values indicate stronger brand recognition in that state.

```sql uni_list
select distinct university from zeus.university_state_interest order by university
```

<Dropdown
    name=selected_university
    data={uni_list}
    value=university
    title="Select University"
/>

```sql state_map_data
select
    state_name,
    state,
    interest,
    state_rank_for_uni,
    uni_rank_in_state,
    interest_vs_uni_avg
from zeus.university_state_interest
where university = '${inputs.selected_university}'
```

<AreaMap
    data={state_map_data}
    geoJsonUrl={addBasePath('/au_state_2021_gen.geojson')}
    geoId="state_name_2021"
    areaCol="state_name"
    value="interest"
    height=500
    startingLat={-28}
    startingLong={134}
    startingZoom={4}
    legendType="scalar"
    title={`Search Interest by State — ${inputs.selected_university}`}
    tooltip={[{id: 'state_name', showColumnName: false, valueClass: 'font-bold text-sm'}, {id: 'interest', title: 'Interest', fmt: 'num1'}, {id: 'state_rank_for_uni', title: 'State Rank (for uni)'}, {id: 'uni_rank_in_state', title: 'Uni Rank (in state)'}, {id: 'interest_vs_uni_avg', title: 'vs Uni Avg', fmt: 'num1'}]}
/>

## Brand Awareness Table

The interest-quality gap highlights marketing opportunities: positive values indicate universities that are under-searched relative to their quality. Momentum shows recent 3-month trend direction.

```sql awareness_table
select
    university,
    interest_rank,
    avg_interest_12m,
    interest_momentum,
    interest_trend,
    quality_rank,
    overall_quality,
    interest_quality_gap,
    awareness_tier,
    top_state,
    ft_employment_rate,
    median_salary
from zeus.university_brand_awareness
order by interest_rank asc nulls last
```

<DataTable
    data={awareness_table}
    rowShading=true
    search=true
>
    <Column id=university title="University" />
    <Column id=interest_rank title="Interest Rank" />
    <Column id=avg_interest_12m title="Avg Interest (12m)" fmt=num1 />
    <Column id=interest_momentum title="Momentum" fmt=pct1 contentType=colorscale />
    <Column id=interest_trend title="Trend" />
    <Column id=quality_rank title="Quality Rank" />
    <Column id=overall_quality title="Overall Quality %" fmt=num1 />
    <Column id=interest_quality_gap title="Interest-Quality Gap" contentType=colorscale />
    <Column id=awareness_tier title="Awareness Tier" />
    <Column id=top_state title="Top State" />
    <Column id=ft_employment_rate title="FT Employment %" fmt=num1 />
    <Column id=median_salary title="Median Salary" fmt=usd0 />
</DataTable>

## Related Queries

What people search alongside university names — reveals brand associations and common search paths. Select a university to see its top and rising related queries.

```sql related_queries
select
    related_query,
    query_type,
    value
from zeus.stg_google_trends_related_queries
where university = '${inputs.selected_university}'
order by query_type, value desc
```

<DataTable
    data={related_queries}
    rowShading=true
    search=true
>
    <Column id=related_query title="Related Query" />
    <Column id=query_type title="Type" />
    <Column id=value title="Value" />
</DataTable>

<Details title="Data Sources">

- **Google Trends — Interest Over Time** — Google (trends.google.com). Monthly relative search interest (0-100) for 42 Australian university names over a rolling 5-year window. Cross-batch normalized using University of Melbourne as anchor. Acronym searches (QUT, UTS, UNSW, RMIT) may capture non-university intent. Relative index only — cannot compare to non-university terms.
- **Google Trends — Interest by State** — Google (trends.google.com). State-level relative search interest (0-100) for each university name. Single snapshot representing ~5-year aggregate geographic patterns. Small states (NT, ACT, TAS) may have noisy or zero signals.
- **Google Trends — Related Queries** — Google (trends.google.com). Top and rising queries associated with each university search term. Rising values show growth percentage or "Breakout" (>5000% growth). Ephemeral — may change between data refreshes.
- **QILT Institution Scorecard** — Quality Indicators for Learning and Teaching, Australian Government. Overall quality (% positive), full-time employment rate, and median graduate salary per university. 2024 release. University of Divinity may have insufficient respondents for some metrics.
- **State boundaries** — ABS ASGS 2021 STE generalised boundaries for choropleth map.

</Details>
