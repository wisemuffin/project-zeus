---
title: Audience Profiles by Field of Study
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-blue-100 text-blue-800">National</span>

Who to target for each field of study — gender split, mature learner affinity, and geographic origin based on **University Admissions Centre (UAC)** Early Bird applicant data. See the [Audience Profile insight](/insights/audience-profile-by-fos) for detailed targeting strategies per field and audience segment recommendations.

UAC is the central admissions portal for NSW/ACT universities. When prospective students apply, they rank their preferred fields of study — giving us a revealed-preference signal of what different audience segments actually want to study. By comparing preference shares across segments (gender, age group, geography), we can build audience profiles that shape ad targeting and creative messaging per field.

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

## How to Read These Metrics

- **Mature Learner Index** — Non-Year 12 preference share / Total preference share. Above 1.0 means the field over-indexes with mature-age applicants (career changers, working professionals). Below 1.0 means it skews toward school leavers.
- **Interstate Draw Ratio** — Interstate preference share / NSW preference share. Above 1.0 means the field pulls disproportionately from interstate — justifying national campaign reach. Below 1.0 means demand is local.
- **Gender Skew** — Whether first preferences skew Female or Male. Informs ad creative and platform selection.
- **Opportunity Gap** — Job vacancy share minus student preference share. Positive values flag fields where employer demand outstrips student interest — a messaging opportunity.

## Gender Split

Female vs male preference share by field. Fields with strong skew present opportunities for gender-targeted creative and channel selection — for example, a female-skewed field may perform better with career-stability messaging on Instagram, while a male-skewed field may suit career-outcomes messaging on TikTok.

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

Ratio of non-Year 12 preference share to total preference share. Values above 1.0 indicate fields that over-index for mature/non-traditional learners — career changers and working professionals who are more reachable on Facebook and LinkedIn. Fields below 1.0 skew toward Year 12 school leavers, who are better reached on TikTok and Instagram.

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

Where applicants come from — NSW, ACT, or interstate. Fields with a high interstate draw ratio (above 1.0) justify national campaign reach, while those with low ratios should focus spend on NSW/ACT only to avoid wasted impressions.

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

## Targeting Takeaways

Key patterns that emerge when the three dimensions are combined:

- **Health** attracts both mature learners (index 1.30) and interstate students (draw 1.59) — run parallel campaigns for career changers and interstate school leavers
- **IT** over-indexes with mature learners (1.24) but is hyper-local (draw 0.47) — focus on NSW/ACT career-change messaging, don't waste spend on national reach
- **Education** is the most geographically local field (draw 0.11) — hyperlocal NSW/ACT campaigns only
- **Engineering** and **Natural & Physical Sciences** draw disproportionately from interstate — these fields justify national campaigns
- **Management & Commerce** and **Architecture & Building** skew young and local — target male Year 12 school leavers in NSW/ACT

## Audience Segments

These profiles suggest four distinct audience segments for campaign planning:

| Segment | Top Fields | Campaign Approach |
|---------|-----------|-------------------|
| Female mature-age career changers | Health, IT | Facebook/LinkedIn, career change messaging |
| Male school leavers (NSW/ACT) | IT, Management & Commerce, Architecture | TikTok/Instagram, career outcomes messaging |
| Female school leavers (NSW/ACT) | Health, Education, Society & Culture | Instagram, career stability messaging |
| Interstate school leavers | Health, Engineering, Natural Sciences | National reach campaigns |

## Full Profile Data

```sql profile_table
select * from zeus.audience_profile_by_fos order by opportunity_rank
```

<DataTable
    data={profile_table}

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
