# Integration Strategy: Stay Upstream of Execution

> **Decision:** Project Zeus does not integrate with university systems (ad platforms, websites, CRMs). We are the intelligence layer that tells universities *what to do*. Their existing tools handle *doing it*.

## Why not integrate?

The product's biggest sales advantage is that **it works without any university cooperation**. We can generate a complete marketing intelligence brief for any of the 42 Australian universities using only public data. That means:

- **Zero onboarding friction** — no IT security review, no data sharing agreement, no 3-month procurement cycle
- **Instant demo** — we can show a prospect their own data before they've signed anything
- **No dependency on their tech maturity** — some universities have sophisticated martech stacks, some run campaigns from spreadsheets. We work for both.

The moment we require access to a university's Google Ads account or website analytics, we lose all three.

## Integrations we considered

| Integration | What it would add | Why we're not doing it |
|---|---|---|
| **Google Ads / Meta Ads** | Measure if recommendations convert; auto-create audience segments | Every university's account is structured differently. We become an ad ops tool competing with agencies, not an intelligence product. |
| **Website analytics** (GA4) | Validate brand awareness findings with real traffic data | Universities already have Google Analytics. We'd be duplicating what they have, not adding what they lack. |
| **CRM / admissions system** | Close the loop — did the campaign actually drive applications? | Involves student PII, requires security reviews, 6-month sales cycles, and every university uses a different CRM (Salesforce, Microsoft Dynamics, home-grown). |
| **Course finder / CMS** | Push recommended programs to homepage dynamically | CMS integration across 42 different university websites is a platform engineering problem, not a data problem. |

## What we do instead

We deliver intelligence in formats that universities can act on with their existing tools:

1. **Dashboards** — Interactive Evidence.dev reports that marketing teams can explore and screenshot for internal presentations
2. **Briefs** — Narrative marketing intelligence documents with specific campaign recommendations (see [UOW example](example-brief-uow.md))
3. **Export-ready targeting data** — LGA postcodes, audience segments, and field prioritisation that can be imported into any ad platform as CSV

## Future lightweight options

If customer demand justifies it, these are the lowest-friction integrations we'd consider — all of which keep us as the intelligence layer:

| Option | Effort | What it enables |
|---|---|---|
| **Audience list exports** (CSV of postcodes + targeting parameters) | Low | Universities import into Google Ads / Meta themselves |
| **UTM templates** per campaign recommendation | Low | Universities track which Zeus-recommended campaigns converted, without us touching their analytics |
| **API / data feed** | Medium | Larger universities pull Zeus data into their own BI tools (Power BI, Tableau) |
| **Looker Studio connector** | Medium | Universities who live in Google's ecosystem can pull Zeus metrics alongside their own GA4 data |

None of these require access to university systems. We push data out; they pull it in.

## The principle

**Public data in, actionable intelligence out.** No logins, no credentials, no PII, no integration projects. A university should be able to go from "never heard of us" to "looking at their own marketing brief" in a single meeting.
