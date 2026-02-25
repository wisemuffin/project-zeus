---
title: Opportunity Gap Analysis
---

Which fields of study have high job demand but low student interest? This analysis combines **Jobs and Skills Australia** Internet Vacancy Index data with **University Admissions Centre (UAC)** Early Bird first preferences to identify targeting opportunities.

For the interactive data explorer, see the [home page](/) which features the opportunity gap chart and state-level demand.

## Summary

Three fields have a positive opportunity gap — job vacancy demand exceeds student preference share. These are the strongest candidates for "study this, jobs are waiting" messaging.

| Rank | Field of Study | Opportunity Gap | Vacancy Share | Preference Share | Vacancy Growth (12m) |
|------|---------------|----------------|---------------|-----------------|---------------------|
| 1 | Health | **+10.2pp** | 36.8% | 26.6% | +7.0% |
| 2 | Information Technology | **+7.2pp** | 10.6% | 3.4% | -10.5% |
| 3 | Management & Commerce | **+4.4pp** | 17.6% | 13.2% | -4.6% |
| 4 | Education | +0.1pp | 5.6% | 5.5% | -5.7% |
| 5 | Architecture & Building | -0.8pp | 3.2% | 4.0% | +3.6% |
| 6 | Engineering & Related Technologies | -2.8pp | 7.4% | 10.2% | -3.8% |
| 7 | Creative Arts | -3.8pp | 2.2% | 6.0% | +19.6% |
| 8 | Society & Culture | -5.4pp | 14.2% | 19.6% | +3.6% |
| 9 | Natural & Physical Sciences | -7.8pp | 2.3% | 10.1% | -5.4% |

*pp = percentage points*

## Key Findings

### 1. Health is the standout opportunity

Health commands 36.8% of all mapped vacancies — more than any other field — and vacancies grew 7.0% year-on-year. Yet only 26.6% of students list it as their first preference. This 10.2 percentage point gap is the largest across all fields.

**Marketing angle:** "Health careers grew 7% this year — demand has never been higher."

### 2. IT has a massive relative gap despite contracting vacancies

Only 3.4% of students prefer IT, but it accounts for 10.6% of vacancies — a 3:1 ratio. However, vacancies are down 10.5% year-on-year, so messaging should focus on the size of the existing market rather than growth.

**Marketing angle:** "IT has 3x more jobs than student interest — there's room for you."

### 3. Management & Commerce is a quiet opportunity

The third-largest gap at 4.4pp. This field has a large absolute vacancy base (10,925 roles) and broad occupational coverage.

### 4. Natural & Physical Sciences has the largest negative gap

Students are 4.4x more interested in this field (10.1% preference) than the job market supports (2.3% vacancy share). This is a challenging field to market on career outcomes alone.

### 5. Creative Arts is growing fastest but from a small base

Vacancies grew 19.6% year-on-year — the fastest of any field — but the absolute base is small (1,371 roles, 2.2% share). Worth monitoring.

## Gender Targeting

Gender preference data reveals how ad creative and audience targeting should differ per field.

| Field of Study | Female Pref. | Male Pref. | Gender Skew | Direction |
|---------------|-------------|------------|-------------|-----------|
| Health | 32.4% | 19.1% | +13.3pp | Female |
| Information Technology | 1.3% | 6.0% | -4.7pp | Male |
| Management & Commerce | 10.1% | 17.4% | -7.3pp | Male |
| Education | 7.3% | 3.1% | +4.2pp | Female |
| Engineering & Related Technologies | 4.0% | 18.5% | -14.5pp | Male |
| Society & Culture | 22.6% | 15.4% | +7.2pp | Female |
| Natural & Physical Sciences | 10.3% | 9.8% | +0.5pp | Balanced |

### Targeting implications

- **Health** (top opportunity): Skews heavily female. Male students are significantly under-represented (19.1% vs 32.4%). Targeting male audiences with health career messaging could capture an underserved segment.
- **IT** (#2 opportunity): Skews male but both genders show very low interest. Female preference is just 1.3% — targeted campaigns to women in tech could differentiate a university's offering.
- **Management & Commerce** (#3 opportunity): Skews male (17.4% vs 10.1%). Female-targeted business and commerce messaging is an underexplored angle.
- **Engineering**: The most gender-skewed field at -14.5pp. Despite having a negative opportunity gap overall, female-targeted engineering campaigns address both diversity goals and an underserved audience.

<Details title="Data Sources">

- **Internet Vacancy Index (IVI)** — Jobs and Skills Australia. Monthly online job vacancy counts by occupation. National scope.
- **UAC Early Bird Applicant Preferences** — University Admissions Centre. Annual first-preference counts by field of study and gender. NSW/ACT applicants only.
- **Occupation-to-Field-of-Study mapping** — manually curated crosswalk linking ANZSCO2 occupation groups to UAC broad fields of education.
- **Source models:** `opportunity_gap`, `opportunity_gap_by_gender`
- Only 9 of 12 UAC fields have mapped ANZSCO2 occupations. "Food, Hospitality & Personal Services", "Mixed Field Programs", and "Agriculture, Environmental & Related Studies" are excluded.
- UAC preference shares below 0.5% are recorded as 0, slightly inflating gaps for very small fields.
- Gender preference data uses abbreviated FOS names which are normalised during staging.

</Details>
