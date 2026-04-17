# Function Repository Overview

This file is the entry point for the function-building effort in `sa-tidy-tuesday`.

## Purpose

- Explain how the repository tracks transcript intent, code mappings, dataset relationships, and reusable workflow signatures.
- Point to the main knowledge register and prompt pack.
- Describe the control-table-driven extraction workflow.

## Primary files

- `control_table.csv`
  - authoritative mapping of transcript titles, code files, function names, extraction metadata, and workflow status
- `knowledge register.md`
  - long-form knowledge register for intent, thought patterns, data transformations, and adaptation-ready workflows
- `prompts.md`
  - prompt pack for extracting reusable functions from transcript, code, and data relationships
- `R/screencast_intent_stubs.R`
  - generated R function stubs for every mapped episode
- `R/screencast_helpers.R`
  - shared helper functions used by episode implementations, including local-first TidyTuesday loading to avoid unnecessary GitHub PAT dependence
- `R/screencast_implementations.R`
  - actual implementations for selected episode functions
- `build_intent_stubs.ps1`
  - script to regenerate the stub file from `control_table.csv`
- `build_ker_entries.py`
  - batch builder that enriches `control_table.csv` and generates extracted episode entries in `knowledge register.md`
- `build_super_qmd.py`
  - generates a cognition-first "super QMD" that bridges an episode reproduction guide and a finished guided analysis document
- `R/intents.R`
  - R utilities for loading the control table and generating stubs from the enriched schema

## How to use this repo

1. Review `control_table.csv` to understand the existing transcript and code mappings.
2. Use `control_table.csv` as the row-level work queue for extraction and implementation.
3. Use `prompts.md` to run the master `Thought -> Code -> Data` extraction prompt for each row.
4. Store concise episode metadata in `control_table.csv` and long-form results in `knowledge register.md`.
5. Use `py -3 build_ker_entries.py` to batch-generate extracted KER entries for mapped rows.
6. Generate or regenerate stubs with `build_intent_stubs.ps1` after updating `control_table.csv`.
7. Move repeated logic into `R/screencast_helpers.R` and episode-specific logic into `R/screencast_implementations.R`.
8. Prefer `load_tidyweek_data()` for mirrored TidyTuesday weeks before falling back to `tidytuesdayR::tt_load()`.
9. Use `py -3 build_super_qmd.py --queue-position <n>` to turn an episode guide plus KER metadata into a cognition-first authoring document.

## Control table workflow

Recommended fields:

- `transcript_title`
- `transcript_file`
- `code_file`
- `function_name`
- `data_source`
- `analysis_intent`
- `analysis_type`
- `pattern_signature`
- `adaptation_hint`
- `ker_status`
- `notes`

Recommended status flow:

- `needs_mapping`
- `mapped`
- `extracted`
- `implemented`
- `reviewed`

## Goals

- capture the author's EDA and predictive analysis patterns
- track every transcript, code, and dataset relationship
- turn episode-level analysis intent into reusable R functions
- preserve reasoning patterns, not just syntax
- apply prior episode knowledge to new datasets and future screencasts

## Next steps

- keep `control_table.csv` aligned with the expanded extraction schema
- use `prompts.md` to extract clean function signatures and reusable workflow patterns
- document which episodes include predictive analysis versus descriptive EDA
- keep `knowledge register.md` up to date as new transcript and code pairs are processed
