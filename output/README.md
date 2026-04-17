# Episode Output Folder

This folder is generated from `control_table.csv` in queue order so the project can reproduce episodes one by one from the top of the list.

## What is here

- `episodes/`: one folder per control-table row with a guide, extracted R script, and manifest
- `reproduction_index.csv`: flat queue summary for automation and review

## Current status counts

- `ready_local`: 57
- `ready_with_external_steps`: 5
- `needs_external_sources`: 16
- `needs_data_review`: 1
- `blocked_*`: 1

## First episodes in queue

- `1` `african_american_achievements` -> `ready_with_external_steps`
- `2` `african_american_history` -> `ready_local`
- `3` `predicting_horror_movie_ratings` -> `ready_local`
- `4` `animal_crossing` -> `ready_local`
- `5` `art_collections` -> `ready_local`
- `6` `australian_animal_outcomes` -> `ready_with_external_steps`
- `7` `beach_volleyball` -> `ready_local`
- `8` `beyonce_taylor_swift_lyrics` -> `ready_local`
- `9` `bike_frequencies_seattle` -> `ready_local`
- `10` `bird_collisions_bootstrapping` -> `ready_local`
