# Search Data Options

Comparison of available providers for search/trend data relevant to understanding prospective student interest.

## Provider Comparison

| Provider | Cost | Data Type | Method | Best For |
|---|---|---|---|---|
| **trendspyg** (current) | Free | Trending searches | RSS feed | Real-time trending topic discovery |
| **Glimpse** | $29-99/mo | Keyword interest-over-time + absolute volume | API | Keyword-level demand analysis with actual search volumes |
| **Exploding Topics** | $249/mo | Trending topic discovery | Web app / API | Identifying emerging topics before they peak |
| **pytrends** | Free | Google Trends data | Web scraping | *Not recommended — archived/unmaintained* |
| **Google Trends API** | Free (alpha) | Trends data | Official API | Official access, but limited endpoints |

## Detailed Notes

### trendspyg (current)

- **What it does**: Fetches Google Trends RSS feed for trending searches
- **Pros**: Free, fast (~0.2s), no authentication, reliable RSS-based
- **Cons**: Only returns current trending topics (~10-20); no keyword lookup or historical interest-over-time data
- **Use case**: Discovering what's trending right now in Australia

### Glimpse

- **What it does**: Google Trends overlay that adds absolute search volume numbers and forecasting
- **Pros**: Real search volume numbers (not just relative index), keyword-level lookups, trend forecasting, API access
- **Cons**: Paid ($29/mo Starter, $99/mo Pro), requires account
- **Use case**: "How many people search for 'nursing degree' per month?" with trend direction
- **URL**: https://meetglimpse.com

### Exploding Topics

- **What it does**: Identifies topics with rapidly growing search interest
- **Pros**: Good at surfacing emerging trends before they become mainstream
- **Cons**: Expensive ($249/mo Pro), more of a discovery tool than an analytics data source
- **Use case**: Identifying emerging fields of study or career interest areas
- **URL**: https://explodingtopics.com

### pytrends (not recommended)

- **What it does**: Unofficial Python library for Google Trends
- **Pros**: Free, returns interest-over-time data for specific keywords
- **Cons**: Archived/unmaintained, relies on scraping Google Trends web UI, frequently breaks when Google changes their page structure
- **Status**: The repo is archived. Should not be used for new projects.

### Google Trends API (official)

- **What it does**: Official Google API for Trends data
- **Pros**: Official, maintained by Google
- **Cons**: Currently in alpha/limited access, restricted endpoint coverage
- **Status**: Worth monitoring for future availability

## Recommendation

For the current project phase, **trendspyg** provides a free, reliable baseline for trending topic discovery. If keyword-level interest-over-time data becomes important (e.g., tracking search volume for specific course names), **Glimpse** at $29/mo would be the most cost-effective upgrade.
