---
title: State Preference Comparison
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-amber-100 text-amber-800">NSW/ACT · VIC · SA/NT</span>

How applicant preferences differ by field of study across three states — based on **UAC** (NSW/ACT), **VTAC** (Victoria), and **SATAC** (SA/NT) first-preference data, covering ~72% of Australian applicants. Use these cross-state signals to tailor geo-targeted campaigns: a field that's popular in one state but underrepresented in another may indicate unmet demand or a saturated market.

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
    field_of_study,
    max(case when state = 'NSW/ACT' then preference_share end) as nsw_act_share,
    max(case when state = 'VIC' then preference_share end) as vic_share,
    max(case when state = 'SA/NT' then preference_share end) as sa_nt_share,
    max(preference_share) - min(preference_share) as max_spread
from (
    select field_of_study, state, sum(preference_share) as preference_share
    from zeus.national_fos_preferences
    group by field_of_study, state
)
group by field_of_study
order by max_spread desc
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

Combined female + male preference share for each field, comparing NSW/ACT (UAC), Victoria (VTAC), and SA/NT (SATAC).

<BarChart
    data={total_by_state}
    x=field_of_study
    y=preference_share
    series=state
    title="Field of Study Preference Share by State"
    yAxisTitle="Preference Share"
    yFmt=pct1
    type=grouped
    sort=false
/>

## Largest Divergences

Fields where preference share varies most across states. A large spread may signal untapped demand or regional market saturation.

<DataTable
    data={divergence}
    rowShading=true
>
    <Column id=field_of_study title="Field of Study" />
    <Column id=nsw_act_share title="NSW/ACT" fmt=pct1 />
    <Column id=vic_share title="VIC" fmt=pct1 />
    <Column id=sa_nt_share title="SA/NT" fmt=pct1 />
    <Column id=max_spread title="Max Spread" fmt=pct1 />
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

- **UAC (University Admissions Centre)** — Early Bird applicant data, 2024-25. Field-of-study first preferences by gender. NSW/ACT only.
- **VTAC (Victorian Tertiary Admissions Centre)** — Annual statistics Section D (Table D1), 2020-21 data. Field-of-study first preferences by gender for Victorian applicants. Victoria only.
- **SATAC (South Australian Tertiary Admissions Centre)** — Undergraduate first preferences and total offers by broad field of study, 2025 PDF. Year 12 + Non-Year 12 summed for domestic totals. SA/NT only. "Food, Hospitality & Personal Services" absent in SA data.
- All sources use ASCED broad field classification. Field names are normalised to canonical categories for comparability. "Mixed Field Programs/Programmes" excluded (no UAC equivalent).

</Details>
