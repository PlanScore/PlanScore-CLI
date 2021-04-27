# PlanScore Command-Line Client

Simple client for interacting with
[PlanScore’s experimental web API](https://github.com/PlanScore/PlanScore/blob/main/API.md).

## Install

PlanScore CLI is available from Python’s package index:

    pip install PlanScore-CLI

## Run

Score a single plan:

    planscore-client <API token> <Input GeoJSON> <Output JSON>

See [API Sample Request](https://github.com/PlanScore/PlanScore/blob/main/API.md#sample-request)
for details on input GeoJSON formating.
See [API Sample Response](https://github.com/PlanScore/PlanScore/blob/main/API.md#sample-response)
for details on output JSON content.

## Advanced Use

Score many plans in parallel with
[GNU Parallel](https://www.gnu.org/software/parallel/).
Example plans in `ok-example` have been exported from
[Dave’s Redistricting App](https://davesredistricting.org/)
samples linked from
[Oklahoma Senate Redistricting Page](https://oksenate.gov/redistricting)
on April 27, 2021:

    parallel -j9 planscore-client <API token> '{}' '{//}/score-{/.}.json' \
        ::: `ls -1 ok-example/*geojson`

- [Public map submission 1](https://davesredistricting.org/join/a2e3fded-03e3-4bca-86c4-379292dfe868) → [PlanScore result 1](https://planscore.org/plan.html?20210427T184121.456477833Z)
- [Public map submission 2](https://davesredistricting.org/join/31484a7b-7e07-47c5-bc10-71072d146ed3) → [PlanScore result 2](https://planscore.org/plan.html?20210427T184121.544097162Z)
- [Public map submission 3](https://davesredistricting.org/join/eaf8e83c-f74f-46bd-becf-380015d6cc95) → [PlanScore result 3](https://planscore.org/plan.html?20210427T184123.327988546Z)
- [Public map submission 4](https://davesredistricting.org/join/9dea2ecc-0641-4dfc-8a26-60049563d760) → [PlanScore result 4](https://planscore.org/plan.html?20210427T184124.064910694Z)
- [Public map submission 5](https://davesredistricting.org/join/9ff06581-03d0-40b3-9fad-1650c9ed0b6c) → [PlanScore result 5](https://planscore.org/plan.html?20210427T184124.625762411Z)
- [Public map submission 6](https://davesredistricting.org/join/c9d59129-7125-4736-b263-346742a43ca5) → [PlanScore result 6](https://planscore.org/plan.html?20210427T184124.150431235Z)
- [Public map submission 7](https://davesredistricting.org/join/b00c96e5-da14-41e2-8955-1f6f336735af) → [PlanScore result 7](https://planscore.org/plan.html?20210427T184121.873422509Z)
- [Public map submission 8](https://davesredistricting.org/join/b01f51b2-960e-4466-be2b-0c6dd692bc37) → [PlanScore result 8](https://planscore.org/plan.html?20210427T184124.767846834Z)
- [Public map submission 9](https://davesredistricting.org/join/42d8a2ee-5a21-463a-b3e8-5c2a3c76251a) → [PlanScore result 9](https://planscore.org/plan.html?20210427T184121.689257791Z)
