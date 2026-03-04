# Project Zeus — Financial Model

> **Last updated:** 2026-03-04
> **Status:** Draft — pre-revenue planning model

## Assumptions

| Assumption | Value | Notes |
|---|---|---|
| Average pilot price | $20,000 | 6-month engagement, under procurement threshold |
| Average annual subscription | $40,000 | Post-pilot conversion, per university |
| One-off brief (paid) | $7,500 | For universities not ready for a pilot |
| Pilot-to-annual conversion rate | 50% | Conservative — if the pilot works, budget pressure makes renewal likely |
| Sales cycle (cold to signed pilot) | 3 months | Based on Phase 1 sales strategy timeline |
| Churn rate (annual subscribers) | 20% | Assume 1 in 5 don't renew in year 1 |

## Cost Structure

Project Zeus runs on open-source infrastructure with free government data. The
primary costs are time and a small amount of hosting.

### Fixed Monthly Costs

| Item | Monthly Cost | Annual Cost | Notes |
|---|---|---|---|
| Evidence.dev hosting (Netlify/Vercel) | $20 | $240 | Static site hosting, free tier likely sufficient for 1-5 clients |
| Domain + email | $15 | $180 | Professional email for outreach |
| LinkedIn Premium (Sales Navigator) | $100 | $1,200 | Essential for Phase 1 outreach |
| Dagster Cloud (optional) | $0–$100 | $0–$1,200 | Free tier may suffice; self-hosted alternative is $0 |
| Google Workspace | $10 | $120 | Docs, calendar, invoicing |
| Professional indemnity insurance | $100–$200 | $1,200–$2,400 | Required by most universities for contracted services |
| Accounting software (Xero) | $30 | $360 | Invoicing, BAS, bookkeeping |
| **Total fixed costs** | **$275–$475** | **$3,300–$5,700** | |

### Variable Costs

| Item | Cost | Trigger |
|---|---|---|
| Accountant (BAS + tax return) | $2,000–$4,000/year | Quarterly BAS if registered for GST |
| Legal (contract review) | $2,000–$5,000 one-off | Initial service agreement drafting |
| Conference attendance (ATEM, EPHEA) | $500–$1,500 per event | Phase 2 — after pilot validation |
| Pty Ltd registration | $538 (ASIC) | One-off company setup |
| Travel (client walkthroughs) | $200–$500 per trip | If in-person demos required |

### One-Off Setup Costs

| Item | Cost |
|---|---|
| ASIC company registration | $538 |
| Legal — service agreement template | $2,000–$5,000 |
| Professional indemnity insurance (first year) | $1,200–$2,400 |
| Branding / logo (optional) | $0–$500 |
| **Total setup** | **$3,738–$8,438** |

## Revenue Scenarios (Year 1)

Year 1 starts from first signed pilot. Assumes 12-week sales cycle per cohort.

### Scenario A: Conservative (1 pilot, slow growth)

| Quarter | Activity | Revenue |
|---|---|---|
| Q1 | 1 pilot signed | $10,000 (half of $20K pilot, paid upfront) |
| Q2 | Pilot delivery + 1 new pilot | $10,000 + $10,000 |
| Q3 | First pilot converts to annual; 1 new pilot | $20,000 + $10,000 |
| Q4 | 2 annual subscribers; 1 new pilot | $10,000 |
| **Year 1 total** | **2 pilots → 1 annual subscriber** | **$70,000** |

Annual costs: ~$5,000 fixed + $4,000 variable = **$9,000**
**Net: ~$61,000** (before tax, before founder time)

### Scenario B: Base Case (2 pilots in Q1, steady growth)

| Quarter | Activity | Revenue |
|---|---|---|
| Q1 | 2 pilots signed | $20,000 |
| Q2 | Pilot delivery + 2 new pilots | $20,000 |
| Q3 | 2 pilots convert to annual; 2 new pilots | $40,000 + $20,000 |
| Q4 | 4 annual subscribers; 1 new pilot | $20,000 + $10,000 |
| **Year 1 total** | **6 pilots → 4 annual subscribers** | **$130,000** |

Annual costs: ~$5,000 fixed + $6,000 variable = **$11,000**
**Net: ~$119,000** (before tax, before founder time)

### Scenario C: Optimistic (fast traction, agency channel opens)

| Quarter | Activity | Revenue |
|---|---|---|
| Q1 | 3 pilots signed | $30,000 |
| Q2 | Delivery + 3 new pilots + 1 paid brief | $30,000 + $7,500 |
| Q3 | 3 convert to annual; 3 new pilots; 1 agency deal | $60,000 + $30,000 + $15,000 |
| Q4 | 6 annual; 2 new pilots; agency expanding | $30,000 + $20,000 |
| **Year 1 total** | **11 engagements → 6 annual + 1 agency** | **$222,500** |

Annual costs: ~$5,700 fixed + $10,000 variable = **$15,700**
**Net: ~$206,800** (before tax, before founder time)

## Break-Even Analysis

With monthly fixed costs of ~$400 and no salary:

- **Break-even on costs:** 1 pilot covers a full year of operating costs
- **Break-even as a liveable income ($100K/year):** Requires ~3 annual subscribers
  ($120K) or 5 pilots ($100K)
- **Break-even with a hire ($200K total comp):** Requires ~6 annual subscribers
  ($240K) — likely a Year 2/3 milestone

## Key Decision: Revenue Model

The business plan lists three options. This model assumes **Option B (Insights-as-a-Service)** transitioning to **Option A (SaaS Subscription)** as the product matures.

| Phase | Model | Why |
|---|---|---|
| Phase 1 (now) | Insights-as-a-Service | Lower product maturity needed; human narrative is the differentiator; justifies pilot pricing |
| Phase 2 (5+ customers) | Hybrid — self-service dashboards + quarterly briefs | Dashboard access is the recurring value; briefs are the premium layer |
| Phase 3 (10+ customers) | SaaS subscription + optional advisory | Scale requires self-service; advisory becomes an upsell, not the core product |

## Year 2–3 Outlook

| Metric | Year 2 (base case) | Year 3 (base case) |
|---|---|---|
| Annual subscribers | 8–12 | 15–20 |
| Annual revenue | $320K–$480K | $600K–$800K |
| First hire | Sales/account manager (~$120K) | Data analyst or second account manager |
| Agency channel revenue | $30K–$60K | $100K–$200K |
| Total addressable (realistic) | 43 universities + 20 agencies | + 50 non-university providers |

## Risks to the Model

| Risk | Impact | Mitigation |
|---|---|---|
| Pilots don't convert to annual | Revenue stays project-based, harder to plan | Build switching costs — integrate into their planning cycle, time renewals with budget season |
| Price is too low for perceived value | Universities don't take it seriously | Anchor against consulting rates ($50K+ for a comparable engagement); increase price if demand exceeds capacity |
| Price is too high for budget reality | Can't close pilots under frozen budgets | Offer a $5K "taster" brief as entry point; flexible payment terms |
| Single-founder bottleneck | Can't deliver + sell simultaneously | Automate brief generation further; hire an account manager before capacity is fully used |
| GST registration threshold | Must register at $75K revenue; adds admin | Register from day one to avoid retrospective compliance; use Xero for BAS |
