---
title: Institution Scorecard
---

Per-university benchmarks combining **student satisfaction** (QILT Student Experience Survey) with **graduate employment outcomes** (QILT Graduate Outcomes Survey). Use this to identify a university's strengths and weaknesses relative to the sector and its competitors.

**More reports:** [Opportunity Gap Dashboard](/) | [Graduate Outcomes](/graduate-outcomes) | [Audience Profiles](/audience-profiles) | [Trending Interests](/trending-interests) | [Historical Demand](/historical-demand)

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
    rows=all
    rowShading=true
    search=true
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
    <Column id=quality_vs_sector title="Quality vs Sector" fmt=num1 contentType=colorscale />
    <Column id=employment_vs_sector title="Employ vs Sector" fmt=num1 contentType=colorscale />
    <Column id=salary_vs_sector title="Salary vs Sector" fmt=usd0 contentType=colorscale />
</DataTable>

<Details title="Data Sources">

- **Student Experience Survey (SES) 2024** — Quality Indicators for Learning and Teaching (QILT), Australian Government. Annual survey of 258,000+ students. Six satisfaction indicators (% positive rating) covering skills development, peer engagement, teaching quality, student support, learning resources, and overall educational experience. Undergraduate data from universities only.
- **Graduate Outcomes Survey (GOS) 2024** — QILT. Annual survey of 117,000+ graduates 4-6 months after completion. Full-time employment rate and median annual salary by institution. Undergraduate data from universities only.
- **Sector averages** are simple means across all universities. Individual cells with fewer than 5 respondents are suppressed (null). University of Divinity typically has too few GOS respondents for employment/salary metrics.
- **Confidence intervals** from the original QILT data have been removed — only point estimates are shown. Original CIs are 90% Agresti-Coull intervals.

</Details>
