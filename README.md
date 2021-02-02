# anc-covid-equity
This project aims to plot COVID-19 associated cases, hospitalizations, and deaths normalized by population for different demographics in Alaska.


## Data

### COVID-19-associated cases, hospitalizations, and deaths

These data are drawn from the Alaska DHSS data hub. This data is requeried whenever the notebook is run. The API is here:
https://coronavirus-response-alaska-dhss.hub.arcgis.com/datasets/table-3-demographic-distribution-of-confirmed-cases/geoservice

### Race and ethnicity population data from AKDLWD

Race and ethnicity population data is from spreadsheets presented on this page: https://live.laborstats.alaska.gov/pop/

>"These data were developed through a combination of estimates from the Alaska Department of Labor and Workforce Development, and the U.S. Census Bureau. Sources: Alaska Department of Labor and Workforce Development, Research and Analysis Section; and U.S. Census Bureau"

## Notes and Cautions
Care should be taken when drawing conclusions directly from the data presented here. The COVID-19-associated data and population data are taken from different sources, and can be affected by how the same people identified to each data source. In particular, caution should be used when drawing conclusions from relatively small populations, where errors or lack of accurate data can be magnified in population-normalized rates.

### Ethnicity
- "Hispanic or Latino" is an ethnicity, so that demographic will have overlap with racial demographics (e.g, one can be "white hispanic").
- There are >20,000 cases where the ethnicity is listed as "Under Investigation", which is nearly the same amount the total number of non-hispanic cases reported, so care should be taken to interpret these humbers.

### Race
- There are ~9,500 cases were race is listed as "Under Investigation" or "Unknown". This may indicate disparaties in how race data is or is not collected across data providers. But these large categories could affect the charts unless these cases are understood or can be accounted for.
- "Other Race" as a category appears unreliable. According to the US Census there are ~12,000 people who identified as "other", but the case data shows ~6,000 cases of people identify as other. If this were true, ~50% of people identifying as a race other than those listed would have gotten COVID but with 0 deaths, an unlikely result. This may be a disparity in how people identified themselves to a testing center vs how they identified themselves to the census.