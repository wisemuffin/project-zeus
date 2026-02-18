# Trending Interests

> What's trending in Australia right now, and does it align with high-opportunity fields?

**Source models:** `trending_interests`, `stg_google_trends`
**Data sources:** Google Trends RSS feed (Australia), opportunity_gap mart

## How It Works

The `trending_interests` model takes the current top Google trending searches in Australia and:

1. **Classifies** each trend to a UAC field of study using keyword matching (best effort)
2. **Enriches** matched trends with the field's opportunity gap and vacancy growth
3. **Signals** whether the trend aligns with a high-opportunity field (positive gap) or low-opportunity field (negative gap)

This model refreshes each time the `google_trends` Dagster asset is re-materialized. It's a snapshot, not a time series.

## Current Snapshot (2026-02-18)

| Trend | Traffic | Matched Field | Opp. Gap | Signal |
|-------|---------|--------------|----------|--------|
| atlassian | 200+ | Information Technology | +7.2pp | High opportunity |
| claude | 1000+ | Information Technology | +7.2pp | High opportunity |
| nab share price | 200+ | Management & Commerce | +4.4pp | High opportunity |
| j cole tickets | 2000+ | Creative Arts | -3.8pp | Low opportunity |
| pixel 10a | 200+ | — | — | Review manually |
| ticketek | 2000+ | — | — | Review manually |
| rugby world cup | 1000+ | — | — | Review manually |
| alysa liu | 200+ | — | — | Review manually |
| morgan evans | 200+ | — | — | Review manually |
| benfica | 500+ | — | — | Review manually |

## Actionable Takeaways

### Today's high-opportunity hooks

- **Atlassian hiring freeze** (trending) + **IT opportunity gap** (+7.2pp): "Tech companies are restructuring — but IT job demand still outpaces student interest 3:1. Future-proof your career with an IT degree."
- **Claude / AI launch** (trending, 1000+ traffic) + **IT opportunity gap**: "AI is transforming every industry. Be the one building it, not just using it."
- **NAB share price / banking results** (trending) + **Management & Commerce gap** (+4.4pp): "Australia's banks are posting record profits. Business and finance careers are booming."

### Low-opportunity — don't chase

- **J Cole tickets** (2000+ traffic, Creative Arts): High traffic but Creative Arts has a -3.8pp gap (more student interest than jobs). Don't invest ad spend here.

## How to Use This Model

1. **Materialise `google_trends`** in Dagster to refresh the RSS feed
2. **Materialise `trending_interests`** to re-classify and enrich
3. **Scan the output** for "High opportunity" signals
4. **Draft timely ad creative** referencing the trending topic + career outcomes data
5. **Deploy ads within 24-48 hours** while the trend is still relevant

## Limitations

- **Keyword matching is best effort** — many trends (sports, entertainment, people's names) won't match any field. These require manual review.
- **Ephemeral data** — trends change multiple times per day. The model captures a single snapshot per materialization.
- **No historical accumulation** — each refresh overwrites the previous snapshot. To track trends over time, the upstream asset would need to append rather than replace.
- **Classification gaps** — brand names (e.g. "pixel 10a" → should be IT) and indirect references are not captured by simple keyword matching. An LLM-based classifier could improve coverage.
