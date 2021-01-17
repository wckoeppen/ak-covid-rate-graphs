# anc-covid-equity
Looking for a graph that has the Deaths, Hospitalizations, and Cases normalized (or shown along with) population for different demographics in Alaska. Ideally the graph can be added to a cron job to keep it up to date.


## Data
There is downloadable data and an API for geojson data here:
https://coronavirus-response-alaska-dhss.hub.arcgis.com/datasets/table-3-demographic-distribution-of-confirmed-cases/geoservice

## Resources
Shannon Kuhn forwarded an email from Charles Fletcher with:
- [Summary Table](https://docs.google.com/presentation/d/1z7hpueIPSHR613sia3cWWS-DGORzsCE9/edit?usp=drive_web&ouid=108065953973861860832&rtpof=true)
- [Sample data from Jan 12 2021](https://docs.google.com/spreadsheets/d/1TAxa1VKD5Sa8hlxvvZ5CHfl80-KnlcpK/edit?usp=drive_web&ouid=108065953973861860832&rtpof=true)

Population estimates for race and ethnicity groups were taken from the US Census - American Community Survey:
- [Race Data for AK](https://data.census.gov/cedsci/table?q=race&g=0400000US02&d=ACS%201-Year%20Estimates%20Detailed%20Tables&tid=ACSDT1Y2019.C02003&moe=true&hidePreview=true)
- [Hispanic Ethnicity data for AK](https://data.census.gov/cedsci/table?q=Race%20and%20Ethnicity&g=0400000US02&d=ACS%201-Year%20Estimates%20Detailed%20Tables&tid=ACSDT1Y2019.B03002&moe=true&hidePreview=true)
- a takeaway here is that "Hispanic" is an ethnicity (e.g, you can be "white hispanic"), and will have overlap with other races. There are also >20,000 cases where the ethnicity is listed as "under investigation", which is nearly the same amount of non-hispanic cases, so these numbers could have a huge error. I'm opposed to including it unless there's a justification to do so.

## Notes
- the "X Cases Percentage" is tricky, and represents the percent of people who have gotten COVID and identified themselves as a particular race. A more interesting statistic is the infection rate, which would be cases / population.
- "Other Race" is also strange, and seems unreliable. According to the US Census there are ~12,000 people who identified as other, but the case data shows ~6,000 cases of people identify as other. If this were true, ~50% of people identifying as a race other than those listed would have gotten COVID but with 0 deaths.