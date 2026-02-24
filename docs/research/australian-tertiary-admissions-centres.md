# Australian Tertiary Admissions Centres (TACs)

> **Last updated:** 2026-02-25
> **Relevance to Project Zeus:** TACs are the primary source of student preference data
> in Australia. Understanding which TACs publish useful data — and at what granularity —
> determines where we can replicate the audience-profiles analysis beyond NSW/ACT.

## Overview

Australia has no national university admissions system. Instead, each state or territory
has its own Tertiary Admissions Centre (TAC) that processes applications and calculates
ATARs (Australian Tertiary Admission Ranks). These are separate organisations with no
shared data infrastructure.

All TACs perform the same core functions:
- **Centralised application processing** — students submit one application to a TAC,
  listing preferences for multiple universities and courses
- **ATAR calculation** — converting Year 12 results into a nationally comparable rank
- **Offer management** — coordinating offers across institutions to avoid double-handling

Despite the common function, each TAC differs significantly in governance, scale, the
number of member institutions, and — critically for Zeus — what data they publish.

## TAC-by-TAC Breakdown

### UAC — Universities Admissions Centre (NSW, ACT)

| | |
|---|---|
| **Website** | [uac.edu.au](https://www.uac.edu.au/) |
| **Coverage** | NSW and ACT |
| **Structure** | Non-profit, owned by member universities |
| **Scale** | ~68,700 domestic undergraduate applications at Early Bird closing (2025–26) |
| **Statistics page** | [uac.edu.au/media-centre/statistics](https://www.uac.edu.au/media-centre/statistics) |

#### Public Data Available

UAC publishes the **most granular public preference data** of any Australian TAC.
Available as downloadable Excel files covering 2016–2025:

- **Applicants by category, gender, offers and age** — breakdown by applicant type
  (Year 12, Non-Year 12, Interstate & IB), gender (Female, Male, Other), and age bands
- **First preferences and offers by broad field of study** — preference shares by
  field (Health, IT, Engineering, etc.) segmented by applicant type
- **First preferences and offers by institution** — per-university demand signals
- **Applicants and offers by region** — NSW regions plus other states
- **ATAR distribution** — for NSW Year 12 students

UAC also publishes media releases with trending field-of-study analysis and year-over-year
comparisons.

#### Usefulness for Zeus

**High.** UAC is the foundation of Project Zeus's current audience-profiles analysis.
The field-of-study × applicant-type × gender cross-tabulations enable the mature learner
index, interstate draw ratio, and gender skew metrics used in the `audience_profile_by_fos`
mart. No other TAC publishes data at this granularity.

---

### QTAC — Queensland Tertiary Admissions Centre (QLD)

| | |
|---|---|
| **Website** | [qtac.edu.au](https://www.qtac.edu.au/) |
| **Coverage** | Queensland (plus some Northern NSW institutions) |
| **Structure** | Non-profit, owned by 17 member institutions |
| **Scale** | ~40,000+ applicants securing Early Bird fee (2025–26) |

#### Public Data Available

QTAC publishes **ATAR reports** (annual, detailed scaling and cohort statistics) but
**does not appear to publish field-of-study preference breakdowns** or demographic
cross-tabulations in the way UAC does.

Available reports:
- **Annual ATAR Reports** — cohort sizes, subject enrolments, scaling processes, ATAR
  distributions (available as PDF, e.g. [2024 report](https://qtac-files.s3.ap-southeast-2.amazonaws.com/ATAR_Report_2024.pdf))
- **Course guides** — downloadable PDF listing available courses and institutions

No publicly accessible preference data by field of study, gender, or applicant type was
found.

#### Usefulness for Zeus

**Low without direct engagement.** QTAC's public data focuses on ATAR calculation rather
than preference analytics. To replicate audience profiling for Queensland, we would need
to either engage QTAC directly or find alternative Queensland-specific data sources
(e.g. QGSO demographics, Queensland government education statistics).

---

### VTAC — Victorian Tertiary Admissions Centre (VIC)

| | |
|---|---|
| **Website** | [vtac.edu.au](https://vtac.edu.au/) |
| **Coverage** | Victoria |
| **Structure** | Non-profit, owned by member institutions |
| **Scale** | ~47,500 tertiary offers to Year 12 students (December 2024) |
| **Statistics page** | [vtac.edu.au/reports](https://vtac.edu.au/reports) |

#### Public Data Available

VTAC publishes several report types, but **preference data is restricted**:

**Publicly available:**
- **Scaling reports** — ATAR scaling methodology and conversion tables
- **ATAR profiles** — aggregate ATAR distributions
- **Lowest selection ranks** — minimum ATAR for domestic offers by course
- **Application statistics** — number of applications by institution and preference level
  (publicly available for historical years, e.g. 2019–2022)
- **Annual reports** — institutional overview

**Restricted (member institutions only):**
- **Weekly preference data** — released throughout the application window (August–February)
  with course-level demand at each preference level
- **Popularity polls** — detailed application counts at specific time points

VTAC's application statistics show applications by course and institution, but **do not
include demographic breakdowns** (gender, age, applicant type) or field-of-study
aggregations.

#### Usefulness for Zeus

**Limited.** VTAC publishes course-level application counts (useful for institutional
demand signals) but not the demographic or field-of-study cross-tabulations needed for
audience profiling. The most valuable preference data is restricted to member institutions.
Victoria is Australia's second-largest higher education market, making this a significant
gap.

---

### SATAC — South Australian Tertiary Admissions Centre (SA, NT)

| | |
|---|---|
| **Website** | [satac.edu.au](https://www.satac.edu.au/) |
| **Coverage** | South Australia and Northern Territory |
| **Structure** | Non-profit, established 1977 by SA universities |
| **Statistics page** | [satac.edu.au/statistics](https://www.satac.edu.au/statistics) |

#### Public Data Available

SATAC publishes **the second-most useful public data** after UAC, with similar
breakdowns:

- **Applicants and offers by gender and age** — demographic cross-tabulation
- **First preferences and total offers by broad field of study** — field-level demand
- **Applicants and total offers by region** — geographic origin of applicants
- **First preferences and total offers by institution** — per-university demand
- **Year 12 applicant ATAR distribution** — entry score profiles

Data is available for 2023, 2024, and 2025 cycles.

SATAC also provides links to equivalent statistics from other state TACs, positioning
itself as a cross-state comparison resource.

#### Usefulness for Zeus

**Moderate to high.** SATAC's field-of-study and gender/age breakdowns are structurally
similar to UAC's data. The key question is whether SATAC publishes the same
applicant-type segmentation (Year 12 vs Non-Year 12 vs Interstate) that enables UAC's
mature learner index calculation. If so, SATAC data could extend the audience-profiles
analysis to SA/NT — making it the most promising TAC for geographic expansion after UAC.

**Action item:** Download SATAC's Excel files and assess whether they include the
applicant-type × field-of-study cross-tabulation needed for the mature learner index
and interstate draw ratio calculations.

---

### TISC — Tertiary Institutions Service Centre (WA)

| | |
|---|---|
| **Website** | [tisc.edu.au](https://www.tisc.edu.au/) |
| **Coverage** | Western Australia |
| **Structure** | Non-profit, owned by WA's four public universities |
| **Scale** | ~10,265 students achieving an ATAR in 2025 |
| **Statistics page** | [tisc.edu.au/static/statistics](https://www.tisc.edu.au/static/statistics/statistics-index.tisc) |

#### Public Data Available

TISC publishes:
- **Application and offer statistics** — available for 2024/2025 and prior years
- **Scaling information** — ATAR scaling methodology and aggregate-to-ATAR conversions
- **Minimum selection ranks** — cutoff ATARs by course and institution
- **Annual reports** — including WA Universities' Foundation Program statistics

TISC's application statistics appear to focus on application and offer volumes by
institution, without the field-of-study or demographic breakdowns available from UAC
or SATAC.

#### Usefulness for Zeus

**Low.** TISC's public data is focused on ATAR scaling and institutional offer
statistics. WA is also the smallest mainland higher education market. Limited value
for audience profiling without direct institutional engagement.

---

### Tasmania — No TAC

| | |
|---|---|
| **Institution** | [University of Tasmania (UTAS)](https://www.utas.edu.au/study/apply) |
| **Coverage** | Tasmania |
| **Admissions model** | Direct application to UTAS (no intermediary TAC) |

Tasmania is unique in that the University of Tasmania is the only university in the state
and handles admissions directly. There is no centralised TAC.

**Key differences from TAC states:**
- No application fee for domestic students
- Students can apply for up to 5 courses at once
- Rolling admissions — no fixed intake dates
- Applications open from August for February starts

#### Usefulness for Zeus

**Minimal.** Single-institution market with no centralised preference data. UTAS
admissions data (if published) would cover only one university.

---

## Comparative Summary

| TAC | States | FOS Preferences | Gender/Age | Applicant Type | Region | Usefulness |
|-----|--------|:-:|:-:|:-:|:-:|---|
| **UAC** | NSW, ACT | Yes | Yes | Yes | Yes | **High** — current data source |
| **SATAC** | SA, NT | Yes | Yes | ? | Yes | **Moderate–High** — needs validation |
| **VTAC** | VIC | No (restricted) | No | No | No | **Low** — key data behind paywall |
| **QTAC** | QLD | No | No | No | No | **Low** — ATAR reports only |
| **TISC** | WA | No | No | No | Yes (limited) | **Low** — small market |
| **UTAS** | TAS | N/A | N/A | N/A | N/A | **Minimal** — no TAC |

## Implications for Project Zeus

### Current state
Project Zeus currently uses **UAC data only** (NSW/ACT), which covers approximately
**30% of Australia's domestic undergraduate applicants**. The audience-profiles analysis
(mature learner index, interstate draw ratio, gender skew) relies on UAC's uniquely
granular field-of-study × applicant-type × gender cross-tabulations.

### Expansion priority
**SATAC is the most promising expansion target.** It publishes field-of-study preference
data and gender/age breakdowns in a similar structure to UAC. If SATAC's data includes
applicant-type segmentation, we could extend the audience-profiles analysis to cover
SA and NT — adding another ~5% of the national market.

### The Victoria gap
**Victoria (VTAC) is the biggest gap.** It's Australia's second-largest higher education
market, but VTAC restricts detailed preference data to member institutions. Covering
Victoria would likely require either:
1. Partnering with a Victorian university that can share VTAC data
2. Finding alternative Victorian data sources (e.g. DESE/TEQSA national statistics)
3. Using national-level datasets (ABS, QILT) as a proxy

### Queensland gap
**Queensland (QTAC) is similarly limited.** QTAC publishes ATAR reports but not
field-of-study preference breakdowns. Queensland is the third-largest market.

### National-level alternatives
To achieve national coverage without TAC data, potential approaches include:
- **DESE (Department of Education) Higher Education Statistics** — national data on
  enrolments (not applications) by field of study, institution, gender, age, etc.
- **QILT (Quality Indicators for Learning and Teaching)** — survey-based data on
  student experience and outcomes by field and institution
- **ABS Education Statistics** — census-based education participation data

These national sources use different methodologies (enrolments vs applications, survey vs
census) and may not support the same revealed-preference analysis that TAC data enables.

## Sources

- [UAC Statistics](https://www.uac.edu.au/media-centre/statistics)
- [UAC Early Bird Statistics 2025](https://www.uac.edu.au/media-centre/statistics/domestic-undergraduate-application-statistics-at-early-bird-closing-2025)
- [QTAC ATAR Report 2024](https://qtac-files.s3.ap-southeast-2.amazonaws.com/ATAR_Report_2024.pdf)
- [QTAC Wikipedia](https://en.wikipedia.org/wiki/Queensland_Tertiary_Admissions_Centre)
- [VTAC Reports and Statistics](https://vtac.edu.au/reports)
- [VTAC Application Statistics 2021/22](https://vtac.edu.au/reports/appstats-ug-2021.html)
- [VTAC Wikipedia](https://en.wikipedia.org/wiki/Victorian_Tertiary_Admissions_Centre)
- [SATAC Statistics](https://www.satac.edu.au/statistics)
- [SATAC Wikipedia](https://en.wikipedia.org/wiki/South_Australian_Tertiary_Admissions_Centre)
- [TISC Reports and Statistics](https://www.tisc.edu.au/static/statistics/statistics-index.tisc)
- [TISC Application and Offer Statistics 2024/2025](https://www.tisc.edu.au/static/statistics/application-offer/statistics-2024-2025.tisc)
- [TISC Wikipedia](https://en.wikipedia.org/wiki/Tertiary_Institutions_Service_Centre)
- [University of Tasmania — How to Apply](https://www.utas.edu.au/study/apply)
- [Times Higher Education — Applying to University in Australia](https://www.timeshighereducation.com/counsellor/admissions-processes-and-funding/applying-university-australia-practical-guide-0)
- [MedView — ATAR & TACs Explained](https://medvieweducation.org/au/resources/blog/guardians/atar-and-tacs-explained)
