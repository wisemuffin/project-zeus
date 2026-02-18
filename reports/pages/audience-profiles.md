---
title: Audience Profiles by Field of Study
---

Who to target for each field of study — gender split, mature learner affinity, and geographic origin based on **University Admissions Centre (UAC)** applicant data. Use these profiles to shape ad targeting parameters and creative messaging per field.

**More reports:** [Opportunity Gap Dashboard](/) | [Graduate Outcomes](/graduate-outcomes) | [Institution Scorecard](/institution-scorecard) | [Trending Interests](/trending-interests) | [Historical Demand](/historical-demand)

```sql profile_summary
select
    field_of_study,
    opportunity_rank,
    opportunity_gap,
    gender_skew,
    mature_learner_index,
    interstate_draw_ratio
from zeus.audience_profile_by_fos
order by opportunity_rank
```

```sql top_mature
select field_of_study, mature_learner_index
from zeus.audience_profile_by_fos
where mature_learner_index = (select max(mature_learner_index) from zeus.audience_profile_by_fos)
```

```sql top_interstate
select field_of_study, interstate_draw_ratio
from zeus.audience_profile_by_fos
where interstate_draw_ratio = (select max(interstate_draw_ratio) from zeus.audience_profile_by_fos)
```

```sql field_count
select count(*) as total from zeus.audience_profile_by_fos
```

<BigValue
    data={field_count}
    value=total
    title="Fields Profiled"
/>
<BigValue
    data={top_mature}
    value=field_of_study
    title="Highest Mature Learner Affinity"
/>
<BigValue
    data={top_interstate}
    value=field_of_study
    title="Strongest Interstate Draw"
/>

## Gender Split

Female vs male preference share by field. Fields with strong skew present opportunities for gender-targeted creative and channel selection.

```sql gender_split
select
    field_of_study,
    female_preference_share,
    male_preference_share,
    gender_skew
from zeus.audience_profile_by_fos
order by opportunity_rank
```

<BarChart
    data={gender_split}
    x=field_of_study
    y={['female_preference_share', 'male_preference_share']}
    title="Preference Share by Gender"
    yAxisTitle="Preference Share"
    yFmt=pct1
    type=grouped
    sort=false
/>

## Mature Learner Index

Ratio of non-Year 12 preference share to total preference share. Values above 1.0 indicate fields that over-index for mature/non-traditional learners — useful for targeting working professionals and career changers.

```sql mature_chart
select
    field_of_study,
    mature_learner_index,
    non_yr12_preference_share,
    total_preference_share
from zeus.audience_profile_by_fos
order by mature_learner_index desc
```

<BarChart
    data={mature_chart}
    x=field_of_study
    y=mature_learner_index
    title="Mature Learner Index by Field"
    yAxisTitle="Index (1.0 = average)"
    sort=false
/>

## Geographic Origin

Where applicants come from — NSW, ACT, or interstate. The interstate draw ratio shows how strongly a field attracts students from outside its home state relative to overall preference share.

```sql geo_chart
select
    field_of_study,
    nsw_preference_share,
    act_preference_share,
    interstate_preference_share
from zeus.audience_profile_by_fos
order by opportunity_rank
```

<BarChart
    data={geo_chart}
    x=field_of_study
    y={['nsw_preference_share', 'act_preference_share', 'interstate_preference_share']}
    title="Preference Share by Geographic Origin"
    yAxisTitle="Preference Share"
    yFmt=pct1
    type=stacked
    sort=false
/>

```sql profile_table
select * from zeus.audience_profile_by_fos order by opportunity_rank
```

<DataTable
    data={profile_table}
    rows=all
    rowShading=true
    search=true
>
    <Column id=opportunity_rank title="Rank" />
    <Column id=field_of_study title="Field of Study" />
    <Column id=gender_skew title="Gender Skew" />
    <Column id=female_preference_share title="Female Pref" fmt=pct1 />
    <Column id=male_preference_share title="Male Pref" fmt=pct1 />
    <Column id=mature_learner_index title="Mature Index" fmt=num2 />
    <Column id=nsw_preference_share title="NSW" fmt=pct1 />
    <Column id=act_preference_share title="ACT" fmt=pct1 />
    <Column id=interstate_preference_share title="Interstate" fmt=pct1 />
    <Column id=interstate_draw_ratio title="Interstate Draw" fmt=num2 />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 />
</DataTable>

<Details title="Data Sources">

- **UAC Early Bird Applicants by Applicant Type** — University Admissions Centre. Annual first-preference counts segmented by applicant type (Year 12, non-Year 12, etc.) and field of study. NSW/ACT applicants only.
- **UAC Early Bird Applicants by Gender** — University Admissions Centre. Annual first-preference counts segmented by gender and field of study. NSW/ACT applicants only.
- **Opportunity gap context** — derived from the Internet Vacancy Index (Jobs and Skills Australia) and UAC preference data via the opportunity_gap mart.

</Details>
