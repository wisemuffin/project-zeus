---
title: Emerging Occupations
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-blue-100 text-blue-800">National</span>

ANZSCO2 occupation groups ranked by 12-month vacancy growth, mapped to UAC fields of study. Identifies fast-growing occupations where student preference hasn't caught up with employer demand. Data sourced from **Jobs and Skills Australia** (Internet Vacancy Index) and the **University Admissions Centre** (preference share).

```sql fastest_growing
select occupation_title, vacancy_growth_12m, uac_field_of_study
from zeus.emerging_occupations
where growth_rank = 1
```

```sql growing_count
select count(*) as total
from zeus.emerging_occupations
where vacancy_growth_12m > 0
```

```sql total_occupations
select count(*) as total from zeus.emerging_occupations
```

<BigValue
    data={fastest_growing}
    value=occupation_title
    title="Fastest Growing Occupation"
/>
<BigValue
    data={fastest_growing}
    value=vacancy_growth_12m
    title="12-Month Growth Rate"
    fmt=pct1
/>
<BigValue
    data={growing_count}
    value=total
    title="Growing Occupations"
    description="Positive 12-month vacancy growth"
/>

## Vacancy Growth by Occupation

12-month growth rate of job vacancies for each ANZSCO2 occupation group. Occupations with strong growth but flat student preference present the clearest messaging opportunities.

```sql growth_chart
select
    occupation_title,
    vacancy_growth_12m,
    uac_field_of_study
from zeus.emerging_occupations
order by growth_rank
```

<BarChart
    data={growth_chart}
    x=occupation_title
    y=vacancy_growth_12m
    title="12-Month Vacancy Growth by Occupation"
    yAxisTitle="Growth Rate"
    yFmt=pct1
    sort=false
/>

## Full Data

```sql occupations_table
select * from zeus.emerging_occupations order by growth_rank
```

<DataTable
    data={occupations_table}

    rowShading=true
    search=true
>
    <Column id=growth_rank title="Rank" />
    <Column id=occupation_title title="Occupation" />
    <Column id=uac_field_of_study title="Field of Study" />
    <Column id=vacancies title="Current Vacancies" fmt=num0 />
    <Column id=vacancies_12m_ago title="Vacancies 12m Ago" fmt=num0 />
    <Column id=vacancy_growth_12m title="Growth (12m)" fmt=pct1 contentType=colorscale />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=preference_share title="Pref Share" fmt=pct1 />
</DataTable>

<Details title="Data Sources">

- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Monthly online job vacancy counts by ANZSCO2 occupation group. National scope (AUST). Growth calculated as (current − 12m prior) / 12m prior.
- **UAC Early Bird Applicant Preferences** — University Admissions Centre. Preference share by field. NSW/ACT applicants only.
- **Occupation-to-Field-of-Study mapping** — manually curated crosswalk linking ANZSCO2 occupation groups to UAC broad fields of education. Not all occupations map cleanly to a single field.

</Details>
