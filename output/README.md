# Episode Output Folder

This folder is generated from `control_table.csv` in queue order so the project can reproduce episodes one by one from the top of the list.

## What is here

- `episodes/`: one folder per control-table row with a guide, extracted R script, and manifest
- `reproduction_index.csv`: flat queue summary for automation and review

## Current status counts

- `ready_local`: 63
- `ready_with_external_steps`: 5
- `needs_external_sources`: 11
- `needs_data_review`: 1
- `blocked_*`: 311

## First episodes in queue

- `1` `api_specs` -> `blocked_needs_mapping`
- `2` `adoptable_dogs` -> `blocked_needs_mapping`
- `3` `african_farmer_led_irrigation_survey` -> `blocked_needs_mapping`
- `4` `african_language_sentiment` -> `blocked_needs_mapping`
- `5` `african_american_achievements` -> `ready_with_external_steps`
- `6` `african_american_history` -> `ready_local`
- `7` `agencies_from_the_fbi_crime_data_api` -> `blocked_needs_mapping`
- `8` `agricultural_production_statistics_in_new_zealand` -> `blocked_needs_mapping`
- `9` `allrecipes` -> `blocked_needs_mapping`
- `10` `alone_data` -> `blocked_needs_mapping`
