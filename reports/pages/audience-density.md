---
title: Audience Density by LGA
---

LGA-level youth population (ages 15-19) for hyper-local geo-targeting of digital campaigns. Identifies specific Local Government Areas with the highest youth concentration within each state. Data sourced from the **Australian Bureau of Statistics** (Estimated Resident Population by LGA).

```sql total_lgas
select count(*) as total from zeus.audience_density_by_lga
```

```sql top_lga
select lga_code, state, youth_population
from zeus.audience_density_by_lga
where youth_population = (select max(youth_population) from zeus.audience_density_by_lga)
```

```sql states_covered
select count(distinct state) as total from zeus.audience_density_by_lga
```

<BigValue
    data={total_lgas}
    value=total
    title="Total LGAs"
/>
<BigValue
    data={top_lga}
    value=lga_code
    title="Top LGA (Highest Youth Pop)"
/>
<BigValue
    data={top_lga}
    value=youth_population
    title="Youth Population"
    fmt=num0
/>

## Youth Population by LGA

```sql map_data
select
    cast(cast(lga_code as integer) as varchar) as lga_code_str,
    lga_code,
    state,
    youth_population,
    lga_share_of_state
from zeus.audience_density_by_lga
```

<AreaMap
    data={map_data}
    geoJsonUrl="/au_lga_2024_gen.geojson"
    geoId="lga_code_2024"
    areaCol="lga_code_str"
    value="youth_population"
    height=500
    startingLat={-28}
    startingLong={134}
    startingZoom={4}
    legendType="scalar"
    title="Youth Population (15-19) by LGA"
/>

## Top LGAs by State

The cumulative share column shows how quickly youth population concentrates — e.g. if the top 20 LGAs in NSW cover 50% of the state's youth, campaigns can focus geo-targeting on those areas for efficient spend.

```sql density_table
select * from zeus.audience_density_by_lga order by state, density_rank_in_state
```

<DataTable
    data={density_table}
    rows=all
    rowShading=true
    search=true
>
    <Column id=state title="State" />
    <Column id=density_rank_in_state title="Rank in State" />
    <Column id=lga_code title="LGA Code" />
    <Column id=youth_population title="Youth Pop (15-19)" fmt=num0 />
    <Column id=state_total title="State Total" fmt=num0 />
    <Column id=lga_share_of_state title="Share of State" fmt=pct1 contentType=colorscale />
    <Column id=cumulative_share title="Cumulative Share" fmt=pct1 />
</DataTable>

<Details title="Data Sources">

- **Estimated Resident Population by LGA** — Australian Bureau of Statistics (ABS). Annual population estimates for 15-19 year olds by Local Government Area (LGA). Most recent available year. All states and territories covered.
- **State mapping** — derived from LGA code first digit (1=NSW, 2=VIC, 3=QLD, 4=SA, 5=WA, 6=TAS, 7=NT, 8=ACT). LGA codes that don't map to a known state are excluded.
- **Cumulative share** — running sum of youth population within each state ordered by population descending. Shows what percentage of the state's youth are covered by the top N LGAs.

</Details>
