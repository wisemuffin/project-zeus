---
title: State × Field of Study Demand
---

State-level job vacancy data crossed with fields of study to reveal **where to spend by state for specific programs**. Shows which fields are strongest in which states relative to the national average, using vacancy data from **Jobs and Skills Australia** and youth population estimates from the **Australian Bureau of Statistics**.

**More reports:** [Opportunity Gap Dashboard](/) | [Graduate Outcomes](/graduate-outcomes) | [Institution Scorecard](/institution-scorecard) | [Audience Profiles](/audience-profiles) | [Trending Interests](/trending-interests) | [Historical Demand](/historical-demand) | [State Preferences](/state-preferences) | [Course Listings](/course-listings)

```sql state_count
select count(distinct state) as total from zeus.state_fos_demand
```

```sql fos_count
select count(distinct field_of_study) as total from zeus.state_fos_demand
```

```sql combo_count
select count(*) as total from zeus.state_fos_demand
```

```sql top_specialisation
select state, field_of_study, state_vs_national_skew
from zeus.state_fos_demand
where state_vs_national_skew = (select max(state_vs_national_skew) from zeus.state_fos_demand)
```

<BigValue
    data={state_count}
    value=total
    title="States Covered"
/>
<BigValue
    data={fos_count}
    value=total
    title="Fields of Study"
/>
<BigValue
    data={combo_count}
    value=total
    title="State × Field Combinations"
/>
<BigValue
    data={top_specialisation}
    value=field_of_study
    title="Strongest Specialisation"
    description={top_specialisation[0].state}
/>

## Top Specialisation by State

Each state's most over-indexed field of study compared to the national average. A positive skew means the state has a larger share of vacancies in that field than the country overall — an opportunity for geo-targeted messaging.

```sql top_by_state
select
    state,
    field_of_study,
    state_vs_national_skew
from zeus.state_fos_demand
where state_specialisation_rank = 1
order by state_vs_national_skew desc
```

<BarChart
    data={top_by_state}
    x=state
    y=state_vs_national_skew
    title="Top Over-Indexed Field per State (Skew vs National)"
    yAxisTitle="State vs National Skew"
    yFmt=pct1
    sort=false
    labels=field_of_study
/>

## Top 3 Fields per State

The three most over-indexed fields in each state. Use this to identify which programs to emphasise in state-specific campaigns.

```sql top3_by_state
select
    state,
    field_of_study,
    state_vs_national_skew
from zeus.state_fos_demand
where state_specialisation_rank <= 3
order by state, state_specialisation_rank
```

<BarChart
    data={top3_by_state}
    x=state
    y=state_vs_national_skew
    series=field_of_study
    title="Top 3 Over-Indexed Fields per State"
    yAxisTitle="State vs National Skew"
    yFmt=pct1
    type=grouped
    sort=false
/>

## Vacancy Density — Top 3 Fields per State

Absolute demand measured as vacancies per 1,000 youth population. Higher density means more job opportunities relative to the local youth cohort.

```sql density_top3
select
    state,
    field_of_study,
    vacancies_per_1k_youth
from zeus.state_fos_demand
where state_specialisation_rank <= 3
order by state, state_specialisation_rank
```

<BarChart
    data={density_top3}
    x=state
    y=vacancies_per_1k_youth
    series=field_of_study
    title="Vacancies per 1,000 Youth — Top 3 Fields per State"
    yAxisTitle="Vacancies per 1k Youth"
    type=grouped
    sort=false
/>

## Opportunity Context

State skew (how much a state over-indexes on a field) vs the national opportunity gap (employer demand minus student interest). Points in the top-right are the best geo-targeted opportunities — fields that are both locally strong and nationally under-served by student interest.

```sql scatter
select
    state,
    field_of_study,
    state_vs_national_skew,
    national_opportunity_gap,
    vacancies_per_1k_youth,
    state || ' — ' || field_of_study as label
from zeus.state_fos_demand
where national_opportunity_gap is not null
```

<ScatterPlot
    data={scatter}
    x=state_vs_national_skew
    y=national_opportunity_gap
    size=vacancies_per_1k_youth
    tooltipTitle=label
    xAxisTitle="State vs National Skew"
    yAxisTitle="National Opportunity Gap"
    xFmt=pct1
    yFmt=pct1
    title="State Skew vs National Opportunity Gap"
    pointSize=8
/>

## Full Detail

```sql detail_table
select * from zeus.state_fos_demand order by state, state_specialisation_rank
```

<DataTable
    data={detail_table}
    rows=all
    rowShading=true
    search=true
>
    <Column id=state title="State" />
    <Column id=field_of_study title="Field of Study" />
    <Column id=state_specialisation_rank title="Spec. Rank" />
    <Column id=vacancies title="Vacancies" fmt=num0 />
    <Column id=fos_share_in_state title="FoS Share (State)" fmt=pct1 />
    <Column id=national_vacancy_share title="FoS Share (National)" fmt=pct1 />
    <Column id=state_vs_national_skew title="State Skew" fmt=pct1 contentType=colorscale />
    <Column id=vacancy_growth_12m title="Vacancy Growth (12m)" fmt=pct1 contentType=colorscale />
    <Column id=vacancies_per_1k_youth title="Vacancies / 1k Youth" fmt=num1 />
    <Column id=national_opportunity_gap title="National Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=national_opportunity_rank title="National Opp Rank" />
</DataTable>

<Details title="Data Sources">

- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Monthly online job vacancy counts by occupation and state. National and state-level coverage. Used to calculate field-of-study vacancy shares and growth rates per state.
- **Estimated Resident Population** — Australian Bureau of Statistics (ABS). Annual population estimates by age and state. Used for youth population (15-19) to calculate vacancy density.
- **Occupation-to-Field-of-Study mapping** — manually curated crosswalk linking ANZSCO occupation groups to broad fields of education. Coverage is approximate and may not capture all relevant occupations for each field.
- **Opportunity gap context** — derived from the Internet Vacancy Index and UAC preference data via the opportunity_gap mart. National-level gap and rank joined to each state × field row.

</Details>
