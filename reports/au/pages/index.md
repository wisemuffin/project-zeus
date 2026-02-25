---
title: University Marketing Opportunities
---

Market research insights to help universities optimise digital marketing campaigns for student acquisition. Data sourced from **Jobs and Skills Australia** (job vacancy statistics), the **University Admissions Centre** (UAC applicant preferences), and the **Australian Bureau of Statistics** (youth population estimates).

## Explore

- **[Audiences](/audiences)** — Who to target: profiles, brand awareness, segments, scorecards
- **[Demand](/demand)** — Where and what to target: vacancy demand, state preferences, trends
- **[Outcomes](/outcomes)** — What message to use: employment, salaries, satisfaction, field value
- **[Insights](/insights)** — Narrative analyses with marketing angles and targeting recommendations
- **[Research](/research)** — Competitor landscape, platform comparisons, market expansion
- **[Methodology](/methodology)** — Data source transparency and ingestion reference

```sql top_opportunity
select
    field_of_study,
    opportunity_gap,
    opportunity_rank
from zeus.opportunity_gap
where opportunity_rank = 1
```

```sql total_fields
select count(*) as total_fields from zeus.opportunity_gap
```

```sql top_growth
select
    field_of_study,
    vacancy_growth_12m
from zeus.opportunity_gap
where vacancy_growth_12m = (select max(vacancy_growth_12m) from zeus.opportunity_gap)
```

<BigValue
    data={top_opportunity}
    value=field_of_study
    title="Top Opportunity Field"
/>
<BigValue
    data={total_fields}
    value=total_fields
    title="Fields Analysed"
/>
<BigValue
    data={top_growth}
    value=field_of_study
    title="Fastest Growing Field"
    description="Highest 12-month vacancy growth"
/>

## Opportunity Gap by Field of Study

Fields where job vacancy share exceeds student preference share represent under-targeted marketing opportunities. A positive gap means employer demand outstrips student interest — an opportunity for universities to attract students with strong employment messaging. See the [Opportunity Gap insight](/insights/opportunity-gap) for detailed marketing angles and gender targeting implications.

```sql opp_gap_chart
select
    field_of_study,
    vacancy_share,
    preference_share,
    opportunity_gap
from zeus.opportunity_gap
order by opportunity_gap desc
```

<BarChart
    data={opp_gap_chart}
    x=field_of_study
    y={['vacancy_share', 'preference_share']}
    title="Vacancy Share vs Preference Share by Field"
    yAxisTitle="Share"
    yFmt=pct1
    type=grouped
    xAxisTitle="Field of Study"
    sort=false
/>

```sql opp_gap_table
select * from zeus.opportunity_gap order by opportunity_rank
```

<DataTable
    data={opp_gap_table}
    rows=all
    rowShading=true
    search=true
>
    <Column id=opportunity_rank title="Rank" />
    <Column id=field_of_study title="Field of Study" />
    <Column id=total_vacancies title="Total Vacancies" fmt=num0 />
    <Column id=vacancy_share title="Vacancy Share" fmt=pct1 />
    <Column id=preference_share title="Preference Share" fmt=pct1 />
    <Column id=opportunity_gap title="Opportunity Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=vacancy_growth_12m title="12m Vacancy Growth" fmt=pct1 contentType=colorscale />
</DataTable>

## Gender Targeting Insights

Understanding gender skew in field preferences helps universities tailor messaging and channel targeting. Fields skewed toward one gender present opportunities to broaden reach to the under-represented group.

```sql gender_chart
select
    field_of_study,
    female_preference_share,
    male_preference_share,
    skew_direction,
    opportunity_rank
from zeus.opportunity_gap_by_gender
order by opportunity_rank
```

<BarChart
    data={gender_chart}
    x=field_of_study
    y={['female_preference_share', 'male_preference_share']}
    title="Student Preferences by Gender"
    yAxisTitle="Preference Share"
    yFmt=pct1
    type=grouped
    sort=false
/>

```sql gender_table
select * from zeus.opportunity_gap_by_gender order by opportunity_rank
```

<DataTable
    data={gender_table}
    rows=all
    rowShading=true
    search=true
>
    <Column id=opportunity_rank title="Rank" />
    <Column id=field_of_study title="Field of Study" />
    <Column id=vacancy_share title="Vacancy Share" fmt=pct1 />
    <Column id=opportunity_gap title="Opportunity Gap" fmt=pct1 />
    <Column id=female_preference_share title="Female Pref Share" fmt=pct1 />
    <Column id=male_preference_share title="Male Pref Share" fmt=pct1 />
    <Column id=gender_skew title="Gender Skew" fmt=pct1 contentType=colorscale />
    <Column id=skew_direction title="Skew Direction" />
</DataTable>

## State-Level Demand

Graduate vacancy density per 1,000 youth population highlights which states have the strongest labour market pull for university graduates. This supports geographic targeting of digital campaigns. See the [State Demand Index insight](/insights/state-demand) for marketing angles by state.

```sql state_chart
select
    state,
    graduate_vacancies_per_1k_youth,
    total_vacancies_per_1k_youth,
    demand_rank
from zeus.state_demand_index
order by demand_rank
```

<BarChart
    data={state_chart}
    x=state
    y={['graduate_vacancies_per_1k_youth', 'total_vacancies_per_1k_youth']}
    title="Vacancies per 1,000 Youth by State"
    yAxisTitle="Vacancies per 1k Youth"
    type=grouped
    sort=false
/>

```sql state_table
select * from zeus.state_demand_index order by demand_rank
```

<DataTable
    data={state_table}
    rows=all
    rowShading=true
    search=true
>
    <Column id=demand_rank title="Rank" />
    <Column id=state title="State" />
    <Column id=graduate_vacancies title="Graduate Vacancies" fmt=num0 />
    <Column id=youth_population_15_19 title="Youth Pop (15-19)" fmt=num0 />
    <Column id=graduate_vacancies_per_1k_youth title="Grad Vacancies / 1k Youth" fmt=num1 />
    <Column id=graduate_share_of_vacancies title="Graduate Share" fmt=pct1 />
    <Column id=graduate_vacancy_growth_12m title="Grad Vacancy Growth (12m)" fmt=pct1 contentType=colorscale />
    <Column id=total_vacancy_growth_12m title="Total Vacancy Growth (12m)" fmt=pct1 contentType=colorscale />
</DataTable>

<Details title="Data Sources">

- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Monthly online job vacancy counts by occupation and state. National and state-level coverage.
- **UAC Early Bird Applicant Preferences** — University Admissions Centre. Annual first-preference counts by field of study, gender, applicant type, and geographic origin. NSW/ACT applicants only.
- **Estimated Resident Population** — Australian Bureau of Statistics (ABS). Annual population estimates by age and state. All states and territories.
- **Occupation-to-Field-of-Study mapping** — manually curated crosswalk linking ANZSCO occupation groups to broad fields of education. Coverage is approximate and may not capture all relevant occupations for each field.

</Details>
