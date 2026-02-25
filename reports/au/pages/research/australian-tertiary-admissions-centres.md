---
title: Australian Tertiary Admissions Centres
---

Australia has no national university admissions system. Instead, each state or territory has its own Tertiary Admissions Centre (TAC) that processes applications and calculates ATARs. Understanding which TACs publish useful data — and at what granularity — determines where we can replicate the audience-profiles analysis beyond NSW/ACT.

## Overview

All TACs perform the same core functions:
- **Centralised application processing** — students submit one application to a TAC, listing preferences for multiple universities and courses
- **ATAR calculation** — converting Year 12 results into a nationally comparable rank
- **Offer management** — coordinating offers across institutions to avoid double-handling

Despite the common function, each TAC differs significantly in governance, scale, the number of member institutions, and — critically for Zeus — what data they publish.

## TAC-by-TAC Breakdown

### UAC — Universities Admissions Centre (NSW, ACT)

| | |
|---|---|
| **Coverage** | NSW and ACT |
| **Structure** | Non-profit, owned by member universities |
| **Scale** | ~68,700 domestic undergraduate applications at Early Bird closing (2025-26) |

UAC publishes the **most granular public preference data** of any Australian TAC. Available as downloadable Excel files covering 2016-2025:

- **Applicants by category, gender, offers and age** — breakdown by applicant type (Year 12, Non-Year 12, Interstate & IB), gender (Female, Male, Other), and age bands
- **First preferences and offers by broad field of study** — preference shares by field segmented by applicant type
- **First preferences and offers by institution** — per-university demand signals
- **Applicants and offers by region** — NSW regions plus other states
- **ATAR distribution** — for NSW Year 12 students

**Usefulness for Zeus: High.** UAC is the foundation of Project Zeus's current audience-profiles analysis. The field-of-study x applicant-type x gender cross-tabulations enable the mature learner index, interstate draw ratio, and gender skew metrics. No other TAC publishes data at this granularity.

---

### QTAC — Queensland Tertiary Admissions Centre (QLD)

| | |
|---|---|
| **Coverage** | Queensland (plus some Northern NSW institutions) |
| **Structure** | Non-profit, owned by 17 member institutions |
| **Scale** | ~40,000+ applicants securing Early Bird fee (2025-26) |

QTAC publishes **ATAR reports** but **does not appear to publish field-of-study preference breakdowns** or demographic cross-tabulations in the way UAC does.

**Usefulness for Zeus: Low without direct engagement.** QTAC's public data focuses on ATAR calculation rather than preference analytics.

---

### VTAC — Victorian Tertiary Admissions Centre (VIC)

| | |
|---|---|
| **Coverage** | Victoria |
| **Structure** | Non-profit, owned by member institutions |
| **Scale** | ~47,500 tertiary offers to Year 12 students (December 2024) |

VTAC publishes course-level application counts (useful for institutional demand signals) but **not the demographic or field-of-study cross-tabulations** needed for audience profiling. The most valuable preference data is **restricted to member institutions**.

**Usefulness for Zeus: Limited.** Victoria is Australia's second-largest higher education market, making this a significant gap.

---

### SATAC — South Australian Tertiary Admissions Centre (SA, NT)

| | |
|---|---|
| **Coverage** | South Australia and Northern Territory |
| **Structure** | Non-profit, established 1977 by SA universities |

SATAC publishes **the second-most useful public data** after UAC, with similar breakdowns: applicants and offers by gender and age, first preferences by broad field of study, applicants by region, and first preferences by institution.

**Usefulness for Zeus: Moderate to high.** SATAC's field-of-study and gender/age breakdowns are structurally similar to UAC's data. SATAC is the most promising TAC for geographic expansion after UAC.

---

### TISC — Tertiary Institutions Service Centre (WA)

| | |
|---|---|
| **Coverage** | Western Australia |
| **Structure** | Non-profit, owned by WA's four public universities |
| **Scale** | ~10,265 students achieving an ATAR in 2025 |

TISC's public data focuses on ATAR scaling and institutional offer statistics, without field-of-study or demographic breakdowns.

**Usefulness for Zeus: Low.** WA is also the smallest mainland higher education market.

---

### Tasmania — No TAC

The University of Tasmania is the only university in the state and handles admissions directly. There is no centralised TAC.

**Usefulness for Zeus: Minimal.** Single-institution market with no centralised preference data.

## Comparative Summary

| TAC | States | FOS Preferences | Gender/Age | Applicant Type | Region | Usefulness |
|-----|--------|:-:|:-:|:-:|:-:|---|
| **UAC** | NSW, ACT | Yes | Yes | Yes | Yes | **High** — current data source |
| **SATAC** | SA, NT | Yes | Yes | ? | Yes | **Moderate-High** — needs validation |
| **VTAC** | VIC | No (restricted) | No | No | No | **Low** — key data behind paywall |
| **QTAC** | QLD | No | No | No | No | **Low** — ATAR reports only |
| **TISC** | WA | No | No | No | Yes (limited) | **Low** — small market |
| **UTAS** | TAS | N/A | N/A | N/A | N/A | **Minimal** — no TAC |

## Implications for Project Zeus

### Current state
Project Zeus currently uses **UAC data only** (NSW/ACT), which covers approximately **30% of Australia's domestic undergraduate applicants**.

### Expansion priority
**SATAC is the most promising expansion target.** It publishes field-of-study preference data and gender/age breakdowns in a similar structure to UAC. If SATAC's data includes applicant-type segmentation, we could extend the audience-profiles analysis to cover SA and NT.

### The Victoria gap
**Victoria (VTAC) is the biggest gap.** It's Australia's second-largest higher education market, but VTAC restricts detailed preference data to member institutions.

### Queensland gap
**Queensland (QTAC) is similarly limited.** QTAC publishes ATAR reports but not field-of-study preference breakdowns. Queensland is the third-largest market.

<Details title="Data Sources">

- **UAC** — University Admissions Centre. NSW/ACT admissions data including field-of-study preferences by applicant type, gender, and region.
- **QTAC** — Queensland Tertiary Admissions Centre. ATAR reports and course guides.
- **VTAC** — Victorian Tertiary Admissions Centre. Application statistics and scaling reports; detailed preference data restricted to members.
- **SATAC** — South Australian Tertiary Admissions Centre. Applicant and offer statistics by field of study, gender/age, and region.
- **TISC** — Tertiary Institutions Service Centre (WA). Application/offer statistics and ATAR scaling.
- **UTAS** — University of Tasmania. Direct applications only (no TAC).
- Research date: February 2026. Data availability may change as TACs update their publishing practices.

</Details>
