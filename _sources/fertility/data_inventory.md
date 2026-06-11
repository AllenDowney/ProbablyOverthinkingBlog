# Data Inventory: `notebooks/fertility`

This folder contains two Our World in Data (OWID) data packages, both downloaded on **June 9, 2026**. Each package includes a CSV dataset, a readme, and a metadata JSON file.

---

## Overview

| Dataset | CSV file | Readme | Metadata |
|---------|----------|--------|----------|
| Fertility rate | `children-born-per-woman.csv` | `children-born-per-woman-readme.md` | `children-born-per-woman.metadata.json` |
| Median daily income | `daily-median-income.csv` | `daily_readme.md` | `daily-median-income.metadata.json` |

Both datasets follow the standard OWID CSV structure:

- **Entity** — country or region name (e.g. "United States")
- **Code** — OWID internal code (usually ISO alpha-3, e.g. "USA"; blank for some subnational entities)
- **Year** — integer year
- **Value column** — the time series for that chart

No active filters were applied at download time (`activeFilters` is empty in both metadata files), but each chart had a default entity selection (listed below).

---

## 1. Fertility rate: births per woman

**Source chart:** [Fertility rate: births per woman](https://ourworldindata.org/grapher/children-born-per-woman?v=1&csvType=full&useColumnShortNames=false)

### CSV summary

| Property | Value |
|----------|-------|
| Rows | 19,402 |
| Entities | 261 |
| Year range | 1891–2023 |
| Columns | `Entity`, `Code`, `Year`, `Total fertility rate` |
| Missing values | None |

### Indicator

The **total fertility rate** is the average number of live births a hypothetical cohort of women would have over their reproductive lifetime if they experienced the age-specific fertility rates of a given period and were not subject to mortality.

- **Unit:** live births per woman
- **Assumption:** current age-specific fertility rates remain constant throughout a woman's lifetime
- **Limitation:** does not account for future changes in social, economic, or health conditions

### Data construction

OWID combines two sources:

- **Before 1950:** Human Fertility Database (2025)
- **1950–2023:** UN World Population Prospects (2024 revision)

### Metadata highlights

| Field | Value |
|-------|-------|
| OWID variable ID | 1118640 |
| Short name | `fertility_rate_hist` |
| Last updated | 2025-10-22 |
| Next update | 2026-10-22 |

**Chart selection (default entities):** World, United States, United Kingdom, Russia, Germany, Japan, India

### Citation

> Human Fertility Database (2025); UN, World Population Prospects (2024) – with major processing by Our World in Data

**Original sources:**

- [Human Fertility Database](https://www.humanfertility.org/Home/Index) (retrieved 2025-10-22)
- [UN World Population Prospects](https://population.un.org/wpp/downloads/) (retrieved 2024-07-11)
- UN World Population Prospects – Interim Update (retrieved 2026-03-31)

---

## 2. Median income or consumption per day

**Source chart:** [Median income or consumption per day](https://ourworldindata.org/grapher/daily-median-income?v=1&csvType=full&useColumnShortNames=false)

### CSV summary

| Property | Value |
|----------|-------|
| Rows | 2,759 |
| Entities | 193 |
| Year range | 1963–2026 |
| Columns | `Entity`, `Code`, `Year`, `Median` |
| Missing values | None |

### Indicator

The **median** is the daily income or consumption level below which 50% of the population falls. Unlike the mean, it is not pulled upward by the richest households.

- **Unit:** international-$ in 2021 prices (constant, PPP-adjusted)
- **Short unit:** $
- **Per:** capita, per day
- **Mix of measures:** depending on country and year, values may reflect disposable income (after taxes and benefits) or consumption; OWID consolidates to one observation per country-year where both exist
- **Non-market income:** includes estimated value of subsistence production (e.g. food grown for own use)

### Data construction

Source is the World Bank Poverty and Inequality Platform (PIP), based on national household surveys. Regional and global estimates are extrapolated using GDP growth estimates and forecasts. OWID drops some overlapping income/consumption data points to produce a single readable series per country, with the exact approach varying by country.

### Metadata highlights

| Field | Value |
|-------|-------|
| OWID variable ID | 1214969 |
| Short name | `median__ppp_version_2021__welfare_type_income_or_consumption__period_day__table_income_or_consumption_consolidated__survey_comparability_no_spells` |
| Last updated | 2026-03-24 |
| Next update | 2026-09-20 |

**Chart selection (default entities):** World, United States, South Korea, Spain, China, Mauritania, Ghana, India, Ethiopia, Democratic Republic of Congo

### Citation

> World Bank Poverty and Inequality Platform (2026) – with major processing by Our World in Data

**Original source:**

- [World Bank PIP](https://pip.worldbank.org) — PIP release 20260324_2021, 20260324_2017 (retrieved 2026-03-24)

---

## File reference

```
notebooks/fertility/
├── children-born-per-woman.csv
├── children-born-per-woman-readme.md
├── children-born-per-woman.metadata.json
├── daily-median-income.csv
├── daily_readme.md
├── daily-median-income.metadata.json
└── data_inventory.md          # this file
```

## Usage notes

- Both datasets are **annual** (Year column, not Day).
- Entity codes are mostly ISO alpha-3; some entities (e.g. "Argentina (urban)") have blank codes.
- OWID is a compiler/processor, not the original data producer — check source licenses and cite appropriately when reusing.
- Full indicator metadata is available via the OWID API links in each `.metadata.json` file under `columns.<name>.fullMetadata`.
