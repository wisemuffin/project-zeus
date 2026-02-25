---
title: Graduate Outcomes by Field of Study
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-blue-100 text-blue-800">National</span>

Career outcome proof points for ad creative — employment rates, salaries, and gender pay gaps from the **QILT Graduate Outcomes Survey (GOS)**, joined with opportunity gap and preference data from **Jobs and Skills Australia** and the **University Admissions Centre**.

```sql top_salary
select field_of_study, median_salary
from zeus.graduate_outcomes_by_fos
where median_salary = (select max(median_salary) from zeus.graduate_outcomes_by_fos)
```

```sql top_employment
select field_of_study, ft_employment_rate
from zeus.graduate_outcomes_by_fos
where ft_employment_rate = (select max(ft_employment_rate) from zeus.graduate_outcomes_by_fos)
```

```sql strong_signal_count
select count(*) as total
from zeus.graduate_outcomes_by_fos
where marketing_signal like 'Strong%'
```

<BigValue
    data={top_salary}
    value=field_of_study
    title="Highest Median Salary"
    fmt=usd0
/>
<BigValue
    data={top_employment}
    value=field_of_study
    title="Highest FT Employment"
/>
<BigValue
    data={strong_signal_count}
    value=total
    title="Strong Signal Fields"
    description="High demand + strong outcomes"
/>

## Median Salary by Field

Graduate salary is the most compelling data point for ad creative. Fields are ordered by opportunity rank — the top-ranked fields have the strongest gap between employer demand and student interest.

```sql salary_chart
select
    field_of_study,
    median_salary,
    median_salary_male,
    median_salary_female,
    opportunity_rank
from zeus.graduate_outcomes_by_fos
order by opportunity_rank nulls last
```

<BarChart
    data={salary_chart}
    x=field_of_study
    y={['median_salary_male', 'median_salary_female']}
    title="Median Graduate Salary by Gender"
    yAxisTitle="Median Annual Salary ($)"
    yFmt=usd0
    type=grouped
    sort=false
/>

## Full-Time Employment Rate

Percentage of graduates in full-time employment 4-6 months after completing their degree. Higher rates support stronger career-outcome messaging.

```sql employment_chart
select
    field_of_study,
    ft_employment_rate,
    ft_employment_rate_prior,
    opportunity_rank
from zeus.graduate_outcomes_by_fos
order by opportunity_rank nulls last
```

<BarChart
    data={employment_chart}
    x=field_of_study
    y={['ft_employment_rate', 'ft_employment_rate_prior']}
    title="Full-Time Employment Rate: 2024 vs 2023"
    yAxisTitle="FT Employment (%)"
    type=grouped
    sort=false
/>

## Marketing Signal Matrix

Each field is classified by combining opportunity gap (employer demand vs student interest) with graduate employment outcomes. **Strong** fields have both high demand and strong outcomes — the best candidates for career-outcome messaging.

```sql signal_table
select * from zeus.graduate_outcomes_by_fos order by opportunity_rank nulls last
```

<DataTable
    data={signal_table}
    rows=all
    rowShading=true
    search=true
>
    <Column id=field_of_study title="Field of Study" />
    <Column id=marketing_signal title="Signal" />
    <Column id=ft_employment_rate title="FT Employ %" fmt=num1 />
    <Column id=median_salary title="Median Salary" fmt=usd0 />
    <Column id=salary_growth_pct title="Salary Growth" fmt=pct1 contentType=colorscale />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=vacancy_growth_12m title="Vacancy Growth (12m)" fmt=pct1 contentType=colorscale />
    <Column id=female_preference_share title="Female Pref" fmt=pct1 />
    <Column id=male_preference_share title="Male Pref" fmt=pct1 />
    <Column id=salary_gender_gap title="Gender Salary Gap" fmt=usd0 contentType=colorscale />
</DataTable>

## Salary Gender Gap

Difference between male and female median graduate salaries. Positive values indicate males earn more. Fields with small or negative gaps support equity-focused messaging.

```sql gender_gap_chart
select
    field_of_study,
    salary_gender_gap,
    opportunity_rank
from zeus.graduate_outcomes_by_fos
where salary_gender_gap is not null
order by salary_gender_gap desc
```

<BarChart
    data={gender_gap_chart}
    x=field_of_study
    y=salary_gender_gap
    title="Salary Gender Gap (Male − Female)"
    yAxisTitle="Salary Gap ($)"
    yFmt=usd0
    sort=false
/>

<Details title="Data Sources">

- **Graduate Outcomes Survey (GOS) 2024** — Quality Indicators for Learning and Teaching (QILT), Australian Government. Annual survey of 117,000+ graduates 4-6 months after completion. Covers employment rates, median salaries by field of study and gender. Undergraduate data only.
- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Monthly online job vacancy counts by occupation and state. Used for opportunity gap calculation.
- **UAC Early Bird Applicant Preferences** — University Admissions Centre. Annual first-preference counts by field of study and gender. NSW/ACT applicants only. Used for preference share and gender preference data.
- **QILT study areas mapped to UAC fields** — Multiple QILT study areas (e.g. Dentistry, Medicine, Nursing, Pharmacy, Rehabilitation, Health services) are averaged into single UAC broad fields (e.g. Health). This is an unweighted average as QILT does not publish respondent counts per study area in the report tables.

</Details>
