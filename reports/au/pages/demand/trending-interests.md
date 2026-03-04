---
title: Trending Interests
---

<span class="px-2 py-0.5 text-xs font-medium rounded-full bg-blue-100 text-blue-800">National</span>

Australian Google Trends matched to fields of study, enriched with opportunity gap context. Use this to identify timely content hooks and align paid media with what prospective students are searching for right now. See the [Trending Interests insight](/insights/trending-interests) for actionable ad hooks and the workflow for deploying timely campaigns.

```sql classified_count
select count(*) as total from zeus.trending_interests where matched_field_of_study is not null
```

```sql total_count
select count(*) as total from zeus.trending_interests
```

```sql high_opp_count
select count(*) as total from zeus.trending_interests where marketing_signal like '%High opportunity%'
```

```sql vintage_google_trends
select source_label || ' ' || data_period as subtitle
from zeus.freshness_vintage where source_key = 'google_trends'
```

<BigValue
    data={total_count}
    value=total
    title="Total Trends Tracked"
/>
<BigValue
    data={classified_count}
    value=total
    title="Matched to a Field of Study"
/>
<BigValue
    data={high_opp_count}
    value=total
    title="High Opportunity Signals"
/>

## Trends with Marketing Signals

Trends that matched a field of study, sorted by opportunity rank. High-opportunity trends align with fields where job demand outstrips student interest — prime candidates for timely ad creative.

```sql classified_trends
select
    trend,
    traffic,
    matched_field_of_study,
    opportunity_gap,
    opportunity_rank,
    vacancy_growth_12m,
    marketing_signal,
    top_article_headline,
    top_article_source
from zeus.trending_interests
where matched_field_of_study is not null
order by opportunity_rank, trend
```

<DataTable
    data={classified_trends}
    subtitle={vintage_google_trends[0].subtitle}
    rowShading=true
    search=true
>
    <Column id=trend title="Trend" />
    <Column id=traffic title="Traffic" />
    <Column id=matched_field_of_study title="Field of Study" />
    <Column id=marketing_signal title="Signal" />
    <Column id=opportunity_gap title="Opp Gap" fmt=pct1 />
    <Column id=vacancy_growth_12m title="Vacancy Growth" fmt=pct1 />
    <Column id=top_article_headline title="Top Article" />
    <Column id=top_article_source title="Source" />
</DataTable>

## Signal Distribution

How trending topics break down by marketing signal category.

```sql signal_dist
select
    marketing_signal,
    count(*) as trend_count
from zeus.trending_interests
group by marketing_signal
order by trend_count desc
```

<BarChart
    data={signal_dist}
    x=marketing_signal
    y=trend_count
    title="Trends by Marketing Signal"
    subtitle={vintage_google_trends[0].subtitle}
    xAxisTitle="Signal"
    yAxisTitle="Number of Trends"
    sort=false
/>

## All Trends

Full list including unclassified trends for manual review.

```sql all_trends
select
    trend,
    traffic,
    matched_field_of_study,
    marketing_signal,
    top_article_headline,
    top_article_source,
    published
from zeus.trending_interests
order by published desc
```

<DataTable
    data={all_trends}
    subtitle={vintage_google_trends[0].subtitle}
    rowShading=true
    search=true
>
    <Column id=trend title="Trend" />
    <Column id=traffic title="Traffic" />
    <Column id=matched_field_of_study title="Field of Study" />
    <Column id=marketing_signal title="Signal" />
    <Column id=top_article_headline title="Top Article" />
    <Column id=top_article_source title="Source" />
    <Column id=published title="Published" />
</DataTable>

```sql page_refreshed
select max(last_refreshed) as refreshed_at
from zeus.freshness_pipeline
where table_name in ('trending_interests')
```

<p style="color: #9ca3af; font-size: 0.75rem;">
Pipeline last refreshed: {fmt(page_refreshed[0].refreshed_at, 'd MMMM yyyy')}
</p>

<Details title="Data Sources">

- **Google Trends (Trending Searches)** — real-time trending search topics for Australia, collected via the trendspyg RSS feed. Refreshed on each pipeline run.
- **Opportunity gap context** — derived from the Internet Vacancy Index (Jobs and Skills Australia) and UAC preference data via the opportunity_gap mart.
- **Note:** field-of-study matching uses keyword patterns and may not capture all relevant trends. Unmatched trends appear in the "All Trends" table for manual review.

</Details>
