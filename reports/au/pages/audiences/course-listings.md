---
title: University Course Listings
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-emerald-100 text-emerald-800">State-level</span>

Program-level view of **which institutions offer courses in high-demand fields**, enriched with opportunity gap and graduate outcome data from the **CRICOS Register**, **Jobs and Skills Australia**, and **QILT Graduate Outcomes Survey**. Use this to identify partner institutions and craft program-specific messaging.

```sql total_courses
select count(*) as total from zeus.university_course_listings
```

```sql total_institutions
select count(distinct institution_name) as total from zeus.university_course_listings
```

```sql total_fields
select count(distinct uac_field_of_study) as total from zeus.university_course_listings where uac_field_of_study is not null
```

```sql strong_signal
select count(*) as total from zeus.university_course_listings where marketing_signal like 'Strong%'
```

<BigValue
    data={total_courses}
    value=total
    title="Total Courses"
    fmt=num0
/>
<BigValue
    data={total_institutions}
    value=total
    title="Institutions"
/>
<BigValue
    data={total_fields}
    value=total
    title="Fields Covered"
/>
<BigValue
    data={strong_signal}
    value=total
    title="Strong Signal Courses"
    description="High demand + strong outcomes"
    fmt=num0
/>

## Courses by Field and Marketing Signal

Distribution of CRICOS courses across fields of study, coloured by marketing signal. **Strong** = high demand and strong graduate outcomes; **Demand** = high demand, moderate outcomes; **Outcomes** = saturated but graduates do well; **Challenging** = low demand, weaker outcomes.

```sql field_signal
select
    uac_field_of_study,
    marketing_signal,
    count(*) as course_count
from zeus.university_course_listings
where uac_field_of_study is not null
group by uac_field_of_study, marketing_signal
order by course_count desc
```

<BarChart
    data={field_signal}
    x=uac_field_of_study
    y=course_count
    series=marketing_signal
    title="Courses by Field of Study and Marketing Signal"
    xAxisTitle="Field of Study"
    yAxisTitle="Number of Courses"
    type=stacked
    sort=false
/>

## Courses by State

Geographic distribution of CRICOS-registered courses across Australian states and territories.

```sql state_dist
select
    location_state,
    count(*) as course_count
from zeus.university_course_listings
where location_state is not null
group by location_state
order by course_count desc
```

<BarChart
    data={state_dist}
    x=location_state
    y=course_count
    title="Course Count by State"
    xAxisTitle="State"
    yAxisTitle="Number of Courses"
    sort=false
/>

## Top 20 Institutions in High-Opportunity Fields

Institutions with the most courses in fields that have a positive opportunity gap (employer demand exceeds student interest).

```sql top_institutions
select
    institution_name,
    count(*) as high_opp_courses
from zeus.university_course_listings
where opportunity_gap > 0
group by institution_name
order by high_opp_courses desc
limit 20
```

<BarChart
    data={top_institutions}
    x=institution_name
    y=high_opp_courses
    title="Top 20 Institutions — Courses in High-Opportunity Fields"
    xAxisTitle="Institution"
    yAxisTitle="Courses with Positive Opp Gap"
    sort=false
/>

## Institution Summary

Per-institution aggregates filtered to institutions with 5 or more courses. Use this to compare institutional breadth, outcome strength, and alignment with high-demand fields.

```sql institution_summary
select
    institution_name,
    count(*) as total_courses,
    count(*) filter (where marketing_signal like 'Strong%') as strong_signal_courses,
    count(*) filter (where opportunity_gap > 0) as high_opp_courses,
    avg(ft_employment_rate) as avg_ft_employment,
    avg(median_salary) as avg_median_salary
from zeus.university_course_listings
where uac_field_of_study is not null
group by institution_name
having count(*) >= 5
order by total_courses desc
```

<DataTable
    data={institution_summary}
    rows=all
    rowShading=true
    search=true
>
    <Column id=institution_name title="Institution" />
    <Column id=total_courses title="Total Courses" fmt=num0 />
    <Column id=strong_signal_courses title="Strong Signal" fmt=num0 />
    <Column id=high_opp_courses title="High Opp Gap" fmt=num0 />
    <Column id=avg_ft_employment title="Avg FT Employ %" fmt=num1 />
    <Column id=avg_median_salary title="Avg Median Salary" fmt=usd0 />
</DataTable>

## Course Detail

Searchable row-level detail for all CRICOS-registered courses with marketing context.

```sql course_detail
select
    institution_name,
    course_name,
    course_level,
    uac_field_of_study,
    location_state,
    location_city,
    marketing_signal,
    opportunity_gap,
    vacancy_growth_12m,
    ft_employment_rate,
    median_salary,
    estimated_total_cost,
    course_count_in_field
from zeus.university_course_listings
order by opportunity_gap desc nulls last
```

<DataTable
    data={course_detail}
    rows=20
    rowShading=true
    search=true
>
    <Column id=institution_name title="Institution" />
    <Column id=course_name title="Course" />
    <Column id=course_level title="Level" />
    <Column id=uac_field_of_study title="Field of Study" />
    <Column id=location_state title="State" />
    <Column id=location_city title="City" />
    <Column id=marketing_signal title="Signal" />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=vacancy_growth_12m title="Vacancy Growth" fmt=pct1 contentType=colorscale />
    <Column id=ft_employment_rate title="FT Employ %" fmt=num1 />
    <Column id=median_salary title="Median Salary" fmt=usd0 />
    <Column id=estimated_total_cost title="Est. Total Cost" fmt=usd0 />
    <Column id=course_count_in_field title="Inst. Field Depth" />
</DataTable>

<Details title="Data Sources">

- **CRICOS Register** — Commonwealth Register of Institutions and Courses for Overseas Students. Course-level data including institution, qualification level, field of education, duration, cost, and delivery location. Covers all CRICOS-registered higher education courses in Australia.
- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Monthly online job vacancy counts by occupation. Used for opportunity gap and vacancy growth calculations.
- **UAC Early Bird Applicant Preferences** — University Admissions Centre. Annual first-preference counts by field of study. NSW/ACT applicants only. Used for preference share in opportunity gap calculation.
- **Graduate Outcomes Survey (GOS) 2024** — Quality Indicators for Learning and Teaching (QILT). Full-time employment rate and median salary by field of study. Undergraduate data only.
- **ASCED-to-UAC field mapping** — CRICOS narrow fields (ASCED codes) are mapped to UAC broad fields via the first two digits of the ASCED code. Some narrow fields may not map cleanly to a single UAC category.

</Details>
