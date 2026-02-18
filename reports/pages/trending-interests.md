---
title: Trending Interests
---

Australian Google Trends matched to fields of study, enriched with opportunity gap context. Use this to identify timely content hooks and align paid media with what prospective students are searching for right now.

```sql classified_count
select count(*) as total from zeus.trending_interests where matched_field_of_study is not null
```

```sql total_count
select count(*) as total from zeus.trending_interests
```

```sql high_opp_count
select count(*) as total from zeus.trending_interests where marketing_signal like '%High opportunity%'
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
    rows=all
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
    rows=all
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

<Details title="Data Sources">

- **Google Trends (Trending Searches)** — real-time trending search topics for Australia, collected via the trendspyg RSS feed. Refreshed on each pipeline run.
- **Opportunity gap context** — derived from the Internet Vacancy Index (Jobs and Skills Australia) and UAC preference data via the opportunity_gap mart.
- **Note:** field-of-study matching uses keyword patterns and may not capture all relevant trends. Unmatched trends appear in the "All Trends" table for manual review.

</Details>
