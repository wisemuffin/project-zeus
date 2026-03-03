---
title: University Brief
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-purple-100 text-purple-800">Per-University</span>

Marketing intelligence brief for a selected university, combining brand positioning, program portfolio, audience profiles, and geographic targeting data. Use this page to prepare personalised outreach briefs or walk through a university's competitive position in a sales meeting.

```sql uni_list
select distinct university
from zeus.university_brand_awareness
where university <> 'All universities'
order by university
```

<Dropdown
    name=selected_university
    data={uni_list}
    value=university
    title="Select University"
/>

## Brand Position

```sql brand
select
    university,
    quality_rank,
    interest_rank,
    interest_quality_gap,
    awareness_tier,
    avg_interest_12m,
    interest_momentum,
    interest_trend,
    overall_quality,
    ft_employment_rate,
    median_salary,
    top_state
from zeus.university_brand_awareness
where university = '${inputs.selected_university.value}'
```

```sql scorecard
select
    institution,
    overall_quality,
    teaching_quality,
    skills_development,
    student_support,
    learning_resources,
    peer_engagement,
    ft_employment_rate,
    median_salary,
    quality_rank,
    employment_rank,
    salary_rank,
    quality_vs_sector,
    employment_vs_sector,
    salary_vs_sector,
    avg_overall_quality,
    avg_ft_employment_rate,
    avg_median_salary
from zeus.institution_scorecard
where institution = '${inputs.selected_university.value}'
```

<BigValue
    data={brand}
    value=quality_rank
    title="Quality Rank"
    description="out of 42 universities"
/>
<BigValue
    data={brand}
    value=interest_rank
    title="Search Interest Rank"
    description="out of 42 universities"
/>
<BigValue
    data={brand}
    value=interest_quality_gap
    title="Interest-Quality Gap"
    description="Positive = under-searched for quality"
/>
<BigValue
    data={brand}
    value=awareness_tier
    title="Awareness Tier"
/>

A positive interest-quality gap means the university is **under-searched relative to its academic quality** — the marketing story is about increasing awareness of an already-strong product. A negative gap means the brand is well-known but quality metrics don't match — messaging should lead with specific program strengths.

```sql scorecard_comparison
select
    'Selected' as group_label,
    overall_quality,
    ft_employment_rate,
    median_salary
from zeus.institution_scorecard
where institution = '${inputs.selected_university.value}'
union all
select
    'Sector Average' as group_label,
    avg_overall_quality as overall_quality,
    avg_ft_employment_rate as ft_employment_rate,
    avg_median_salary as median_salary
from zeus.institution_scorecard
where institution = '${inputs.selected_university.value}'
```

<BarChart
    data={scorecard_comparison}
    x=group_label
    y={['overall_quality', 'ft_employment_rate']}
    y2=median_salary
    y2Fmt=usd0
    title="Selected University vs Sector Average"
    yAxisTitle="% Rating"
    y2AxisTitle="Median Salary"
    type=grouped
/>

<DataTable data={scorecard} rowShading=true>
    <Column id=overall_quality title="Overall Quality %" fmt=num1 />
    <Column id=teaching_quality title="Teaching %" fmt=num1 />
    <Column id=skills_development title="Skills %" fmt=num1 />
    <Column id=student_support title="Support %" fmt=num1 />
    <Column id=learning_resources title="Resources %" fmt=num1 />
    <Column id=peer_engagement title="Peers %" fmt=num1 />
    <Column id=ft_employment_rate title="FT Employment %" fmt=num1 />
    <Column id=median_salary title="Median Salary" fmt=usd0 />
    <Column id=quality_vs_sector title="Quality vs Sector" fmt=num1 contentType=colorscale />
    <Column id=employment_vs_sector title="Employment vs Sector" fmt=num1 contentType=colorscale />
    <Column id=salary_vs_sector title="Salary vs Sector" fmt=usd0 contentType=colorscale />
</DataTable>

## Geographic Brand Strength

Where the university's brand is strongest and weakest across Australian states. States where the university ranks highly for search interest are natural strongholds; states where it ranks poorly despite geographic proximity are awareness gaps worth targeting.

```sql state_interest
select
    state_name,
    state,
    interest,
    state_rank_for_uni,
    uni_rank_in_state,
    interest_vs_uni_avg
from zeus.university_state_interest
where university = '${inputs.selected_university.value}'
order by interest desc
```

<AreaMap
    data={state_interest}
    geoJsonUrl={addBasePath('/au_state_2021_gen.geojson')}
    geoId="state_name_2021"
    areaCol="state_name"
    value="interest"
    height=400
    startingLat={-28}
    startingLong={134}
    startingZoom={4}
    legendType="scalar"
    title={`Search Interest by State — ${inputs.selected_university.value}`}
    tooltip={[{id: 'state_name', showColumnName: false, valueClass: 'font-bold text-sm'}, {id: 'interest', title: 'Interest', fmt: 'num1'}, {id: 'state_rank_for_uni', title: 'State Rank (for uni)'}, {id: 'uni_rank_in_state', title: 'Uni Rank (in state)'}, {id: 'interest_vs_uni_avg', title: 'vs Uni Avg', fmt: 'num1'}]}
/>

<DataTable data={state_interest} rowShading=true>
    <Column id=state title="State" />
    <Column id=interest title="Interest" fmt=num1 />
    <Column id=state_rank_for_uni title="State Rank (for Uni)" />
    <Column id=uni_rank_in_state title="Uni Rank (in State)" />
    <Column id=interest_vs_uni_avg title="vs Uni Avg" fmt=num1 contentType=colorscale />
</DataTable>

## Program Portfolio & Opportunities

Courses offered by this university mapped to national opportunity gap data. **Strong signal** = high employer demand + strong graduate outcomes. **Demand signal** = high employer demand, moderate outcomes. Focus marketing on fields in the top opportunity tiers.

```sql course_field_summary
select
    uac_field_of_study as field_of_study,
    count(*) as courses,
    count(*) filter (where marketing_signal like 'Strong%') as strong_signal,
    count(*) filter (where opportunity_gap > 0) as high_opp_courses,
    max(opportunity_gap) as opportunity_gap,
    max(opportunity_rank) as opportunity_rank,
    max(vacancy_growth_12m) as vacancy_growth_12m,
    avg(ft_employment_rate) as avg_ft_employment,
    avg(median_salary) as avg_median_salary
from zeus.university_course_listings
where institution_name like '${inputs.selected_university.value}%'
   or institution_name like 'The ' || '${inputs.selected_university.value}' || '%'
group by uac_field_of_study
having uac_field_of_study is not null
order by opportunity_gap desc nulls last
```

<BarChart
    data={course_field_summary}
    x=field_of_study
    y={['courses', 'strong_signal', 'high_opp_courses']}
    title="Course Portfolio by Field of Study"
    xAxisTitle="Field of Study"
    yAxisTitle="Number of Courses"
    type=grouped
    sort=false
/>

<DataTable data={course_field_summary} rowShading=true>
    <Column id=field_of_study title="Field of Study" />
    <Column id=courses title="Total Courses" fmt=num0 />
    <Column id=strong_signal title="Strong Signal" fmt=num0 />
    <Column id=high_opp_courses title="High Opp Gap" fmt=num0 />
    <Column id=opportunity_gap title="Opportunity Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=vacancy_growth_12m title="Vacancy Growth (12m)" fmt=pct1 contentType=colorscale />
    <Column id=avg_ft_employment title="Avg FT Employ %" fmt=num1 />
    <Column id=avg_median_salary title="Avg Median Salary" fmt=usd0 />
</DataTable>

### Course Detail

```sql courses
select
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
    estimated_total_cost
from zeus.university_course_listings
where institution_name like '${inputs.selected_university.value}%'
   or institution_name like 'The ' || '${inputs.selected_university.value}' || '%'
order by opportunity_gap desc nulls last
```

<DataTable
    data={courses}
    rows=15
    rowShading=true
    search=true
>
    <Column id=course_name title="Course" />
    <Column id=course_level title="Level" />
    <Column id=uac_field_of_study title="Field" />
    <Column id=location_state title="State" />
    <Column id=location_city title="City" />
    <Column id=marketing_signal title="Signal" />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=vacancy_growth_12m title="Vacancy Growth" fmt=pct1 contentType=colorscale />
    <Column id=ft_employment_rate title="FT Employ %" fmt=num1 />
    <Column id=median_salary title="Salary" fmt=usd0 />
    <Column id=estimated_total_cost title="Est. Cost" fmt=usd0 />
</DataTable>

## Audience Targeting by Field

National audience profiles for fields of study this university offers. Shows who to target (gender, mature learner affinity) and where the students come from (interstate draw) for each field.

```sql uni_fields
select distinct uac_field_of_study
from zeus.university_course_listings
where (institution_name like '${inputs.selected_university.value}%'
   or institution_name like 'The ' || '${inputs.selected_university.value}' || '%')
  and uac_field_of_study is not null
```

```sql audience
select
    a.field_of_study,
    a.opportunity_gap,
    a.opportunity_rank,
    a.female_preference_share,
    a.male_preference_share,
    a.gender_skew,
    a.mature_learner_index,
    a.interstate_draw_ratio,
    a.nsw_preference_share,
    a.act_preference_share,
    a.interstate_preference_share
from zeus.audience_profile_by_fos a
inner join (${uni_fields}) f on a.field_of_study = f.uac_field_of_study
order by a.opportunity_rank
```

<DataTable data={audience} rowShading=true>
    <Column id=field_of_study title="Field of Study" />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=female_preference_share title="Female %" fmt=pct1 />
    <Column id=male_preference_share title="Male %" fmt=pct1 />
    <Column id=gender_skew title="Gender Skew" />
    <Column id=mature_learner_index title="Mature Learner Index" fmt=num2 />
    <Column id=interstate_draw_ratio title="Interstate Draw" fmt=num2 />
</DataTable>

**Reading the audience data:**
- **Gender skew** tells you which gender to target or which under-represented group to try to attract
- **Mature learner index** above 1.0 means the field attracts more career-changers than average — use career-switcher messaging
- **Interstate draw** above 1.0 means the field attracts students from outside NSW/ACT — run national campaigns. Below 1.0 means students are local — keep campaigns geographically focused.

## Graduate Outcomes by Field

Employment rates, salary levels, and growth trends for the fields this university offers. Use these as proof points in campaign messaging.

```sql outcomes
select
    g.field_of_study,
    g.ft_employment_rate,
    g.median_salary,
    g.salary_growth_pct,
    g.median_salary_male,
    g.median_salary_female,
    g.marketing_signal
from zeus.graduate_outcomes_by_fos g
inner join (${uni_fields}) f on g.field_of_study = f.uac_field_of_study
order by g.ft_employment_rate desc
```

<BarChart
    data={outcomes}
    x=field_of_study
    y=ft_employment_rate
    y2=median_salary
    y2Fmt=usd0
    title="Graduate Outcomes — Fields Offered by This University"
    yAxisTitle="FT Employment Rate (%)"
    y2AxisTitle="Median Salary"
    sort=false
/>

<DataTable data={outcomes} rowShading=true>
    <Column id=field_of_study title="Field of Study" />
    <Column id=ft_employment_rate title="FT Employment %" fmt=num1 />
    <Column id=median_salary title="Median Salary" fmt=usd0 />
    <Column id=salary_growth_pct title="Salary Growth" fmt=pct1 contentType=colorscale />
    <Column id=median_salary_male title="Male Salary" fmt=usd0 />
    <Column id=median_salary_female title="Female Salary" fmt=usd0 />
    <Column id=marketing_signal title="Signal" />
</DataTable>

## State Demand Context

Job vacancy demand by state for fields this university offers. Highlights which states have the strongest labour market pull — use for geographic targeting decisions.

```sql state_demand
select
    s.state,
    s.field_of_study,
    s.vacancies,
    s.fos_share_in_state,
    s.state_vs_national_skew,
    s.vacancy_growth_12m,
    s.vacancies_per_1k_youth,
    s.national_opportunity_gap,
    s.state_specialisation_rank
from zeus.state_fos_demand s
inner join (${uni_fields}) f on s.field_of_study = f.uac_field_of_study
order by s.vacancies desc
```

<DataTable
    data={state_demand}
    rows=15
    rowShading=true
    search=true
>
    <Column id=state title="State" />
    <Column id=field_of_study title="Field" />
    <Column id=vacancies title="Vacancies" fmt=num0 />
    <Column id=fos_share_in_state title="FoS Share in State" fmt=pct1 />
    <Column id=state_vs_national_skew title="State vs National" fmt=num2 contentType=colorscale />
    <Column id=vacancy_growth_12m title="Vacancy Growth (12m)" fmt=pct1 contentType=colorscale />
    <Column id=vacancies_per_1k_youth title="Vacancies / 1k Youth" fmt=num1 />
    <Column id=state_specialisation_rank title="Specialisation Rank" />
</DataTable>

<Details title="Data Sources">

- **QILT Student Experience Survey (SES) 2024** — Quality Indicators for Learning and Teaching, Australian Government. Six satisfaction indicators (% positive rating) covering skills development, peer engagement, teaching quality, student support, learning resources, and overall educational experience. Undergraduate data from universities only.
- **QILT Graduate Outcomes Survey (GOS) 2024** — Quality Indicators for Learning and Teaching. Full-time employment rate, median annual salary, and salary by gender per field of study. Undergraduate data from universities only.
- **Google Trends** — Google (trends.google.com). Search interest by state for university names, normalised using University of Melbourne as anchor. Acronym searches (QUT, UTS, UNSW, RMIT) may capture non-university intent.
- **CRICOS Register** — Commonwealth Register of Institutions and Courses for Overseas Students. Course-level data including institution, qualification level, field of education, duration, cost, and delivery location.
- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Monthly online job vacancy counts by occupation and state. Used for opportunity gap, vacancy growth, and state demand calculations.
- **UAC Early Bird Applicant Preferences** — University Admissions Centre. Annual first-preference counts by field of study, gender, and applicant type. NSW/ACT applicants only.
- **ABS Estimated Resident Population** — Australian Bureau of Statistics. Youth population (15-19) by state for demand density calculations.
- **Occupation-to-Field-of-Study mapping** — manually curated crosswalk linking ANZSCO occupation groups to broad fields of education.

</Details>
