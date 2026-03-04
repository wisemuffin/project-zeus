---
title: Institution Scorecard
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-blue-100 text-blue-800">National</span>

Per-university benchmarks combining **student satisfaction** (QILT Student Experience Survey), **graduate employment outcomes** (QILT Graduate Outcomes Survey), and **employer satisfaction** (QILT Employer Satisfaction Survey). Use this to identify a university's strengths and weaknesses relative to the sector and its competitors.

```sql top_quality
select institution, overall_quality
from zeus.institution_scorecard
where quality_rank = 1
```

```sql top_employment
select institution, ft_employment_rate
from zeus.institution_scorecard
where employment_rank = 1
```

```sql top_salary
select institution, median_salary
from zeus.institution_scorecard
where salary_rank = 1
```

```sql uni_count
select count(*) as total from zeus.institution_scorecard
```

```sql top_employer_sat_inst
select institution, overall_employer_satisfaction
from zeus.institution_scorecard
where employer_sat_rank = 1
```

```sql vintage_qilt_ses
select source_label || ' ' || data_period as subtitle
from zeus.freshness_vintage where source_key = 'qilt_ses'
```

```sql vintage_qilt_gos
select source_label || ' ' || data_period as subtitle
from zeus.freshness_vintage where source_key = 'qilt_gos'
```

```sql vintage_qilt_ess
select source_label || ' ' || data_period as subtitle
from zeus.freshness_vintage where source_key = 'qilt_ess'
```

<BigValue
    data={uni_count}
    value=total
    title="Universities Benchmarked"
/>
<BigValue
    data={top_quality}
    value=institution
    title="Highest Overall Quality"
/>
<BigValue
    data={top_employment}
    value=institution
    title="Highest FT Employment"
/>
<BigValue
    data={top_salary}
    value=institution
    title="Highest Median Salary"
/>
<BigValue
    data={top_employer_sat_inst}
    value=institution
    title="Highest Employer Satisfaction"
    description={top_employer_sat_inst[0].overall_employer_satisfaction + '%'}
/>

## Overall Quality vs Employment

Universities in the top-right quadrant have both high student satisfaction and strong graduate employment — the ideal position for marketing. Those in other quadrants have clear strengths to lead with or gaps to address.

```sql scatter_data
select
    institution,
    overall_quality,
    ft_employment_rate,
    median_salary
from zeus.institution_scorecard
where overall_quality is not null and ft_employment_rate is not null
```

<ScatterPlot
    data={scatter_data}
    x=ft_employment_rate
    y=overall_quality
    tooltipTitle=institution
    xAxisTitle="Full-Time Employment Rate (%)"
    yAxisTitle="Overall Quality (% positive)"
    title="Student Satisfaction vs Graduate Employment"
    subtitle="Sources: {vintage_qilt_ses[0].subtitle}, {vintage_qilt_gos[0].subtitle}"
    pointSize=10
/>

## Student vs Employer Satisfaction

Do universities that students rate highly also produce graduates that employers value? This scatter plot reveals alignment — or gaps — between the two perspectives.

```sql student_vs_employer
select
    institution,
    overall_quality,
    overall_employer_satisfaction
from zeus.institution_scorecard
where overall_quality is not null and overall_employer_satisfaction is not null
```

<ScatterPlot
    data={student_vs_employer}
    x=overall_quality
    y=overall_employer_satisfaction
    tooltipTitle=institution
    xAxisTitle="Student Satisfaction — Overall Quality (%)"
    yAxisTitle="Employer Satisfaction (%)"
    title="Student Satisfaction vs Employer Satisfaction"
    subtitle="Sources: {vintage_qilt_ses[0].subtitle}, {vintage_qilt_ess[0].subtitle}"
    pointSize=10
/>

## Satisfaction Indicators

Six focus areas from the Student Experience Survey. Higher scores indicate a larger proportion of students rating the experience positively.

```sql satisfaction_chart
select
    institution,
    overall_quality,
    teaching_quality,
    skills_development,
    student_support,
    learning_resources,
    peer_engagement,
    quality_rank
from zeus.institution_scorecard
where overall_quality is not null
order by quality_rank
limit 20
```

<BarChart
    data={satisfaction_chart}
    x=institution
    y={['overall_quality', 'teaching_quality', 'skills_development']}
    title="Top 20 Universities — Key Satisfaction Indicators"
    subtitle={vintage_qilt_ses[0].subtitle}
    yAxisTitle="% Positive Rating"
    type=grouped
    sort=false
/>

## Full Scorecard

```sql scorecard_table
select * from zeus.institution_scorecard
```

<DataTable
    data={scorecard_table}
    rowShading=true
    search=true
    subtitle="Sources: {vintage_qilt_ses[0].subtitle}, {vintage_qilt_gos[0].subtitle}, {vintage_qilt_ess[0].subtitle}"
>
    <Column id=institution title="Institution" />
    <Column id=overall_quality title="Overall Quality %" fmt=num1 />
    <Column id=quality_rank title="Quality Rank" />
    <Column id=teaching_quality title="Teaching %" fmt=num1 />
    <Column id=skills_development title="Skills %" fmt=num1 />
    <Column id=student_support title="Support %" fmt=num1 />
    <Column id=learning_resources title="Resources %" fmt=num1 />
    <Column id=ft_employment_rate title="FT Employ %" fmt=num1 />
    <Column id=employment_rank title="Employ Rank" />
    <Column id=median_salary title="Median Salary" fmt=usd0 />
    <Column id=salary_rank title="Salary Rank" />
    <Column id=overall_employer_satisfaction title="Employer Sat %" fmt=num1 />
    <Column id=employer_sat_vs_sector title="Emp Sat vs Sector" fmt={'+0.0;-0.0'} contentType=colorscale />
    <Column id=employer_sat_rank title="Emp Sat Rank" />
    <Column id=quality_vs_sector title="Quality vs Sector" fmt=num1 contentType=colorscale />
    <Column id=employment_vs_sector title="Employ vs Sector" fmt=num1 contentType=colorscale />
    <Column id=salary_vs_sector title="Salary vs Sector" fmt=usd0 contentType=colorscale />
</DataTable>

```sql page_refreshed
select max(last_refreshed) as refreshed_at
from zeus.freshness_pipeline
where table_name in ('institution_scorecard')
```

<p style="color: #9ca3af; font-size: 0.75rem;">
Pipeline last refreshed: {fmt(page_refreshed[0].refreshed_at, 'd MMMM yyyy')}
</p>

<Details title="Data Sources">

- **Student Experience Survey (SES) 2024** — Quality Indicators for Learning and Teaching (QILT), Australian Government. Annual survey of 258,000+ students. Six satisfaction indicators (% positive rating) covering skills development, peer engagement, teaching quality, student support, learning resources, and overall educational experience. Undergraduate data from universities only.
- **Graduate Outcomes Survey (GOS) 2024** — QILT. Annual survey of 117,000+ graduates 4-6 months after completion. Full-time employment rate and median annual salary by institution. Undergraduate data from universities only.
- **Employer Satisfaction Survey (ESS) 2024** — QILT. National survey of 4,000+ employers rating graduates on five skill domains. 3-year pooled data (2022-2024). Institution-level scores are overall employer satisfaction (% rating graduates as well or very well prepared).
- **Sector averages** are simple means across all universities. Individual cells with fewer than 5 respondents are suppressed (null). University of Divinity typically has too few GOS respondents for employment/salary metrics.
- **Confidence intervals** from the original QILT data have been removed — only point estimates are shown. Original CIs are 90% Agresti-Coull intervals.

</Details>
