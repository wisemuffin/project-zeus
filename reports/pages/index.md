---
title: University Marketing Opportunities
---

Market research insights to help universities optimise digital marketing campaigns for student acquisition. Data sourced from Australian Government job vacancy statistics, UAC application preferences, and ABS youth population estimates.

**More reports:** [Audience Profiles](/audience-profiles) | [Trending Interests](/trending-interests) | [Historical Demand](/historical-demand)

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

Fields where job vacancy share exceeds student preference share represent under-targeted marketing opportunities. A positive gap means employer demand outstrips student interest — an opportunity for universities to attract students with strong employment messaging.

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

Graduate vacancy density per 1,000 youth population highlights which states have the strongest labour market pull for university graduates. This supports geographic targeting of digital campaigns.

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
