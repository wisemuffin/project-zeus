---
title: Segment Playbooks
---

Per-applicant-type field affinity with employment outcomes context — shows which applicant segments over-index on which fields. Data sourced from the **University Admissions Centre** (applicant preferences by type), **QILT Graduate Outcomes Survey** (employment and salary), and **Jobs and Skills Australia** (vacancy demand).

```sql segments
select distinct applicant_type from zeus.segment_field_affinity order by applicant_type
```

```sql segment_data
select * from zeus.segment_field_affinity order by applicant_type, segment_rank
```

```sql top_affinity
select applicant_type, field_of_study, segment_affinity_index
from zeus.segment_field_affinity
where segment_affinity_index = (select max(segment_affinity_index) from zeus.segment_field_affinity)
```

```sql segment_count
select count(distinct applicant_type) as total from zeus.segment_field_affinity
```

<BigValue
    data={segment_count}
    value=total
    title="Applicant Segments"
/>
<BigValue
    data={top_affinity}
    value=field_of_study
    title="Strongest Over-Index"
    description="Highest affinity index across all segments"
/>
<BigValue
    data={top_affinity}
    value=segment_affinity_index
    title="Affinity Index"
    fmt=num2
/>

## Preference Share by Segment

Select a segment to see which fields its applicants prefer most. An affinity index above 1.0 means the segment over-indexes on that field relative to the total applicant pool.

<Dropdown name=segment_filter data={segments} value=applicant_type title="Applicant Segment" />

```sql filtered_data
select *
from zeus.segment_field_affinity
where applicant_type = '${inputs.segment_filter.value}'
order by segment_rank
```

<BarChart
    data={filtered_data}
    x=field_of_study
    y=preference_share
    title="Preference Share: {inputs.segment_filter.value}"
    yAxisTitle="Preference Share"
    yFmt=pct1
    sort=false
/>

## Segment Detail

<DataTable
    data={filtered_data}
    rows=all
    rowShading=true
    search=true
>
    <Column id=segment_rank title="Rank" />
    <Column id=field_of_study title="Field of Study" />
    <Column id=preference_share title="Segment Pref" fmt=pct1 />
    <Column id=segment_affinity_index title="Affinity Index" fmt=num2 contentType=colorscale />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=ft_employment_rate title="FT Employ %" fmt=num1 />
    <Column id=median_salary title="Median Salary" fmt=usd0 />
    <Column id=vacancy_growth_12m title="Vacancy Growth (12m)" fmt=pct1 contentType=colorscale />
</DataTable>

## All Segments Comparison

```sql all_segments
select * from zeus.segment_field_affinity order by applicant_type, segment_rank
```

<DataTable
    data={all_segments}
    rows=all
    rowShading=true
    search=true
>
    <Column id=applicant_type title="Segment" />
    <Column id=field_of_study title="Field of Study" />
    <Column id=segment_rank title="Rank" />
    <Column id=preference_share title="Pref Share" fmt=pct1 />
    <Column id=segment_affinity_index title="Affinity" fmt=num2 contentType=colorscale />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=ft_employment_rate title="FT Employ %" fmt=num1 />
    <Column id=median_salary title="Salary" fmt=usd0 />
</DataTable>

<Details title="Data Sources">

- **UAC Early Bird Applicants by Applicant Type** — University Admissions Centre. Annual first-preference counts segmented by applicant type (NSW Year 12, ACT Year 12, Interstate & IB, Non-Year 12) and field of study. NSW/ACT applicants only.
- **Graduate Outcomes Survey (GOS) 2024** — QILT. Employment rates and median salaries by field.
- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Used for opportunity gap calculation.
- **Affinity index** — segment preference share divided by total preference share. Values above 1.0 indicate the segment over-indexes on that field relative to the overall applicant pool.

</Details>
