# The Pitch: Why Universities Need Project Zeus

> The data is public. The value is in the joins.

## The one-liner

We combine 8 government data sources to tell you exactly which programs to promote, what the ad should say, where to run it, and who to target — with proof points.

Instead of guessing which fields to feature in your next campaign, you get a ranked list backed by job vacancy data, graduate employment rates, and salary figures. Instead of running the same ads nationally, you get state-by-state and LGA-level targeting based on where youth populations and job demand actually concentrate.

Every recommendation traces back to a public, auditable data source — Jobs and Skills Australia, QILT, the ABS, and three state admissions centres covering 72% of Australian applicants.

## "Won't the university already have this?"

Universities have access to most of the underlying data. QILT scores are public. Job vacancy data is on the Jobs and Skills Australia website. Google Trends is free. So why do they need us?

**The value isn't the data — it's the joins.**

### What universities typically have

| Capability | Status |
|---|---|
| Their own QILT scores and rankings | Yes — they receive these annually |
| Basic Google Analytics on their website | Yes — standard marketing stack |
| General awareness of job market trends | Yes — from industry news and employer relationships |
| Their own enrolment and application data | Yes — from their admissions system |

### What they don't have

| Capability | Why it's hard to build internally |
|---|---|
| **Opportunity gap quantification** — exact percentage gap between employer demand and student interest, by field | Requires joining IVI vacancy data (occupation-grain) to UAC/VTAC/SATAC preference data (field-grain) via a manually curated occupation-to-field crosswalk. Three different admissions centres use different field naming conventions. |
| **Competitive brand positioning** — how their search interest ranks against all 42 universities, by state | Requires systematic Google Trends collection for all 42 institutions across 8 states, normalised and joined to QILT quality rankings. A one-off manual check is possible; continuous monitoring isn't. |
| **LGA-level geo-targeting** — which specific local government areas have the highest youth density for campaign targeting | Requires ABS population data at LGA grain, joined to state-level demand data and institutional catchment analysis. Marketing teams typically target at postcode or state level because the LGA data is buried in ABS TableBuilder. |
| **Field-specific audience profiles** — gender skew, mature learner affinity, and interstate draw ratio for each field | Requires combining UAC gender breakdowns, applicant-type segmentation (Year 12 vs Non-Year 12 vs Interstate), and preference ratios across three admissions centres. No single source provides this view. |
| **Cross-source proof points** — a single brief that combines employment rates, salaries, vacancy growth, student satisfaction, and demand gaps for a specific field at a specific institution | Requires joining QILT (institution × field), IVI (occupation × state), UAC (field × gender × applicant type), and CRICOS (institution × campus × course) into one coherent narrative. This is a 4-source join that nobody maintains internally. |

### The real barrier

The data is public. The problem is that it lives in **8 different systems with 5 different classification schemes**:

- ANZSCO occupation codes (IVI job vacancies)
- UAC broad fields of study (NSW/ACT preferences)
- ASCED field codes (CRICOS course register)
- QILT study areas (graduate outcomes)
- ABS geographic codes (population data)

Mapping between these systems — and keeping those mappings current — is the unglamorous infrastructure work that makes cross-source analysis possible. A university marketing team could build this, but it would take months and isn't their core competency. We maintain the crosswalks, run the joins, and deliver the insights ready to act on.

## What they get from us

1. **Speed** — A complete marketing intelligence brief for any university in hours, not months
2. **Breadth** — Every field, every state, every competitor in one place, updated regularly
3. **Specificity** — Not "Health is growing" but "Health has a +10.2% opportunity gap, 87% employment, $78K salary, and your Bachelor of Nursing at your Wollongong campus is in the top-opportunity tier — target career-changer women 25-40 in the ACT corridor where your brand is already strongest"
4. **Objectivity** — Third-party data means the recommendations aren't influenced by internal politics about which faculty gets marketing budget

## Example output

See the [University of Wollongong example brief](example-brief-uow.md) for a real demonstration of the marketing intelligence we produce from 8 public data sources.

## Related

- [Use Cases](use-cases.md) — the 7 campaign and planning decisions Zeus supports
- [Data Sources](use-cases.md#data-sources) — the 8 government and public sources we combine
