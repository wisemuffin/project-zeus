# Google Trends Data (Trending Searches)

## Overview

Trending Google searches in Australia via RSS feed. Provides real-time demand signals — what topics and queries are currently trending. Useful for identifying emerging interest areas and timely content opportunities.

## Data Source

| Field | Value |
|---|---|
| Provider | Google Trends (via `trendspyg` library) |
| Method | RSS feed parsing |
| Geo | `AU` (Australia) |
| Auth | None |
| Rate limits | Cached for 5 minutes by default |
| Latency | ~0.2s (no browser automation needed) |

## Data Contents

- **Trending topic titles** — current trending search terms
- **Traffic volume** — approximate search volume
- **News articles** — related headlines and URLs
- **Article images** — thumbnail images for each trend
- **Publication timestamps** — when the trend was detected

## How It Works

The `trendspyg` library fetches Google Trends RSS feeds, which provide ~10-20 currently trending topics. Unlike the deprecated `pytrends` (which scraped the web UI), this uses the official RSS endpoint and is fast and reliable.

## Limitations

- **Current trends only**: RSS returns what's trending right now; no historical time-series data
- **No keyword lookup**: Cannot query interest for specific terms (use Glimpse or Google Trends API for that)
- **~10-20 results**: Returns a small number of top trending topics, not comprehensive search data
- **General trends**: Not filtered to education/university topics specifically

See [Search Data Options](search-data-options.md) for alternatives that provide keyword-level interest-over-time data.

## Asset

- **Key**: `google_trends`
- **Group**: `google_trends`
- **Tags**: `source:google`, `domain:search_interest`
- **File**: `analytics/src/analytics/defs/assets/google_trends.py`
