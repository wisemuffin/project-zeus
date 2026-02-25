---
title: Gender Pay Gap × Opportunity
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-blue-100 text-blue-800">National</span>

Gender salary gap alongside female/male preference shares and opportunity gap — a diversity-marketing view. Data sourced from **QILT Graduate Outcomes Survey** (salary by gender), the **University Admissions Centre** (gender preferences), and **Jobs and Skills Australia** (vacancy demand).

```sql top_gap
select field_of_study, salary_gender_gap
from zeus.gender_opportunity_profile
where salary_gender_gap = (select max(salary_gender_gap) from zeus.gender_opportunity_profile)
```

```sql diversity_opp_count
select count(*) as total
from zeus.gender_opportunity_profile
where diversity_opportunity = 'High diversity opportunity'
```

```sql smallest_gap
select field_of_study, salary_gender_gap
from zeus.gender_opportunity_profile
where salary_gender_gap is not null
order by abs(salary_gender_gap)
limit 1
```

<BigValue
    data={top_gap}
    value=field_of_study
    title="Largest Gender Salary Gap"
/>
<BigValue
    data={diversity_opp_count}
    value=total
    title="High Diversity Opportunity Fields"
    description="Positive opp gap + women underrepresented"
/>
<BigValue
    data={smallest_gap}
    value=field_of_study
    title="Most Equitable Field"
    description="Smallest absolute gender pay gap"
/>

## Median Salary by Gender

Side-by-side comparison of male and female median graduate salaries. Fields with large gaps and high opportunity present messaging opportunities around transparency and equity.

```sql salary_by_gender
select
    field_of_study,
    median_salary_female,
    median_salary_male,
    opportunity_rank
from zeus.gender_opportunity_profile
order by opportunity_rank nulls last
```

<BarChart
    data={salary_by_gender}
    x=field_of_study
    y={['median_salary_male', 'median_salary_female']}
    title="Median Graduate Salary by Gender"
    yAxisTitle="Median Annual Salary ($)"
    yFmt=usd0
    type=grouped
    sort=false
/>

## Gender Salary Gap ($)

Absolute difference between male and female median salaries. Positive values indicate males earn more. Fields with high demand and large gaps present opportunities for equity-focused messaging to attract women.

```sql gap_chart
select
    field_of_study,
    salary_gender_gap
from zeus.gender_opportunity_profile
where salary_gender_gap is not null
order by salary_gender_gap desc
```

<BarChart
    data={gap_chart}
    x=field_of_study
    y=salary_gender_gap
    title="Salary Gender Gap (Male − Female)"
    yAxisTitle="Salary Gap ($)"
    yFmt=usd0
    sort=false
/>

## Diversity Opportunity Classification

```sql diversity_table
select * from zeus.gender_opportunity_profile order by opportunity_rank nulls last
```

<DataTable
    data={diversity_table}
    rows=all
    rowShading=true
    search=true
>
    <Column id=field_of_study title="Field of Study" />
    <Column id=diversity_opportunity title="Classification" />
    <Column id=salary_gender_gap title="Gender Gap ($)" fmt=usd0 contentType=colorscale />
    <Column id=gender_gap_pct title="Gap %" fmt=pct1 />
    <Column id=female_preference_share title="Female Pref" fmt=pct1 />
    <Column id=male_preference_share title="Male Pref" fmt=pct1 />
    <Column id=female_underrepresentation title="Female Under-rep" fmt=pct1 contentType=colorscale />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=ft_employment_rate title="FT Employ %" fmt=num1 />
</DataTable>

<Details title="Data Sources">

- **Graduate Outcomes Survey (GOS) 2024** — QILT, Australian Government. Median salaries by gender and field of study. Undergraduate data only. Multiple QILT study areas averaged into UAC broad fields.
- **UAC Early Bird Applicant Preferences** — University Admissions Centre. Gender preference shares by field. NSW/ACT applicants only.
- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Used for opportunity gap calculation.
- **Female underrepresentation** — calculated as 0.5 minus female preference share. Positive values mean women are underrepresented in that field's applicant pool.
- **Diversity opportunity classification** — "High diversity opportunity" requires both a positive opportunity gap and women underrepresented by more than 10 percentage points.

</Details>
