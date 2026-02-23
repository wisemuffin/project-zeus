---
title: State Preference Comparison
---

How Victorian and NSW/ACT applicant preferences differ by field of study — based on **VTAC** (Victoria) and **UAC** (NSW/ACT) first-preference data. Use these cross-state signals to tailor geo-targeted campaigns: a field that's popular in one state but underrepresented in another may indicate unmet demand or a saturated market.

**More reports:** [Opportunity Gap Dashboard](/) | [Graduate Outcomes](/graduate-outcomes) | [Institution Scorecard](/institution-scorecard) | [Audience Profiles](/audience-profiles) | [Trending Interests](/trending-interests) | [Historical Demand](/historical-demand) | [State × Field Demand](/state-fos-demand) | [Course Listings](/course-listings)

```sql preferences
select
    field_of_study,
    state,
    gender,
    preference_share
from zeus.national_fos_preferences
```

```sql total_by_state
select
    field_of_study,
    state,
    sum(preference_share) as preference_share
from zeus.national_fos_preferences
group by field_of_study, state
order by field_of_study
```

```sql divergence
select
    nsw.field_of_study,
    nsw.preference_share as nsw_act_share,
    vic.preference_share as vic_share,
    vic.preference_share - nsw.preference_share as difference,
    abs(vic.preference_share - nsw.preference_share) as abs_difference
from (
    select field_of_study, sum(preference_share) as preference_share
    from zeus.national_fos_preferences
    where state = 'NSW/ACT'
    group by field_of_study
) nsw
join (
    select field_of_study, sum(preference_share) as preference_share
    from zeus.national_fos_preferences
    where state = 'VIC'
    group by field_of_study
) vic on nsw.field_of_study = vic.field_of_study
order by abs_difference desc
```

```sql gender_by_state
select
    field_of_study,
    state,
    gender,
    preference_share
from zeus.national_fos_preferences
order by field_of_study, state, gender
```

## Preference Share by State

Combined female + male preference share for each field, comparing NSW/ACT (UAC) with Victoria (VTAC).

<BarChart
    data={total_by_state}
    x=field_of_study
    y=preference_share
    series=state
    title="Field of Study Preference Share: NSW/ACT vs Victoria"
    yAxisTitle="Preference Share"
    yFmt=pct1
    type=grouped
    sort=false
/>

## Largest Divergences

Fields where Victorian preferences diverge most from NSW/ACT — positive difference means VIC has higher preference share, negative means NSW/ACT is higher. Large gaps may signal untapped demand or regional market saturation.

<DataTable
    data={divergence}
    rows=all
    rowShading=true
>
    <Column id=field_of_study title="Field of Study" />
    <Column id=nsw_act_share title="NSW/ACT Share" fmt=pct1 />
    <Column id=vic_share title="VIC Share" fmt=pct1 />
    <Column id=difference title="Difference (VIC − NSW)" fmt=pct1 />
</DataTable>

## Gender Split by State

Female vs male preference share per field and state. Differences in gender patterns between states can inform state-specific creative and targeting.

```sql female_by_state
select field_of_study, state, preference_share
from zeus.national_fos_preferences
where gender = 'Female'
order by field_of_study
```

```sql male_by_state
select field_of_study, state, preference_share
from zeus.national_fos_preferences
where gender = 'Male'
order by field_of_study
```

<BarChart
    data={female_by_state}
    x=field_of_study
    y=preference_share
    series=state
    title="Female Preference Share by State"
    yAxisTitle="Preference Share"
    yFmt=pct1
    type=grouped
    sort=false
/>

<BarChart
    data={male_by_state}
    x=field_of_study
    y=preference_share
    series=state
    title="Male Preference Share by State"
    yAxisTitle="Preference Share"
    yFmt=pct1
    type=grouped
    sort=false
/>

<Details title="Data Sources">

- **VTAC (Victorian Tertiary Admissions Centre)** — Annual statistics Section D (Table D1), 2020-21 data. Field-of-study first preferences by gender for Victorian applicants. Victoria only.
- **UAC (University Admissions Centre)** — Early Bird applicant data, 2024-25. Field-of-study first preferences by gender. NSW/ACT only.
- Both sources use ASCED broad field classification (11 fields). Field names are normalised to canonical categories for comparability. "Mixed Field Programs" excluded (no UAC equivalent).

</Details>
