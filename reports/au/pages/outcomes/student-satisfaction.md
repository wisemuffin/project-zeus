---
title: Student Satisfaction × Opportunity
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-blue-100 text-blue-800">National</span>

QILT Student Experience Survey satisfaction scores aggregated to field-of-study level, joined with opportunity gap and graduate outcomes. Adds "student experience" proof points for marketing creative. Data sourced from the **QILT Student Experience Survey (SES)**, **QILT Graduate Outcomes Survey (GOS)**, **Jobs and Skills Australia**, and the **University Admissions Centre**.

```sql top_satisfaction
select field_of_study, overall_quality
from zeus.satisfaction_opportunity
where overall_quality = (select max(overall_quality) from zeus.satisfaction_opportunity)
```

```sql above_sector_count
select count(*) as total
from zeus.satisfaction_opportunity
where quality_vs_sector > 0
```

```sql vintage_qilt_ses
select source_label || ' ' || data_period as subtitle
from zeus.freshness_vintage where source_key = 'qilt_ses'
```

```sql vintage_qilt_gos
select source_label || ' ' || data_period as subtitle
from zeus.freshness_vintage where source_key = 'qilt_gos'
```

```sql vintage_ivi
select source_label || ' ' || data_period as subtitle
from zeus.freshness_vintage where source_key = 'ivi'
```

```sql vintage_uac
select source_label || ' ' || data_period as subtitle
from zeus.freshness_vintage where source_key = 'uac'
```

<BigValue
    data={top_satisfaction}
    value=field_of_study
    title="Highest Overall Satisfaction"
/>
<BigValue
    data={top_satisfaction}
    value=overall_quality
    title="Top Satisfaction Score"
    description="% agreement on overall quality"
    fmt=num1
/>
<BigValue
    data={above_sector_count}
    value=total
    title="Fields Above Sector Average"
/>

## Satisfaction vs Employment

Fields with both high satisfaction and high employment offer the strongest combined proof points for marketing messaging.

```sql scatter_data
select
    field_of_study,
    overall_quality,
    ft_employment_rate,
    opportunity_gap
from zeus.satisfaction_opportunity
where ft_employment_rate is not null
```

<ScatterPlot
    data={scatter_data}
    x=overall_quality
    y=ft_employment_rate
    pointLabel=field_of_study
    title="Student Satisfaction vs FT Employment Rate"
    subtitle="Sources: {vintage_qilt_ses[0].subtitle}, {vintage_qilt_gos[0].subtitle}"
    xAxisTitle="Overall Quality (% Agreement)"
    yAxisTitle="FT Employment Rate (%)"
/>

## Satisfaction Indicators by Field

Six QILT satisfaction dimensions across fields, ordered by opportunity rank. Teaching quality and skills development are the most directly relevant for ad creative.

```sql indicators_chart
select
    field_of_study,
    teaching_quality,
    skills_development,
    student_support,
    learning_resources,
    peer_engagement,
    overall_quality,
    opportunity_rank
from zeus.satisfaction_opportunity
order by opportunity_rank nulls last
```

<BarChart
    data={indicators_chart}
    x=field_of_study
    y={['teaching_quality', 'skills_development', 'student_support', 'learning_resources', 'peer_engagement']}
    title="Satisfaction Indicators by Field"
    subtitle={vintage_qilt_ses[0].subtitle}
    yAxisTitle="% Agreement"
    type=grouped
    sort=false
/>

## Full Data

```sql satisfaction_table
select * from zeus.satisfaction_opportunity order by opportunity_rank nulls last
```

<DataTable
    data={satisfaction_table}
    rowShading=true
    search=true
    subtitle="Sources: {vintage_qilt_ses[0].subtitle}, {vintage_ivi[0].subtitle}, {vintage_uac[0].subtitle}"
>
    <Column id=field_of_study title="Field of Study" />
    <Column id=overall_quality title="Overall Quality" fmt=num1 contentType=colorscale />
    <Column id=quality_vs_sector title="vs Sector" fmt=num1 contentType=colorscale colorScale=positive />
    <Column id=teaching_quality title="Teaching" fmt=num1 />
    <Column id=skills_development title="Skills" fmt=num1 />
    <Column id=student_support title="Support" fmt=num1 />
    <Column id=learning_resources title="Resources" fmt=num1 />
    <Column id=peer_engagement title="Peers" fmt=num1 />
    <Column id=ft_employment_rate title="FT Employ %" fmt=num1 />
    <Column id=median_salary title="Median Salary" fmt=usd0 />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
</DataTable>

```sql page_refreshed
select max(last_refreshed) as refreshed_at
from zeus.freshness_pipeline
where table_name in ('satisfaction_opportunity')
```

<p style="color: #9ca3af; font-size: 0.75rem;">
Pipeline last refreshed: {fmt(page_refreshed[0].refreshed_at, 'd MMMM yyyy')}
</p>

<Details title="Data Sources">

- **Student Experience Survey (SES) 2024** — Quality Indicators for Learning and Teaching (QILT), Australian Government. Annual survey of ~300,000 current students measuring teaching quality, skills development, student support, learning resources, peer engagement, and overall quality. Scores are % agreement. Undergraduate data only.
- **Graduate Outcomes Survey (GOS) 2024** — QILT. Employment rates and median salaries by field.
- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Used for opportunity gap calculation.
- **UAC Early Bird Applicant Preferences** — University Admissions Centre. NSW/ACT applicants only.
- **QILT study areas mapped to UAC fields** — Multiple QILT study areas are averaged (unweighted) into UAC broad fields. Some fields aggregate many study areas (e.g. Health includes 6 QILT areas).

</Details>
