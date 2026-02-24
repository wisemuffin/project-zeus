---
title: Audience Density by LGA
---

LGA-level youth population (ages 15-19) for hyper-local geo-targeting of digital campaigns. Identifies specific Local Government Areas with the highest youth concentration within each state. Data sourced from the **Australian Bureau of Statistics** (Estimated Resident Population and ASGS LGA boundaries).

```sql total_lgas
select count(*) as total from zeus.audience_density_by_lga
```

```sql top_lga
select lga_name, state, youth_population
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
    value=lga_name
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
    lga_name,
    state,
    youth_population,
    youth_density_per_sqkm,
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
    tooltip={[{id: 'lga_name', showColumnName: false, valueClass: 'font-bold text-sm'}, {id: 'youth_population', fmt: 'num0'}, {id: 'youth_density_per_sqkm', title: 'Youth/km²', fmt: 'num1'}]}
/>

## Top LGAs by State

The cumulative share column shows how quickly youth population concentrates — e.g. if the top 20 LGAs in NSW cover 50% of the state's youth, campaigns can focus geo-targeting on those areas for efficient spend.

```sql density_table
select
    state,
    density_rank_in_state,
    cast(cast(lga_code as integer) as varchar) as lga_code,
    lga_name,
    youth_population,
    youth_density_per_sqkm,
    state_total,
    lga_share_of_state,
    cumulative_share
from zeus.audience_density_by_lga
order by state, density_rank_in_state
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
    <Column id=lga_name title="LGA Name" />
    <Column id=youth_population title="Youth Pop (15-19)" fmt=num0 />
    <Column id=youth_density_per_sqkm title="Youth/km²" fmt=num1 contentType=colorscale />
    <Column id=state_total title="State Total" fmt=num0 />
    <Column id=lga_share_of_state title="Share of State" fmt=pct1 contentType=colorscale />
    <Column id=cumulative_share title="Cumulative Share" fmt=pct1 />
</DataTable>

<Details title="Data Sources">

- **Estimated Resident Population by LGA** — Australian Bureau of Statistics (ABS). Annual population estimates for 15-19 year olds by Local Government Area (LGA). Most recent available year. All states and territories covered.
- **LGA Reference Data** — Australian Bureau of Statistics (ABS) ASGS 2024. LGA names, state mapping, and land area (Albers equal-area projection, km²) from the ABS MapServer API. Used for LGA name lookups and youth density per km² calculation.
- **Cumulative share** — running sum of youth population within each state ordered by population descending. Shows what percentage of the state's youth are covered by the top N LGAs.

</Details>
