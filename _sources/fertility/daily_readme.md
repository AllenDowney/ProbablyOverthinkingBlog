# Median income or consumption per day - Data package

This data package contains the data that powers the chart ["Median income or consumption per day"](https://ourworldindata.org/grapher/daily-median-income?v=1&csvType=full&useColumnShortNames=false) on the Our World in Data website. It was downloaded on June 9, 2026.

### Active Filters

A filtered subset of the full data was downloaded. The following filters were applied:

## CSV Structure

The high level structure of the CSV file is that each row is an observation for an entity (usually a country or region) and a timepoint (usually a year).

The first two columns in the CSV file are "Entity" and "Code". "Entity" is the name of the entity (e.g. "United States"). "Code" is the OWID internal entity code that we use if the entity is a country or region. For most countries, this is the same as the [iso alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) code of the entity (e.g. "USA") - for non-standard countries like historical countries these are custom codes.

The third column is either "Year" or "Day". If the data is annual, this is "Year" and contains only the year as an integer. If the column is "Day", the column contains a date string in the form "YYYY-MM-DD".

The final column is the data column, which is the time series that powers the chart. If the CSV data is downloaded using the "full data" option, then the column corresponds to the time series below. If the CSV data is downloaded using the "only selected data visible in the chart" option then the data column is transformed depending on the chart type and thus the association with the time series might not be as straightforward.


## Metadata.json structure

The .metadata.json file contains metadata about the data package. The "charts" key contains information to recreate the chart, like the title, subtitle etc.. The "columns" key contains information about each of the columns in the csv, like the unit, timespan covered, citation for the data etc..

## About the data

Our World in Data is almost never the original producer of the data - almost all of the data we use has been compiled by others. If you want to re-use data, it is your responsibility to ensure that you adhere to the sources' license and to credit them correctly. Please note that a single time series may have more than one source - e.g. when we stich together data from different time periods by different producers or when we calculate per capita metrics using population data from a second source.

## Detailed information about the data


## Median
Value of income or consumption per day below which 50% of the population live.
Last updated: March 24, 2026  
Next update: September 2026  
Date range: 1963–2026  
Unit: international-$ in 2021 prices  


### How to cite this data

#### In-line citation
If you have limited space (e.g. in data visualizations), you can use this abbreviated in-line citation:  
World Bank Poverty and Inequality Platform (2026) – with major processing by Our World in Data

#### Full citation
World Bank Poverty and Inequality Platform (2026) – with major processing by Our World in Data. “Median – World Bank” [dataset]. World Bank Poverty and Inequality Platform, “World Bank Poverty and Inequality Platform (PIP) 20260324_2021, 20260324_2017” [original data].
Source: World Bank Poverty and Inequality Platform (2026) – with major processing by Our World In Data

### What you should know about this data
* This data shows the median income or consumption per person — the level below which half the population falls. Unlike the mean, the median is not pulled up by the incomes of the richest, so it better reflects what a typical person has. We discuss how incomes are distributed in more detail on our page on [economic inequality](https://ourworldindata.org/economic-inequality).
* This data is expressed in constant international dollars to adjust for inflation and differences in living costs between countries. Read more in our article, [What are international dollars?](https://ourworldindata.org/international-dollars)
* Depending on the country and year, the data refers either to income (after taxes and benefits) or to consumption, [per capita](#dod:per-capita). These are not perfectly comparable — consumption tends to be more evenly distributed than income. For most countries, we have only one option available. But when there is a mix of consumption and income data points, we process the data to keep one observation per country and year.
* Many people, today and in the past, have no formal monetary income. This data accounts for that by including the estimated value of non-market income, such as food grown by subsistence farmers for their own use.
* The data comes from the World Bank's Poverty and Inequality Platform (PIP), which draws on national household surveys. Regional and global estimates are extrapolated to the year of the data release using GDP growth estimates and forecasts. For more details about the methodology, please refer to the [World Bank PIP documentation](https://datanalytics.worldbank.org/PIP-Methodology/lineupestimates.html#nowcasts).

### How is this data described by its producer - World Bank Poverty and Inequality Platform (2026)?
The median of monthly household per capita income or consumption expenditure from the survey in 2021 PPP.

### Source

#### World Bank Poverty and Inequality Platform – World Bank Poverty and Inequality Platform (PIP)
Retrieved on: 2026-03-24  
Retrieved from: https://pip.worldbank.org  

#### Notes on our processing step for this indicator
For most countries in the dataset, estimates relate to disposable income or consumption, for all available years. Several countries, however, have a mix of income and consumption data points, with both data types sometimes available for particular years.

In most of our charts, we present the data with some data points dropped to present a single series for each country. This allows us to make readable visualizations that combine multiple countries. In choosing which data points to keep, we strike a balance between maintaining comparability over time and showing as long a time series as possible. As such, the exact approach varies across countries.


    