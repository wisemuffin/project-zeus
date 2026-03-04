---
title: Field Value Proposition
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-blue-100 text-blue-800">National</span>

Composite ranking of each field of study by opportunity gap, employment rate, and salary — a single "best bet" view for prioritising marketing spend. Data sourced from **Jobs and Skills Australia** (vacancy data), **QILT Graduate Outcomes Survey** (employment and salary), the **University Admissions Centre** (preference share), **QILT Employer Satisfaction Survey** (employer validation), and **WordStream** (ad cost benchmarks).

```sql top_field
select field_of_study, value_score, value_tier
from zeus.field_value_proposition
where value_rank = 1
```

```sql nobrainer_count
select count(*) as total
from zeus.field_value_proposition
where value_tier = 'No-brainer'
```

```sql tier_summary
select
    value_tier,
    count(*) as field_count
from zeus.field_value_proposition
group by value_tier
order by
    case value_tier
        when 'No-brainer' then 1
        when 'High potential' then 2
        when 'Proven outcomes' then 3
        when 'Challenging' then 4
    end
```

<BigValue
    data={top_field}
    value=field_of_study
    title="Top-Ranked Field"
    description="Highest composite value score"
/>
<BigValue
    data={nobrainer_count}
    value=total
    title="No-Brainer Fields"
    description="Positive gap + strong employment + above-median salary"
/>

## Value Tier Distribution

Fields are classified into four tiers based on opportunity gap, full-time employment rate, and median salary relative to the sector. **No-brainer** fields have positive opportunity gap AND 80%+ FT employment AND above-sector-median salary.

<BarChart
    data={tier_summary}
    x=value_tier
    y=field_count
    title="Fields by Value Tier"
    yAxisTitle="Number of Fields"
    sort=false
/>

## Value Score Ranking

The value score is the average of three percentile ranks: opportunity gap, FT employment rate, and median salary. Higher scores indicate fields that perform well across all three dimensions.

```sql value_chart
select
    field_of_study,
    value_score,
    value_tier
from zeus.field_value_proposition
order by value_rank
```

<BarChart
    data={value_chart}
    x=field_of_study
    y=value_score
    title="Composite Value Score by Field"
    yAxisTitle="Value Score (0-1)"
    sort=false
/>

## Full Ranking

```sql value_table
select * from zeus.field_value_proposition order by value_rank
```

<DataTable
    data={value_table}
    rowShading=true
    search=true
>
    <Column id=value_rank title="Rank" />
    <Column id=field_of_study title="Field of Study" />
    <Column id=value_tier title="Tier" />
    <Column id=value_score title="Value Score" fmt=num2 contentType=colorscale />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=ft_employment_rate title="FT Employ %" fmt=num1 />
    <Column id=median_salary title="Median Salary" fmt=usd0 />
    <Column id=vacancy_growth_12m title="Vacancy Growth (12m)" fmt=pct1 contentType=colorscale />
</DataTable>

## Employer Validation

Beyond student outcomes, employer satisfaction confirms graduate quality from the demand side. Data from the **QILT Employer Satisfaction Survey (ESS)** — a national survey of 4,000+ employers rating graduates on foundation skills, adaptive skills, collaborative skills, technical skills, and employability skills.

```sql ess_by_fos
select
    field_of_study,
    overall_employer_satisfaction,
    employer_sat_vs_sector
from zeus.employer_satisfaction_by_fos
order by overall_employer_satisfaction desc
```

```sql sector_avg_ess
select round(avg(overall_employer_satisfaction), 1) as sector_avg
from zeus.employer_satisfaction_by_fos
```

<BarChart
    data={ess_by_fos}
    x=field_of_study
    y=overall_employer_satisfaction
    title="Overall Employer Satisfaction by Field"
    yAxisTitle="Satisfaction (%)"
    swapXY=true
    sort=false
    yMin=75
    labels=true
    labelFmt=num1
/>

Fields above the sector average ({sector_avg_ess[0].sector_avg}%) have a stronger employer proof point. The `employer_sat_vs_sector` value shows percentage points above or below this average — positive values indicate fields where employers are especially satisfied with graduates.

## Cost-Adjusted Priorities

Combining value scores with estimated advertising costs reveals which "No-brainer" fields are also cheapest to target. Fields with high value scores *and* high gap-per-CPC-dollar are the strongest candidates for marketing investment.

```sql cost_adjusted
select
    v.value_rank,
    v.field_of_study,
    v.value_tier,
    r.roi_tier,
    v.value_score,
    r.gap_per_cpc_dollar,
    r.estimated_cpc_aud
from zeus.field_value_proposition v
left join zeus.field_roi_recommendation r on v.field_of_study = r.field_of_study
order by v.value_rank
```

<DataTable
    data={cost_adjusted}
    rowShading=true
    search=true
>
    <Column id=value_rank title="Value Rank" />
    <Column id=field_of_study title="Field of Study" />
    <Column id=value_tier title="Value Tier" />
    <Column id=roi_tier title="ROI Tier" />
    <Column id=value_score title="Value Score" fmt=num2 contentType=colorscale />
    <Column id=gap_per_cpc_dollar title="Gap / $1 CPC" fmt=num4 contentType=colorscale colorScale=positive />
    <Column id=estimated_cpc_aud title="Est. CPC (AUD)" fmt=usd2 />
</DataTable>

<Details title="Data Sources">

- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Monthly online job vacancy counts by occupation. Used for opportunity gap and vacancy growth calculations.
- **UAC Early Bird Applicant Preferences** — University Admissions Centre. Annual first-preference counts by field of study. NSW/ACT applicants only.
- **Graduate Outcomes Survey (GOS) 2024** — Quality Indicators for Learning and Teaching (QILT). Employment rates and median salaries by field of study. Undergraduate data only.
- **Value score** — average of three percentile ranks (opportunity gap, FT employment rate, median salary). Tier classification uses absolute thresholds: "No-brainer" requires positive gap, 80%+ FT employment, and salary at or above the sector median.
- **Employer Satisfaction Survey (ESS) 2024** — Quality Indicators for Learning and Teaching (QILT), Australian Government. National survey of 4,000+ employers rating graduates across five skill domains. 3-year pooled data (2022-2024). Mapped to UAC broad fields via a manual crosswalk.
- **WordStream Google Ads Benchmarks 2025** — WordStream (Localiq). Industry-level CPC, CPL, and CTR benchmarks for Google Search ads. US data adjusted with a 1.3× multiplier for Australian market. Education sector averages applied to all fields.

</Details>
