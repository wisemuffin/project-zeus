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

```sql brand_ranked
select
    *,
    21 - quality_rank as quality_rank_vs_median,
    21 - interest_rank as interest_rank_vs_median
from (${brand})
```

<BigValue
    data={brand_ranked}
    value=quality_rank
    title="Quality Rank"
    description="out of 42 universities (1 = best)"
    comparison=quality_rank_vs_median
    comparisonTitle="vs median"
    downIsGood=true
/>
<BigValue
    data={brand_ranked}
    value=interest_rank
    title="Search Interest Rank"
    description="out of 42 universities (1 = most searched)"
    comparison=interest_rank_vs_median
    comparisonTitle="vs median"
    downIsGood=true
/>
<BigValue
    data={brand}
    value=interest_quality_gap
    title="Interest-Quality Gap"
    description="Positive = under-searched for quality"
    comparison=interest_trend
    comparisonTitle="trend"
/>
{#if brand[0].awareness_tier === 'High'}
<BigValue
    data={brand}
    value=awareness_tier
    title="Awareness Tier"
    comparison=avg_interest_12m
    comparisonTitle="avg interest"
    comparisonFmt=num1
    valueClass="text-positive"
/>
{:else if brand[0].awareness_tier === 'Low'}
<BigValue
    data={brand}
    value=awareness_tier
    title="Awareness Tier"
    comparison=avg_interest_12m
    comparisonTitle="avg interest"
    comparisonFmt=num1
    valueClass="text-negative"
/>
{:else}
<BigValue
    data={brand}
    value=awareness_tier
    title="Awareness Tier"
    comparison=avg_interest_12m
    comparisonTitle="avg interest"
    comparisonFmt=num1
/>
{/if}

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
    'Sector Avg' as group_label,
    avg_overall_quality as overall_quality,
    avg_ft_employment_rate as ft_employment_rate,
    avg_median_salary as median_salary
from zeus.institution_scorecard
where institution = '${inputs.selected_university.value}'
```

### Selected University vs Sector Average

<Grid cols=3>
<div style="background-color: #f8f8f8; padding: 16px; border-radius: 10px; border: 1px solid #e5e5e5;">
<BigValue
    data={scorecard}
    value=overall_quality
    title="Overall Quality"
    fmt={'0.0"%"'}
    comparison=quality_vs_sector
    comparisonTitle="vs sector"
    comparisonFmt={'"+0.0;-0.0"'}
/>
<BarChart
    data={scorecard_comparison}
    x=group_label
    y=overall_quality
    series=group_label
    yMin=0
    yGridlines=false
    yAxisLabels=false
    colorPalette={['#b0b0b0', '#1e3a5f']}
    labels=true
    labelFmt={'0.0"%"'}
    labelPosition=above
    legend=false
    echartsOptions={{backgroundColor: '#f8f8f8'}}
/>
</div>
<div style="background-color: #f8f8f8; padding: 16px; border-radius: 10px; border: 1px solid #e5e5e5;">
<BigValue
    data={scorecard}
    value=ft_employment_rate
    title="FT Employment Rate"
    fmt={'0.0"%"'}
    comparison=employment_vs_sector
    comparisonTitle="vs sector"
    comparisonFmt={'"+0.0;-0.0"'}
/>
<BarChart
    data={scorecard_comparison}
    x=group_label
    y=ft_employment_rate
    series=group_label
    yMin=0
    yGridlines=false
    yAxisLabels=false
    colorPalette={['#b0b0b0', '#1e3a5f']}
    labels=true
    labelFmt={'0.0"%"'}
    labelPosition=above
    legend=false
    echartsOptions={{backgroundColor: '#f8f8f8'}}
/>
</div>
<div style="background-color: #f8f8f8; padding: 16px; border-radius: 10px; border: 1px solid #e5e5e5;">
<BigValue
    data={scorecard}
    value=median_salary
    title="Median Salary"
    fmt=usd0
    comparison=salary_vs_sector
    comparisonTitle="vs sector"
    comparisonFmt=usd0
/>
<BarChart
    data={scorecard_comparison}
    x=group_label
    y=median_salary
    series=group_label
    yMin=0
    yGridlines=false
    yAxisLabels=false
    colorPalette={['#b0b0b0', '#1e3a5f']}
    labels=true
    labelFmt=usd0
    labelPosition=above
    legend=false
    echartsOptions={{backgroundColor: '#f8f8f8'}}
/>
</div>
</Grid>

### QILT Quality Breakdown

The overall quality score is a composite of five QILT Student Experience Survey dimensions. This breakdown shows where the university is strongest and where there's room to improve messaging around the student experience.

```sql quality_breakdown
with selected as (
    select teaching_quality, skills_development, student_support, learning_resources, peer_engagement
    from zeus.institution_scorecard
    where institution = '${inputs.selected_university.value}'
),
sector as (
    select
        avg(teaching_quality) as teaching_quality,
        avg(skills_development) as skills_development,
        avg(student_support) as student_support,
        avg(learning_resources) as learning_resources,
        avg(peer_engagement) as peer_engagement
    from zeus.institution_scorecard
)
select dimension, score, group_label from (
    select 'Teaching' as dimension, teaching_quality as score, 'Selected' as group_label, 1 as sort_order from selected
    union all select 'Skills Development', skills_development, 'Selected', 2 from selected
    union all select 'Student Support', student_support, 'Selected', 3 from selected
    union all select 'Learning Resources', learning_resources, 'Selected', 4 from selected
    union all select 'Peer Engagement', peer_engagement, 'Selected', 5 from selected
    union all select 'Teaching', teaching_quality, 'Sector Average', 1 from sector
    union all select 'Skills Development', skills_development, 'Sector Average', 2 from sector
    union all select 'Student Support', student_support, 'Sector Average', 3 from sector
    union all select 'Learning Resources', learning_resources, 'Sector Average', 4 from sector
    union all select 'Peer Engagement', peer_engagement, 'Sector Average', 5 from sector
)
order by sort_order, group_label
```

<BarChart
    data={quality_breakdown}
    x=dimension
    y=score
    series=group_label
    swapXY=true
    sort=false
    type=grouped
    labels=true
    labelFmt={'0.0"%"'}
    labelPosition=above
    colorPalette={['#b0b0b0', '#1e3a5f']}
    title="Where does the student experience stand out?"
    yGridlines=false
    yAxisLabels=false
    xAxisTitle=""
/>

## Enrolment Profile

DET Higher Education enrolment data showing the selected university's student composition by field of study — international share, online/external delivery, gender mix, and pipeline health. Use this to tailor messaging to each field's actual student profile.

```sql enrolment_summary
select
    institution,
    sum(total_enrolments) as total_enrolments,
    round(sum(international_enrolments) * 1.0 / nullif(sum(total_enrolments), 0), 3) as intl_share,
    round(sum(external_enrolments) * 1.0 / nullif(sum(total_enrolments), 0), 3) as ext_share,
    count(distinct uac_field_of_study) as fields_count
from zeus.institution_enrolment_profile
where institution = '${inputs.selected_university.value}'
group by institution
```

<BigValue
    data={enrolment_summary}
    value=total_enrolments
    title="Total Enrolments"
    fmt=num0
/>
<BigValue
    data={enrolment_summary}
    value=intl_share
    title="International Share"
    fmt=pct1
/>
<BigValue
    data={enrolment_summary}
    value=ext_share
    title="External/Online Share"
    fmt=pct1
/>
<BigValue
    data={enrolment_summary}
    value=fields_count
    title="Fields with Enrolments"
/>

```sql enrolment_detail
select
    uac_field_of_study as field_of_study,
    total_enrolments,
    international_enrolments,
    international_share,
    sector_international_share,
    international_index,
    external_enrolments,
    external_share,
    female_share,
    sector_female_share,
    commencing_share,
    opportunity_gap,
    opportunity_rank,
    field_rank_in_institution
from zeus.institution_enrolment_profile
where institution = '${inputs.selected_university.value}'
order by field_rank_in_institution
```

<DataTable data={enrolment_detail} rowShading=true>
    <Column id=field_of_study title="Field of Study" />
    <Column id=total_enrolments title="Enrolments" fmt=num0 />
    <Column id=international_share title="Intl %" fmt=pct1 />
    <Column id=sector_international_share title="Sector Intl %" fmt=pct1 />
    <Column id=international_index title="Intl Index" fmt=num2 contentType=colorscale />
    <Column id=external_share title="External %" fmt=pct1 />
    <Column id=female_share title="Female %" fmt=pct1 />
    <Column id=sector_female_share title="Sector Female %" fmt=pct1 />
    <Column id=commencing_share title="Commencing %" fmt=pct1 />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
</DataTable>

**Reading the enrolment data:**
- **International index** above 1.0 means this institution has a higher-than-sector share of international students in that field — a signal for international recruitment messaging or to diversify toward domestic
- **External share** shows online/distance penetration — high values indicate established distance programs suitable for "study from anywhere" campaigns
- **Commencing share** above ~0.3 suggests healthy pipeline; below ~0.2 may indicate mature programs with limited new student inflow

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
    title="Where are the strongest courses?"
    yAxisTitle="Number of Courses"
    type=grouped
    sort=false
    swapXY=true
    colorPalette={['#b0b0b0', '#1e3a5f', '#e07020']}
    labels=true
    labelPosition=above
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
    marketing_signal,
    opportunity_gap,
    ft_employment_rate,
    median_salary,
    vacancy_growth_12m,
    location_state,
    location_city,
    estimated_total_cost
from zeus.university_course_listings
where (institution_name like '${inputs.selected_university.value}%'
   or institution_name like 'The ' || '${inputs.selected_university.value}' || '%')
   and uac_field_of_study like '${inputs.field_filter.value}%'
order by opportunity_gap desc nulls last
```

```sql field_options
select distinct uac_field_of_study as field
from zeus.university_course_listings
where institution_name like '${inputs.selected_university.value}%'
   or institution_name like 'The ' || '${inputs.selected_university.value}' || '%'
order by field
```

<Dropdown
    name=field_filter
    data={field_options}
    value=field
    title="Filter by Field"
>
    <DropdownOption value="" valueLabel="All Fields" />
</Dropdown>

<DataTable
    data={courses}
    rows=20
    rowShading=true
    search=true
>
    <Column id=course_name title="Course" />
    <Column id=course_level title="Level" />
    <Column id=uac_field_of_study title="Field" />
    <Column id=marketing_signal title="Signal" />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 contentType=colorscale colorScale=positive />
    <Column id=ft_employment_rate title="FT Employ %" fmt=num1 />
    <Column id=median_salary title="Salary" fmt=usd0 />
    <Column id=vacancy_growth_12m title="Vacancy Growth" fmt=pct1 contentType=colorscale />
    <Column id=location_state title="State" />
    <Column id=location_city title="City" />
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
    g.marketing_signal,
    g.survey_year,
    g.survey_year_prior
from zeus.graduate_outcomes_by_fos g
inner join (${uni_fields}) f on g.field_of_study = f.uac_field_of_study
order by g.ft_employment_rate desc
```

<Grid cols=2>
<BarChart
    data={outcomes}
    x=field_of_study
    y=ft_employment_rate
    yFmt=num1
    title="Which fields lead on employment?"
    yAxisTitle="FT Employment %"
    yMin=0
    sort=false
    swapXY=true
    labels=true
    labelFmt=num1
/>
<BarChart
    data={outcomes}
    x=field_of_study
    y=median_salary
    yFmt=usd0
    title="Which fields pay the most?"
    yAxisTitle="Salary"
    yMin=0
    labels=true
    labelFmt=usd0
    sort=false
    swapXY=true
/>
</Grid>

Salary growth shows the percentage change in median graduate salary between **{outcomes[0].survey_year_prior}** and **{outcomes[0].survey_year}** (QILT Graduate Outcomes Survey). Large values typically reflect small base salaries in the earlier period rather than dramatic market shifts.

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
    <Column id=vacancy_growth_12m title="Vacancy Growth" fmt=pct1 contentType=colorscale />
    <Column id=state_vs_national_skew title="State vs National" fmt={'+0.00;-0.00'} contentType=colorscale />
    <Column id=fos_share_in_state title="FoS Share" fmt=pct1 />
    <Column id=vacancies_per_1k_youth title="Per 1k Youth" fmt=num1 />
    <Column id=state_specialisation_rank title="Spec. Rank" />
</DataTable>

<Details title="Data Sources">

- **QILT Student Experience Survey (SES) 2024** — Quality Indicators for Learning and Teaching, Australian Government. Six satisfaction indicators (% positive rating) covering skills development, peer engagement, teaching quality, student support, learning resources, and overall educational experience. Undergraduate data from universities only.
- **QILT Graduate Outcomes Survey (GOS) 2024** — Quality Indicators for Learning and Teaching. Full-time employment rate, median annual salary, and salary by gender per field of study. Undergraduate data from universities only.
- **Google Trends** — Google (trends.google.com). Search interest by state for university names, normalised using University of Melbourne as anchor. Acronym searches (QUT, UTS, UNSW, RMIT) may capture non-university intent.
- **CRICOS Register** — Commonwealth Register of Institutions and Courses for Overseas Students. Course-level data including institution, qualification level, field of education, duration, cost, and delivery location.
- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Monthly online job vacancy counts by occupation and state. Used for opportunity gap, vacancy growth, and state demand calculations.
- **UAC Early Bird Applicant Preferences** — University Admissions Centre. Annual first-preference counts by field of study, gender, and applicant type. NSW/ACT applicants only.
- **ABS Estimated Resident Population** — Australian Bureau of Statistics. Youth population (15-19) by state for demand density calculations.
- **DET Higher Education Student Enrolments** — Department of Education, Australian Government. Institution × field × citizenship × mode enrolments from 2016-2020 pivot table. National coverage (~47 institutions).
- **Occupation-to-Field-of-Study mapping** — manually curated crosswalk linking ANZSCO occupation groups to broad fields of education.

</Details>
