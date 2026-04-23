# Function Knowledge Register (KER) - Data Screencast Transcript Intent Repository

This file captures the reusable knowledge for every transcript, code, and data pair in the `sa-tidy-tuesday` workspace. It tracks the analysis intent behind each screencast episode, preserves the author's reasoning patterns, and supports the creation of reusable R functions that can be applied to future datasets.

## Metadata

| Field | Value |
|-------|-------|
| Project | Data Screencast Transcript Intent Functions |
| Repository | `c:\Users\mstoian\R\sa-tidy-tuesday` |
| Status | Working knowledge store |
| Date | 2026-04-16 |
| Purpose | Track transcript intent, code mapping, reusable function knowledge, and adaptation-ready patterns for every episode |

## How to use this file

1. Open `control_table.csv` to review the authoritative episode mapping and current work-queue status.
2. Treat `control_table.csv` as the compact row-level metadata store.
3. Treat this file as the long-form semantic memory for each episode.
4. Add or update one entry per transcript and code pair after running the master prompt from `prompts.md`.
5. Use the extracted patterns here to guide updates to `R/screencast_helpers.R`, `R/screencast_intent_stubs.R`, and `R/screencast_implementations.R`.

## Authoritative inputs

- `control_table.csv`
- `raw-data/inspiration/*.txt`
- `data-screencasts/*.Rmd`
- `R/intents.R`
- `R/screencast_intent_stubs.R`
- `build_intent_stubs.ps1`
- `build_ker_entries.py`
- `control_table_reverse_code_only.txt`

## Current repository summary

- Transcript text is stored in `raw-data/inspiration/`.
- Screencast analysis code is stored in `data-screencasts/`.
- Episode-to-code mapping and extraction status are maintained in `control_table.csv`.
- Function stubs are generated in `R/screencast_intent_stubs.R`.
- Shared helper functions are implemented in `R/screencast_helpers.R`.
- Episode implementations start in `R/screencast_implementations.R`.
- Regeneration logic is in `build_intent_stubs.ps1` and `R/intents.R`.
- `knowledge register.md` and `prompts.md` are the primary guidance files for building the function repository.

## Control table fields

The control table should store the concise fields needed to iterate row by row:

- `transcript_title`: exact title or headline from the transcript file
- `transcript_file`: path to the transcript text file
- `code_file`: path to the matched R Markdown screencast code file
- `function_name`: reusable function name derived from the transcript intent
- `data_source`: dataset or data file used by the episode, inferred from code and transcript evidence
- `analysis_intent`: the episode's main question, story, or predictive objective
- `analysis_type`: category such as `EDA`, `Visualization`, `Data Cleaning`, `Predictive`, `Modeling`, `Scraping`, or `Summary`
- `pattern_signature`: short label for the dominant reusable workflow
- `adaptation_hint`: short note for how to transfer the workflow to a new dataset
- `ker_status`: workflow status such as `needs_mapping`, `mapped`, `extracted`, `implemented`, or `reviewed`
- `notes`: mapping quality, assumptions, data issues, and helper-function hints

## What belongs in the KER

The KER should hold the full outputs from the master prompt:

1. Thought Process Map
2. Code Mapping Table
3. Data Transformation Flow
4. Reusable Patterns
5. Function Candidates
6. Episode Signature
7. Adaptation Plan

Use the control table for summaries. Use the KER for the rich episode record.

## Current learning pattern

- Most episodes use a strong EDA-first workflow: load data, inspect structure, explore distributions, compare groups, and tell a story.
- The author often layers domain context or timelines on top of the EDA output, making those visualization patterns reusable.
- Predictive analysis typically builds on the EDA base: clean the data, select features, fit a model, and evaluate performance.
- Capturing intent at the episode level allows new datasets to benefit from prior EDA and modeling patterns.
- The master prompt should preserve not just what code was written, but why the author chose that path.

## Reusable knowledge goals

- Capture common EDA patterns across episodes:
  - dataset loading and type inspection
  - cleaning and renaming variable names
  - missing-value and outlier checks
  - category counts and frequency summaries
  - time-series and timeline visualizations
  - joins or enrichments for supplemental context
- Capture text-analysis patterns when they appear:
  - tokenization
  - stopword removal
  - tf-idf
  - log-odds
  - grouped vocabulary comparison
- Capture predictive and modeling patterns when they appear:
  - outcome selection
  - train-test validation
  - model training and metric reporting
  - simple forecasting or classification pipelines
- Extract generic helper function names from repeated behavior, such as:
  - `clean_screencast_names()`
  - `summarize_categorical_data()`
  - `plot_time_series_summary()`
  - `build_predictive_pipeline()`
  - `load_remote_csv()`
  - `prepare_lyrics_tokens()`
  - `compute_tf_idf()`
  - `compute_log_odds()`

## Episode entry template

Use this template when appending a new episode section:

### `function_name`

- `transcript_title`:
- `transcript_file`:
- `code_file`:
- `data_source`:
- `analysis_intent`:
- `analysis_type`:
- `pattern_signature`:
- `adaptation_hint`:
- `ker_status`:

Thought Process Map:

- `Thought_ID | Step_Type | Description | Trigger`

Code Mapping Table:

- `Thought_ID | Code_Block | Function_Used | Purpose`

Data Transformation Flow:

- `Stage | Input | Operation | Output | Purpose`

Reusable Patterns:

- `Pattern_Name | Description | Inputs | Outputs | Reusable`

Function Candidates:

- `function_name`

Episode Signature:

- `analysis_intent`
- `analysis_type`
- `primary_techniques`
- `data_complexity_level`
- `reusable_difficulty_score`

Adaptation Plan:

- `Step | Reused Pattern | Adaptation Required`

## Extracted episodes

### `african_american_achievements`

- `transcript_title`: Analyzing African-American achievements in R
- `transcript_file`: `raw-data/inspiration/Analyzing African-American achievements in R.txt`
- `code_file`: `data-screencasts/african-american-achievements.Rmd`
- `data_source`: TidyTuesday 2020-06-09 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in African-American achievements through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_scrape_reshape_trend_compare_visualize`
- `adaptation_hint`: Reuse for datasets that must be assembled from HTML or JSON sources before analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of African-American achievements with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T3 | Transform | Acquire or supplement source data from external web pages or APIs before analysis. | Presence of scraping or external-source code`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, read_html, count | Establish source shape, units, and comparison candidates`
- `T3 | External acquisition | read_html | Build or enrich the dataset before analysis`
- `T4 | Structuring and enrichment | spread, separate_rows, unnest | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Collected | External web or JSON sources | Scrape or request supplemental records | Collected reference tables | Fill gaps not available in the initial source`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `scrape_supporting_reference_data | Pull structured records from HTML or JSON before analysis | External source url and parsing rules | Supplemental reference table | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `scrape_reference_table(url, css_selector)`
- `collect_episode_source_records(urls, parser)`
- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in African-American achievements through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, web or API data collection, reshaping, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `2 | scrape_supporting_reference_data | Rebuild any missing lookup or metadata tables from the relevant external source`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `african_american_history`

- `transcript_title`: Analyzing African-American history in R
- `transcript_file`: `raw-data/inspiration/Analyzing African-American history in R.txt`
- `code_file`: `data-screencasts/african-american-history.Rmd`
- `data_source`: TidyTuesday 2020-06-16 dataset
- `analysis_intent`: Explore and compare language patterns in African-American history using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_tokenize_trend_compare_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of African-American history with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | episode-specific dplyr and ggplot verbs | Identify terms that distinguish groups or documents`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in African-American history using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, tokenization, term comparison, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `animal_crossing`

- `transcript_title`: Analyzing Animal Crossing in R
- `transcript_file`: `raw-data/inspiration/Analyzing Animal Crossing in R.txt`
- `code_file`: `data-screencasts/animal-crossing.Rmd`
- `data_source`: TidyTuesday 2020-05-05 source files
- `analysis_intent`: Explore and compare language patterns in Animal Crossing using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_tokenize_trend_compare_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Animal Crossing with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, unnest, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | unnest_tokens, anti_join | Identify terms that distinguish groups or documents`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in Animal Crossing using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `australian_animal_outcomes`

- `transcript_title`: Analyzing Australian animal outcomes in R
- `transcript_file`: `raw-data/inspiration/Analyzing Australian animal outcomes in R.txt`
- `code_file`: `data-screencasts/australian-animal-outcomes.Rmd`
- `data_source`: TidyTuesday 2020-07-21 dataset
- `analysis_intent`: Explore geographic and temporal variation in Australian animal outcomes through joins, summarization, and mapping
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_scrape_reshape_join_map_trend_compare_visualize`
- `adaptation_hint`: Reuse for web-sourced reference tables that need cleaning, joining, and geographic display
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Australian animal outcomes with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T3 | Transform | Acquire or supplement source data from external web pages or APIs before analysis. | Presence of scraping or external-source code`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Translate the analytical result into geographic views to reveal regional variation and outliers. | Spatial joins or mapping code`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, read_html, count | Establish source shape, units, and comparison candidates`
- `T3 | External acquisition | read_html, html_nodes, GET | Build or enrich the dataset before analysis`
- `T4 | Structuring and enrichment | pivot_longer, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, geom_sf | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Collected | External web or JSON sources | Scrape or request supplemental records | Collected reference tables | Fill gaps not available in the initial source`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Analytical summaries with geographic identifiers | Join map geometry or region lookup data | Map-ready plotting table | Display geographic variation`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `scrape_supporting_reference_data | Pull structured records from HTML or JSON before analysis | External source url and parsing rules | Supplemental reference table | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `prepare_geographic_summary | Aggregate metrics by region and join map geometry or lookup tables | Regional metrics and identifiers | Map-ready data | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `scrape_reference_table(url, css_selector)`
- `collect_episode_source_records(urls, parser)`
- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_map_summary(data, region_col, value_col)`
- `plot_geographic_metric(map_data, value_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore geographic and temporal variation in Australian animal outcomes through joins, summarization, and mapping
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, web or API data collection, reshaping, table joins, mapping, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `2 | scrape_supporting_reference_data | Rebuild any missing lookup or metadata tables from the relevant external source`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `7 | prepare_geographic_summary | Aggregate to the geographic unit available in the new dataset and rebuild the map join`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `bob_ross_paintings`

- `transcript_title`: Analyzing Bob Ross paintings in R
- `transcript_file`: `raw-data/inspiration/Analyzing Bob Ross paintings in R.txt`
- `code_file`: `data-screencasts/bob-ross.Rmd`
- `data_source`: TidyTuesday 2019-08-06 source files
- `analysis_intent`: Explore and compare language patterns in Bob Ross paintings using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_tokenize_compare_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Bob Ross paintings with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | episode-specific dplyr and ggplot verbs | Identify terms that distinguish groups or documents`
- `T6 | Group comparison | group_by, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in Bob Ross paintings using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, tokenization, term comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `broadway_shows`

- `transcript_title`: Analyzing Broadway shows in R
- `transcript_file`: `raw-data/inspiration/Analyzing Broadway shows in R.txt`
- `code_file`: `data-screencasts/broadway.Rmd`
- `data_source`: TidyTuesday 2020-04-28 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in Broadway shows through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Broadway shows with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load | Establish source shape, units, and comparison candidates`
- `T6 | Group comparison | summarize, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in Broadway shows through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `chopped_epiodes`

- `transcript_title`: Analyzing Chopped epiodes in R
- `transcript_file`: `raw-data/inspiration/Analyzing Chopped epiodes in R.txt`
- `code_file`: `data-screencasts/2020_08_25_chopped.Rmd`
- `data_source`: TidyTuesday 2020-08-25 dataset
- `analysis_intent`: Predict or estimate outcomes in Chopped epiodes using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `pattern_signature`: `load_inspect_reshape_join_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for tabular datasets with a clear outcome column, engineered features, and model evaluation needs
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Chopped epiodes with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | pivot_longer, pivot_wider, separate_rows | Convert messy inputs into analysis-ready tables`
- `T6 | Modeling and evaluation | lm, glm, recipe, fit, predict | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Predict or estimate outcomes in Chopped epiodes using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `european_energy`

- `transcript_title`: Analyzing European energy in R
- `transcript_file`: `raw-data/inspiration/Analyzing European energy in R.txt`
- `code_file`: `data-screencasts/2020_08_04_europe_energy.Rmd`
- `data_source`: TidyTuesday 2020-08-04 dataset
- `analysis_intent`: Explore and compare language patterns in European energy using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_tokenize_trend_compare_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of European energy with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | pivot_longer | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | episode-specific dplyr and ggplot verbs | Identify terms that distinguish groups or documents`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in European energy using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, tokenization, term comparison, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `friends_transcripts`

- `transcript_title`: Analyzing Friends transcripts in R
- `transcript_file`: `raw-data/inspiration/Analyzing Friends transcripts in R.txt`
- `code_file`: `data-screencasts/2020_09_08_friends.Rmd`
- `data_source`: TidyTuesday 2020-09-08 dataset
- `analysis_intent`: Explore and compare language patterns in Friends transcripts using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_reshape_join_tokenize_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Friends transcripts with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count, glimpse | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | spread, unnest, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | unnest_tokens, anti_join, bind_log_odds | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | lm, predict | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in Friends transcripts using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, modeling, time-aware comparison, visualization
- `data_complexity_level`: high
- `reusable_difficulty_score`: 5

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `gdpr_violations`

- `transcript_title`: Analyzing GDPR violations in R
- `transcript_file`: `raw-data/inspiration/Analyzing GDPR violations in R.txt`
- `code_file`: `data-screencasts/gdpr.Rmd`
- `data_source`: TidyTuesday 2020-04-21 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in GDPR violations through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_trend_compare_visualize`
- `adaptation_hint`: Reuse for messy multi-table datasets that need reshaping, enrichment, and grouped summaries before plotting
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of GDPR violations with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | separate_rows, left_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in GDPR violations through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `global_health_spending`

- `transcript_title`: Analyzing Global Health Spending in R
- `transcript_file`: `raw-data/inspiration/Analyzing Global Health Spending in R.txt`
- `code_file`: `data-screencasts/2026_04_21_global_health_spending.Rmd`
- `data_source`: TidyTuesday 2026-04-21 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in Global Health Spending through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_trend_compare`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Global Health Spending with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, glimpse | Establish source shape, units, and comparison candidates`
- `T6 | Group comparison | episode-specific dplyr and ggplot verbs | Compare categories, time periods, or entities`
- `T7 | Visualization | episode-specific dplyr and ggplot verbs | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in Global Health Spending through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `hbcu_enrollment`

- `transcript_title`: Analyzing HBCU enrollment in R
- `transcript_file`: `raw-data/inspiration/Analyzing HBCU enrollment in R.txt`
- `code_file`: `data-screencasts/2021_02_02_hbcu.Rmd`
- `data_source`: TidyTuesday 2021-02-02 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in HBCU enrollment through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_trend_compare_visualize`
- `adaptation_hint`: Reuse for messy multi-table datasets that need reshaping, enrichment, and grouped summaries before plotting
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of HBCU enrollment with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, read_excel | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, spread | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in HBCU enrollment through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `ikea_furniture`

- `transcript_title`: Analyzing IKEA furniture in R
- `transcript_file`: `raw-data/inspiration/Analyzing IKEA furniture in R.txt`
- `code_file`: `data-screencasts/2020_11_03_ikea.Rmd`
- `data_source`: TidyTuesday 2020-11-03 dataset
- `analysis_intent`: Explore, explain, and model patterns in IKEA furniture using engineered features and comparative summaries
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for structured datasets where descriptive analysis leads into explanatory or predictive models
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of IKEA furniture with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T6 | Modeling and evaluation | lm, predict | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore, explain, and model patterns in IKEA furniture using engineered features and comparative summaries
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, modeling, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `maryland_bridges`

- `transcript_title`: Analyzing Maryland bridges with R
- `transcript_file`: `raw-data/inspiration/Analyzing Maryland bridges with R.txt`
- `code_file`: `data-screencasts/baltimore_bridges.Rmd`
- `data_source`: Local source files read in episode: https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-11-27/baltimore_bridges.csv
- `analysis_intent`: Explore, explain, and model patterns in Maryland bridges using engineered features and comparative summaries
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_model_evaluate_visualize`
- `adaptation_hint`: Reuse for structured datasets where descriptive analysis leads into explanatory or predictive models
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Maryland bridges with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T6 | Modeling and evaluation | lm, glm, fit, predict | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore, explain, and model patterns in Maryland bridges using engineered features and comparative summaries
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, modeling, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `medium_articles`

- `transcript_title`: Analyzing Medium articles with R
- `transcript_file`: `raw-data/inspiration/Analyzing Medium articles with R.txt`
- `code_file`: `data-screencasts/medium-datasci.Rmd`
- `data_source`: Local source files read in episode: https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-12-04/medium_datasci.csv
- `analysis_intent`: Predict or estimate outcomes in Medium articles using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `pattern_signature`: `load_inspect_reshape_join_tokenize_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for tabular datasets with a clear outcome column, engineered features, and model evaluation needs
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Medium articles with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, unnest | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | unnest_tokens, anti_join | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | lm, glm, fit, predict | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_line | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Predict or estimate outcomes in Medium articles using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `ncaa_women_s_basketball`

- `transcript_title`: Analyzing NCAA Women's Basketball
- `transcript_file`: `raw-data/inspiration/Analyzing NCAA Women's Basketball.txt`
- `code_file`: `data-screencasts/2020_10_06_ncaa_womens_basketball.Rmd`
- `data_source`: TidyTuesday 2020-10-06 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in NCAA Women's Basketball through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of NCAA Women's Basketball with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in NCAA Women's Basketball through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `nyc_restaurant_inspections`

- `transcript_title`: Analyzing NYC restaurant inspections with R
- `transcript_file`: `raw-data/inspiration/Analyzing NYC restaurant inspections with R.txt`
- `code_file`: `data-screencasts/nyc-restaurants.Rmd`
- `data_source`: Local source files read in episode: https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv
- `analysis_intent`: Explore distributions, group differences, and notable patterns in NYC restaurant inspections through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_trend_compare_visualize`
- `adaptation_hint`: Reuse for messy multi-table datasets that need reshaping, enrichment, and grouped summaries before plotting
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of NYC restaurant inspections with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | unnest | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in NYC restaurant inspections through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `netflix_titles`

- `transcript_title`: Analyzing Netflix titles in R
- `transcript_file`: `raw-data/inspiration/Analyzing Netflix titles in R.txt`
- `code_file`: `data-screencasts/2021_04_20_netflix_titles.Rmd`
- `data_source`: TidyTuesday 2021-04-20 dataset
- `analysis_intent`: Predict or estimate outcomes in Netflix titles using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `pattern_signature`: `load_inspect_reshape_join_tokenize_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for tabular datasets with a clear outcome column, engineered features, and model evaluation needs
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Netflix titles with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, spread, separate_rows, unnest | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | unnest_tokens, anti_join, bind_log_odds | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | lm, glm, fit | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Predict or estimate outcomes in Netflix titles using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `ninja_warrior`

- `transcript_title`: Analyzing Ninja Warrior in R
- `transcript_file`: `raw-data/inspiration/Analyzing Ninja Warrior in R.txt`
- `code_file`: `data-screencasts/2020_12_15_ninja_warrior.Rmd`
- `data_source`: TidyTuesday 2020-12-15 dataset
- `analysis_intent`: Explore and compare language patterns in Ninja Warrior using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_tokenize_trend_compare_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Ninja Warrior with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count, glimpse | Establish source shape, units, and comparison candidates`
- `T5 | Text comparison | bind_log_odds | Identify terms that distinguish groups or documents`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in Ninja Warrior using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, tokenization, term comparison, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `nobel_prize_winners`

- `transcript_title`: Analyzing Nobel Prize winners in R
- `transcript_file`: `raw-data/inspiration/Analyzing Nobel Prize winners in R.txt`
- `code_file`: `data-screencasts/nobel-prize.Rmd`
- `data_source`: TidyTuesday 2019-05-14 source files
- `analysis_intent`: Explore distributions, group differences, and notable patterns in Nobel Prize winners through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_join_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Nobel Prize winners with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in Nobel Prize winners through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, table joins, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `simpsons_guest_stars_dialogue`

- `transcript_title`: Analyzing Simpsons guest stars and dialogue in R
- `transcript_file`: `raw-data/inspiration/Analyzing Simpsons guest stars and dialogue in R.txt`
- `code_file`: `data-screencasts/simpsons-guests.Rmd`
- `data_source`: TidyTuesday 2019-08-27 source files
- `analysis_intent`: Explore and compare language patterns in Simpsons guest stars and dialogue using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_tokenize_compare_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Simpsons guest stars and dialogue with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | separate_rows, unnest, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | unnest_tokens, anti_join, bind_tf_idf | Identify terms that distinguish groups or documents`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in Simpsons guest stars and dialogue using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `super_bowl_ads`

- `transcript_title`: Analyzing Super Bowl ads in R
- `transcript_file`: `raw-data/inspiration/Analyzing Super Bowl ads in R.txt`
- `code_file`: `data-screencasts/2021_03_02_super_bowl_ads.Rmd`
- `data_source`: TidyTuesday 2021-03-02 dataset
- `analysis_intent`: Explore and compare language patterns in Super Bowl ads using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_reshape_join_tokenize_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Super Bowl ads with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, unnest, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | episode-specific dplyr and ggplot verbs | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | lm, glm | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in Super Bowl ads using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `thanksgiving_dinners`

- `transcript_title`: Analyzing Thanksgiving dinners in R
- `transcript_file`: `raw-data/inspiration/Analyzing Thanksgiving dinners in R.txt`
- `code_file`: `data-screencasts/thanksgiving.Rmd`
- `data_source`: Local source files read in episode: https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-11-20/thanksgiving_meals.csv
- `analysis_intent`: Explore distributions, group differences, and notable patterns in Thanksgiving dinners through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_compare_visualize`
- `adaptation_hint`: Reuse for messy multi-table datasets that need reshaping, enrichment, and grouped summaries before plotting
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Thanksgiving dinners with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in Thanksgiving dinners through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `tour_de_france`

- `transcript_title`: Analyzing Tour de France data in R
- `transcript_file`: `raw-data/inspiration/Analyzing Tour de France data in R.txt`
- `code_file`: `data-screencasts/tour-de-france.Rmd`
- `data_source`: TidyTuesday 2020-04-07 dataset
- `analysis_intent`: Explore and compare language patterns in Tour de France using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_join_tokenize_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Tour de France with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | episode-specific dplyr and ggplot verbs | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | fit, predict, survfit | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_line | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in Tour de France using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, table joins, tokenization, term comparison, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `un_votes`

- `transcript_title`: Analyzing UN votes in R
- `transcript_file`: `raw-data/inspiration/Analyzing UN votes in R.txt`
- `code_file`: `data-screencasts/2021_03_23_un_votes.Rmd`
- `data_source`: TidyTuesday 2021-03-23 dataset
- `analysis_intent`: Explore and compare language patterns in UN votes using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_tokenize_map_trend_compare_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of UN votes with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Translate the analytical result into geographic views to reveal regional variation and outliers. | Spatial joins or mapping code`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | spread, unnest, left_join, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | unnest_tokens, anti_join | Identify terms that distinguish groups or documents`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Analytical summaries with geographic identifiers | Join map geometry or region lookup data | Map-ready plotting table | Display geographic variation`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `prepare_geographic_summary | Aggregate metrics by region and join map geometry or lookup tables | Regional metrics and identifiers | Map-ready data | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `prepare_map_summary(data, region_col, value_col)`
- `plot_geographic_metric(map_data, value_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in UN votes using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, mapping, time-aware comparison, visualization
- `data_complexity_level`: high
- `reusable_difficulty_score`: 5

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `7 | prepare_geographic_summary | Aggregate to the geographic unit available in the new dataset and rebuild the map join`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `dairy_consumption`

- `transcript_title`: Analyzing US dairy consumption in R
- `transcript_file`: `raw-data/inspiration/Analyzing US dairy consumption in R.txt`
- `code_file`: `data-screencasts/us-dairy.Rmd`
- `data_source`: TidyTuesday 2019-01-29 source files
- `analysis_intent`: Explore distributions, group differences, and notable patterns in US dairy consumption through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_trend_simulate_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of US dairy consumption with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, unnest | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in US dairy consumption through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `wind`

- `transcript_title`: Analyzing US wind data in R
- `transcript_file`: `raw-data/inspiration/Analyzing US wind data in R.txt`
- `code_file`: `data-screencasts/us-wind.Rmd`
- `data_source`: Local source files read in episode: https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-11-06/us_wind.csv
- `analysis_intent`: Explore distributions, group differences, and notable patterns in US wind through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_trend_simulate_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of US wind with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv | Establish source shape, units, and comparison candidates`
- `T6 | Group comparison | group_by, summarize, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_point | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in US wind through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `video_games`

- `transcript_title`: Analyzing Video Games in R
- `transcript_file`: `raw-data/inspiration/Analyzing Video Games in R.txt`
- `code_file`: `data-screencasts/2021_03_16_video_games.Rmd`
- `data_source`: TidyTuesday 2021-03-16 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in Video Games through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_trend_compare_visualize`
- `adaptation_hint`: Reuse for messy multi-table datasets that need reshaping, enrichment, and grouped summaries before plotting
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Video Games with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count, glimpse | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | pivot_wider, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in Video Games through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `women_s_world_cup`

- `transcript_title`: Analyzing Women's World Cup data in R
- `transcript_file`: `raw-data/inspiration/Analyzing Women's World Cup data.txt`
- `code_file`: `data-screencasts/womens-world-cup.Rmd`
- `data_source`: TidyTuesday 2019-07-09 source files
- `analysis_intent`: Explore distributions, group differences, and notable patterns in Women's World Cup through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_scrape_join_trend_compare_visualize`
- `adaptation_hint`: Reuse for datasets that must be assembled from HTML or JSON sources before analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of Women's World Cup with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T3 | Transform | Acquire or supplement source data from external web pages or APIs before analysis. | Presence of scraping or external-source code`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, read_html, count | Establish source shape, units, and comparison candidates`
- `T3 | External acquisition | read_html, html_nodes, GET | Build or enrich the dataset before analysis`
- `T4 | Structuring and enrichment | left_join, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Collected | External web or JSON sources | Scrape or request supplemental records | Collected reference tables | Fill gaps not available in the initial source`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `scrape_supporting_reference_data | Pull structured records from HTML or JSON before analysis | External source url and parsing rules | Supplemental reference table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `scrape_reference_table(url, css_selector)`
- `collect_episode_source_records(urls, parser)`
- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in Women's World Cup through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, web or API data collection, table joins, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `2 | scrape_supporting_reference_data | Rebuild any missing lookup or metadata tables from the relevant external source`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `x_men_comics`

- `transcript_title`: Analyzing X-Men comics in R
- `transcript_file`: `raw-data/inspiration/Analyzing X-Men comics in R.txt`
- `code_file`: `data-screencasts/uncanny-xmen.Rmd`
- `data_source`: TidyTuesday 2020-06-30 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in X-Men comics through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_join_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of X-Men comics with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | left_join, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in X-Men comics through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, table joins, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `predicting_horror_movie_ratings`

- `transcript_title`: Analyzing and predicting horror movie ratings in R
- `transcript_file`: `raw-data/inspiration/Analyzing and predicting horror movie ratings in R.txt`
- `code_file`: `data-screencasts/horror-movie-ratings.Rmd`
- `data_source`: TidyTuesday 2019-10-22 source files
- `analysis_intent`: Predict or estimate outcomes in horror movie ratings using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `pattern_signature`: `load_inspect_reshape_join_tokenize_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for tabular datasets with a clear outcome column, engineered features, and model evaluation needs
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of horror movie ratings with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, separate_rows, unnest | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | unnest_tokens, anti_join | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | lm, glm, fit, predict | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Predict or estimate outcomes in horror movie ratings using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `art_collections`

- `transcript_title`: Analyzing art collections in R
- `transcript_file`: `raw-data/inspiration/Analyzing art collections in R.txt`
- `code_file`: `data-screencasts/2021_01_12_tate_art.Rmd`
- `data_source`: TidyTuesday 2021-01-12 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in art collections through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of art collections with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count, glimpse | Establish source shape, units, and comparison candidates`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in art collections through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `beach_volleyball`

- `transcript_title`: Analyzing beach volleyball in R
- `transcript_file`: `raw-data/inspiration/Analyzing beach volleyball in R.txt`
- `code_file`: `data-screencasts/beach-volleyball.Rmd`
- `data_source`: TidyTuesday 2020-05-19 dataset
- `analysis_intent`: Explore, explain, and model patterns in beach volleyball using engineered features and comparative summaries
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_reshape_join_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for structured datasets where descriptive analysis leads into explanatory or predictive models
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of beach volleyball with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | pivot_longer, gather, spread, separate_rows, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Modeling and evaluation | lm, glm, predict | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_point | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore, explain, and model patterns in beach volleyball using engineered features and comparative summaries
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `bike_frequencies_seattle`

- `transcript_title`: Analyzing bike frequencies in Seattle in R
- `transcript_file`: `raw-data/inspiration/Analyzing bike frequencies in Seattle in R.txt`
- `code_file`: `data-screencasts/bike_traffic.Rmd`
- `data_source`: TidyTuesday 2019-04-02 source files
- `analysis_intent`: Explore distributions, group differences, and notable patterns in bike frequencies in Seattle through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of bike frequencies in Seattle with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | spread | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in bike frequencies in Seattle through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `bird_collisions_bootstrapping`

- `transcript_title`: Analyzing bird collisions with bootstrapping in R
- `transcript_file`: `raw-data/inspiration/Analyzing bird collisions with bootstrapping in R.txt`
- `code_file`: `data-screencasts/bird-collisions.Rmd`
- `data_source`: TidyTuesday 2019-04-30 source files
- `analysis_intent`: Explore distributions, group differences, and notable patterns in bird collisions with bootstrapping through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_trend_simulate_compare_visualize`
- `adaptation_hint`: Reuse for messy multi-table datasets that need reshaping, enrichment, and grouped summaries before plotting
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of bird collisions with bootstrapping with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, unnest, left_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in bird collisions with bootstrapping through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `board_games_predicting_ratings`

- `transcript_title`: Analyzing board games and predicting ratings in R
- `transcript_file`: `raw-data/inspiration/Analyzing board games and predicting ratings in R.txt`
- `code_file`: `data-screencasts/board-games.Rmd`
- `data_source`: TidyTuesday 2019-03-12 source files
- `analysis_intent`: Predict or estimate outcomes in board games and predicting ratings using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `pattern_signature`: `load_inspect_reshape_join_tokenize_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for tabular datasets with a clear outcome column, engineered features, and model evaluation needs
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of board games and predicting ratings with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, separate_rows, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | episode-specific dplyr and ggplot verbs | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | lm, glm, fit, predict | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Predict or estimate outcomes in board games and predicting ratings using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `car_fuel_efficiency`

- `transcript_title`: Analyzing car fuel efficiency in R
- `transcript_file`: `raw-data/inspiration/Analyzing car fuel efficiency in R.txt`
- `code_file`: `data-screencasts/car-economy.Rmd`
- `data_source`: TidyTuesday 2019-10-15 source files
- `analysis_intent`: Explore, explain, and model patterns in car fuel efficiency using engineered features and comparative summaries
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_reshape_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for structured datasets where descriptive analysis leads into explanatory or predictive models
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of car fuel efficiency with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | unnest | Convert messy inputs into analysis-ready tables`
- `T6 | Modeling and evaluation | lm, fit, predict | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore, explain, and model patterns in car fuel efficiency using engineered features and comparative summaries
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, reshaping, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `caribou_locations`

- `transcript_title`: Analyzing caribou locations in R
- `transcript_file`: `raw-data/inspiration/Analyzing caribou locations in R.txt`
- `code_file`: `data-screencasts/caribou-locations.Rmd`
- `data_source`: TidyTuesday 2020-06-23 dataset
- `analysis_intent`: Explore geographic and temporal variation in caribou locations through joins, summarization, and mapping
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_map_trend_compare_visualize`
- `adaptation_hint`: Reuse for geographic datasets with region codes, time fields, and map-ready joins
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of caribou locations with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Translate the analytical result into geographic views to reveal regional variation and outliers. | Spatial joins or mapping code`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_point, geom_line, geom_sf, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Analytical summaries with geographic identifiers | Join map geometry or region lookup data | Map-ready plotting table | Display geographic variation`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `prepare_geographic_summary | Aggregate metrics by region and join map geometry or lookup tables | Regional metrics and identifiers | Map-ready data | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `prepare_map_summary(data, region_col, value_col)`
- `plot_geographic_metric(map_data, value_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore geographic and temporal variation in caribou locations through joins, summarization, and mapping
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, mapping, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `7 | prepare_geographic_summary | Aggregate to the geographic unit available in the new dataset and rebuild the map join`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `cocktail_recipes`

- `transcript_title`: Analyzing cocktail recipes in R
- `transcript_file`: `raw-data/inspiration/Analyzing cocktail recipes in R.txt`
- `code_file`: `data-screencasts/cocktails.Rmd`
- `data_source`: TidyTuesday 2020-05-26 dataset
- `analysis_intent`: Explore and compare language patterns in cocktail recipes using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_tokenize_compare_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of cocktail recipes with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T5 | Text comparison | episode-specific dplyr and ggplot verbs | Identify terms that distinguish groups or documents`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in cocktail recipes using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, tokenization, term comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `code_cran_packages`

- `transcript_title`: Analyzing code in CRAN packages in R
- `transcript_file`: `raw-data/inspiration/Analyzing code in CRAN packages in R.txt`
- `code_file`: `data-screencasts/cran-code.Rmd`
- `data_source`: TidyTuesday 2019-11-12 dataset
- `analysis_intent`: Explore and compare language patterns in code in CRAN packages using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_tokenize_compare_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of code in CRAN packages with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, separate_rows, left_join, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | episode-specific dplyr and ggplot verbs | Identify terms that distinguish groups or documents`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in code in CRAN packages using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `coffee_ratings`

- `transcript_title`: Analyzing coffee ratings in R
- `transcript_file`: `raw-data/inspiration/Analyzing coffee ratings in R.txt`
- `code_file`: `data-screencasts/coffee-ratings.Rmd`
- `data_source`: TidyTuesday 2020-07-07 dataset
- `analysis_intent`: Explore and compare language patterns in coffee ratings using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_reshape_tokenize_model_evaluate_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of coffee ratings with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | pivot_longer, gather, unnest | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | episode-specific dplyr and ggplot verbs | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | lm | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in coffee ratings using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, reshaping, tokenization, term comparison, modeling, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `college_major_income`

- `transcript_title`: Analyzing college major & income data in R
- `transcript_file`: `raw-data/inspiration/Analyzing college major & income data in R.txt`
- `code_file`: `data-screencasts/college-majors.Rmd`
- `data_source`: Local source files read in episode: https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-10-16/recent-grads.csv
- `analysis_intent`: Explore, explain, and model patterns in college major & income using engineered features and comparative summaries
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_reshape_model_evaluate_visualize`
- `adaptation_hint`: Reuse for structured datasets where descriptive analysis leads into explanatory or predictive models
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of college major & income with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, unnest | Convert messy inputs into analysis-ready tables`
- `T6 | Modeling and evaluation | lm | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore, explain, and model patterns in college major & income using engineered features and comparative summaries
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, reshaping, modeling, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `downloads`

- `transcript_title`: Analyzing data on R downloads
- `transcript_file`: `raw-data/inspiration/Analyzing data on R downloads.txt`
- `code_file`: `data-screencasts/r-downloads.Rmd`
- `data_source`: Local source files read in episode: http://cran-logs.rstudio.com/2018/2018-10-27.csv.gz, https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-10-30/r_downloads_year.csv
- `analysis_intent`: Explore distributions, group differences, and notable patterns in data on R downloads through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of data on R downloads with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | spread | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in data on R downloads through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `women_workplace`

- `transcript_title`: Analyzing data on women in the workplace in R
- `transcript_file`: `raw-data/inspiration/Analyzing data on women in the workplace in R.txt`
- `code_file`: `data-screencasts/women-workplace.Rmd`
- `data_source`: TidyTuesday 2019-03-05 source files
- `analysis_intent`: Explore distributions, group differences, and notable patterns in data on women in the workplace through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of data on women in the workplace with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv | Establish source shape, units, and comparison candidates`
- `T6 | Group comparison | group_by, summarize, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in data on women in the workplace through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `deforestation`

- `transcript_title`: Analyzing deforestation in R
- `transcript_file`: `raw-data/inspiration/Analyzing deforestation in R.txt`
- `code_file`: `data-screencasts/2021_04_06_deforestation.Rmd`
- `data_source`: TidyTuesday 2021-04-06 dataset
- `analysis_intent`: Explore and compare language patterns in deforestation using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_tokenize_map_trend_compare_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of deforestation with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Translate the analytical result into geographic views to reveal regional variation and outliers. | Spatial joins or mapping code`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | pivot_longer, spread, left_join, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | episode-specific dplyr and ggplot verbs | Identify terms that distinguish groups or documents`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Analytical summaries with geographic identifiers | Join map geometry or region lookup data | Map-ready plotting table | Display geographic variation`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `prepare_geographic_summary | Aggregate metrics by region and join map geometry or lookup tables | Regional metrics and identifiers | Map-ready data | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `prepare_map_summary(data, region_col, value_col)`
- `plot_geographic_metric(map_data, value_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in deforestation using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, mapping, time-aware comparison, visualization
- `data_complexity_level`: high
- `reusable_difficulty_score`: 5

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `7 | prepare_geographic_summary | Aggregate to the geographic unit available in the new dataset and rebuild the map join`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `dolphin`

- `transcript_title`: Analyzing dolphin data in R
- `transcript_file`: `raw-data/inspiration/Analyzing dolphin data in R.txt`
- `code_file`: `data-screencasts/cetaceans.Rmd`
- `data_source`: Local source files read in episode: https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-12-18/allCetaceanData.csv
- `analysis_intent`: Explore, explain, and model patterns in dolphin using engineered features and comparative summaries
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for structured datasets where descriptive analysis leads into explanatory or predictive models
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of dolphin with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T6 | Modeling and evaluation | fit, survfit | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_line | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore, explain, and model patterns in dolphin using engineered features and comparative summaries
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, modeling, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `employment_earnings`

- `transcript_title`: Analyzing employment and earnings in R
- `transcript_file`: `raw-data/inspiration/Analyzing employment and earnings in R.txt`
- `code_file`: `data-screencasts/2021_02_23_employment_earnings.Rmd`
- `data_source`: TidyTuesday 2021-02-23 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in employment and earnings through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of employment and earnings with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in employment and earnings through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `exploring_beer_production`

- `transcript_title`: Analyzing exploring US beer production in R
- `transcript_file`: `raw-data/inspiration/Analyzing exploring US beer production in R.txt`
- `code_file`: `data-screencasts/beer-production.Rmd`
- `data_source`: TidyTuesday 2020-03-31 source files
- `analysis_intent`: Explore geographic and temporal variation in exploring US beer production through joins, summarization, and mapping
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_join_map_trend_compare_visualize`
- `adaptation_hint`: Reuse for geographic datasets with region codes, time fields, and map-ready joins
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of exploring US beer production with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Translate the analytical result into geographic views to reveal regional variation and outliers. | Spatial joins or mapping code`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line, geom_sf, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Analytical summaries with geographic identifiers | Join map geometry or region lookup data | Map-ready plotting table | Display geographic variation`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `prepare_geographic_summary | Aggregate metrics by region and join map geometry or lookup tables | Regional metrics and identifiers | Map-ready data | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_map_summary(data, region_col, value_col)`
- `plot_geographic_metric(map_data, value_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore geographic and temporal variation in exploring US beer production through joins, summarization, and mapping
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, table joins, mapping, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `7 | prepare_geographic_summary | Aggregate to the geographic unit available in the new dataset and rebuild the map join`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `extinct_plants`

- `transcript_title`: Analyzing extinct plants in R
- `transcript_file`: `raw-data/inspiration/Analyzing extinct plants in R.txt`
- `code_file`: `data-screencasts/2020_08_18_extinct_plants.Rmd`
- `data_source`: TidyTuesday 2020-08-18 dataset
- `analysis_intent`: Explore and compare language patterns in extinct plants using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_scrape_join_tokenize_trend_compare_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of extinct plants with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T3 | Transform | Acquire or supplement source data from external web pages or APIs before analysis. | Presence of scraping or external-source code`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, read_html, count | Establish source shape, units, and comparison candidates`
- `T3 | External acquisition | read_html, html_nodes, GET | Build or enrich the dataset before analysis`
- `T4 | Structuring and enrichment | inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | episode-specific dplyr and ggplot verbs | Identify terms that distinguish groups or documents`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Collected | External web or JSON sources | Scrape or request supplemental records | Collected reference tables | Fill gaps not available in the initial source`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `scrape_supporting_reference_data | Pull structured records from HTML or JSON before analysis | External source url and parsing rules | Supplemental reference table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `scrape_reference_table(url, css_selector)`
- `collect_episode_source_records(urls, parser)`
- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in extinct plants using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, web or API data collection, table joins, tokenization, term comparison, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `2 | scrape_supporting_reference_data | Rebuild any missing lookup or metadata tables from the relevant external source`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `franchise_revenue`

- `transcript_title`: Analyzing franchise revenue in R
- `transcript_file`: `raw-data/inspiration/Analyzing franchise revenue in R.txt`
- `code_file`: `data-screencasts/media-franchises.Rmd`
- `data_source`: TidyTuesday 2019-07-02 source files
- `analysis_intent`: Explore distributions, group differences, and notable patterns in franchise revenue through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_join_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of franchise revenue with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | episode-specific dplyr and ggplot verbs | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in franchise revenue through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, table joins, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `global_crop_yields`

- `transcript_title`: Analyzing global crop yields in R
- `transcript_file`: `raw-data/inspiration/Analyzing global crop yields in R.txt`
- `code_file`: `data-screencasts/2020_09_01_crop_yields.Rmd`
- `data_source`: TidyTuesday 2020-09-01 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in global crop yields through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of global crop yields with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | pivot_longer | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in global crop yields through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `government_spending_kids`

- `transcript_title`: Analyzing government spending on kids in R
- `transcript_file`: `raw-data/inspiration/Analyzing government spending on kids in R.txt`
- `code_file`: `data-screencasts/2020_09_15_government_spending_kids.Rmd`
- `data_source`: TidyTuesday 2020-09-15 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in government spending on kids through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of government spending on kids with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, read_csv | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | pivot_longer, pivot_wider | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in government spending on kids through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `historical_phones`

- `transcript_title`: Analyzing historical phones in R
- `transcript_file`: `raw-data/inspiration/Analyzing historical phones in R.txt`
- `code_file`: `data-screencasts/2020_11_10_phone_history.Rmd`
- `data_source`: TidyTuesday 2020-11-10 dataset
- `analysis_intent`: Explore geographic and temporal variation in historical phones through joins, summarization, and mapping
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_map_trend_compare_visualize`
- `adaptation_hint`: Reuse for geographic datasets with region codes, time fields, and map-ready joins
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of historical phones with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Translate the analytical result into geographic views to reveal regional variation and outliers. | Spatial joins or mapping code`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count, glimpse | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | pivot_wider, left_join, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Analytical summaries with geographic identifiers | Join map geometry or region lookup data | Map-ready plotting table | Display geographic variation`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `prepare_geographic_summary | Aggregate metrics by region and join map geometry or lookup tables | Regional metrics and identifiers | Map-ready data | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_map_summary(data, region_col, value_col)`
- `plot_geographic_metric(map_data, value_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore geographic and temporal variation in historical phones through joins, summarization, and mapping
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, mapping, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `7 | prepare_geographic_summary | Aggregate to the geographic unit available in the new dataset and rebuild the map join`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `horror_movie_profits`

- `transcript_title`: Analyzing horror movie profits in R
- `transcript_file`: `raw-data/inspiration/Analyzing horror movie profits in R.txt`
- `code_file`: `data-screencasts/movie-profit.Rmd`
- `data_source`: Local source files read in episode: https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-10-23/movie_profit.csv
- `analysis_intent`: Explore distributions, group differences, and notable patterns in horror movie profits through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of horror movie profits with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in horror movie profits through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `malaria_incidence`

- `transcript_title`: Analyzing malaria incidence in R
- `transcript_file`: `raw-data/inspiration/Analyzing malaria incidence in R.txt`
- `code_file`: `data-screencasts/malaria.Rmd`
- `data_source`: Local source files read in episode: https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-11-13/malaria_deaths.csv, https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-11-13/malaria_inc.csv
- `analysis_intent`: Explore geographic and temporal variation in malaria incidence through joins, summarization, and mapping
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_map_trend_compare_visualize`
- `adaptation_hint`: Reuse for geographic datasets with region codes, time fields, and map-ready joins
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of malaria incidence with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Translate the analytical result into geographic views to reveal regional variation and outliers. | Spatial joins or mapping code`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | spread, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Analytical summaries with geographic identifiers | Join map geometry or region lookup data | Map-ready plotting table | Display geographic variation`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `prepare_geographic_summary | Aggregate metrics by region and join map geometry or lookup tables | Regional metrics and identifiers | Map-ready data | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_map_summary(data, region_col, value_col)`
- `plot_geographic_metric(map_data, value_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore geographic and temporal variation in malaria incidence through joins, summarization, and mapping
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, mapping, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `7 | prepare_geographic_summary | Aggregate to the geographic unit available in the new dataset and rebuild the map join`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `penguins`

- `transcript_title`: Analyzing penguins in R
- `transcript_file`: `raw-data/inspiration/Analyzing penguins in R.txt`
- `code_file`: `data-screencasts/2020_07_28_penguins.Rmd`
- `data_source`: TidyTuesday 2020-07-28 dataset
- `analysis_intent`: Predict or estimate outcomes in penguins using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `pattern_signature`: `load_inspect_reshape_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for tabular datasets with a clear outcome column, engineered features, and model evaluation needs
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of penguins with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | pivot_longer, unnest | Convert messy inputs into analysis-ready tables`
- `T6 | Modeling and evaluation | lm, glm, fit, predict, vfold_cv | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_point, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Predict or estimate outcomes in penguins using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `primary_techniques`: schema inspection, grouped summaries, reshaping, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `pet_names_seattle`

- `transcript_title`: Analyzing pet names in Seattle in R
- `transcript_file`: `raw-data/inspiration/Analyzing pet names in Seattle in R.txt`
- `code_file`: `data-screencasts/seattle-pets.Rmd`
- `data_source`: TidyTuesday 2019-03-26 source files
- `analysis_intent`: Explore distributions, group differences, and notable patterns in pet names in Seattle through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_join_trend_simulate_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of pet names in Seattle with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in pet names in Seattle through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, table joins, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `pizza_ratings`

- `transcript_title`: Analyzing pizza ratings in R
- `transcript_file`: `raw-data/inspiration/Analyzing pizza ratings in R.txt`
- `code_file`: `data-screencasts/nyc-pizza.Rmd`
- `data_source`: TidyTuesday 2019-10-01 source files
- `analysis_intent`: Explore, explain, and model patterns in pizza ratings using engineered features and comparative summaries
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_reshape_join_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for structured datasets where descriptive analysis leads into explanatory or predictive models
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of pizza ratings with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | unnest, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Modeling and evaluation | lm | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore, explain, and model patterns in pizza ratings using engineered features and comparative summaries
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `plastic_waste_across_countries`

- `transcript_title`: Analyzing plastic waste across countries in R
- `transcript_file`: `raw-data/inspiration/Analyzing plastic waste across countries in R.txt`
- `code_file`: `data-screencasts/plastic-waste.Rmd`
- `data_source`: TidyTuesday 2019-05-21 source files
- `analysis_intent`: Explore distributions, group differences, and notable patterns in plastic waste across countries through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_join_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of plastic waste across countries with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | left_join, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_point | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in plastic waste across countries through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, table joins, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `post_offices`

- `transcript_title`: Analyzing post offices in R
- `transcript_file`: `raw-data/inspiration/Analyzing post offices in R.txt`
- `code_file`: `data-screencasts/2021_04_13_post_offices.Rmd`
- `data_source`: TidyTuesday 2021-04-13 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in post offices through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_trend_compare_visualize`
- `adaptation_hint`: Reuse for messy multi-table datasets that need reshaping, enrichment, and grouped summaries before plotting
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of post offices with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | unnest, left_join, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in post offices through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `predicting_wine_ratings`

- `transcript_title`: Analyzing predicting wine ratings in R
- `transcript_file`: `raw-data/inspiration/Analyzing predicting wine ratings in R.txt`
- `code_file`: `data-screencasts/wine-ratings.Rmd`
- `data_source`: TidyTuesday 2019-05-28 source files
- `analysis_intent`: Predict or estimate outcomes in wine ratings using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `pattern_signature`: `load_inspect_join_tokenize_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for tabular datasets with a clear outcome column, engineered features, and model evaluation needs
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of wine ratings with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | unnest, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | unnest_tokens, anti_join | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | lm, glm, fit, predict | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Predict or estimate outcomes in wine ratings using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `primary_techniques`: schema inspection, grouped summaries, table joins, tokenization, term comparison, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `ratings_scripts_from_office`

- `transcript_title`: Analyzing ratings and scripts from The Office in R
- `transcript_file`: `raw-data/inspiration/Analyzing ratings and scripts from The Office in R.txt`
- `code_file`: `data-screencasts/office-transcripts.Rmd`
- `data_source`: TidyTuesday 2020-03-17 source files
- `analysis_intent`: Predict or estimate outcomes in ratings and scripts from The Office using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `pattern_signature`: `load_inspect_reshape_join_tokenize_model_evaluate_visualize`
- `adaptation_hint`: Reuse for tabular datasets with a clear outcome column, engineered features, and model evaluation needs
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of ratings and scripts from The Office with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, separate_rows, unnest, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | unnest_tokens, anti_join, bind_tf_idf | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | lm, glm, fit | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Predict or estimate outcomes in ratings and scripts from The Office using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, modeling, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `space_launches`

- `transcript_title`: Analyzing space launches in R
- `transcript_file`: `raw-data/inspiration/Analyzing space launches in R.txt`
- `code_file`: `data-screencasts/space-launches.Rmd`
- `data_source`: TidyTuesday 2019-01-15 source files
- `analysis_intent`: Explore distributions, group differences, and notable patterns in space launches through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_join_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of space launches with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in space launches through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, table joins, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `squirrels_nyc`

- `transcript_title`: Analyzing squirrels in NYC in R
- `transcript_file`: `raw-data/inspiration/Analyzing squirrels in NYC in R.txt`
- `code_file`: `data-screencasts/nyc-squirrels.Rmd`
- `data_source`: TidyTuesday 2019-10-29 source files
- `analysis_intent`: Explore geographic variation in squirrels in NYC through joins, summarization, and visualization
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_map_model_evaluate_visualize`
- `adaptation_hint`: Reuse for structured datasets where descriptive analysis leads into explanatory or predictive models
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of squirrels in NYC with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Translate the analytical result into geographic views to reveal regional variation and outliers. | Spatial joins or mapping code`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T6 | Modeling and evaluation | lm, glm | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_point, geom_sf | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Analytical summaries with geographic identifiers | Join map geometry or region lookup data | Map-ready plotting table | Display geographic variation`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `prepare_geographic_summary | Aggregate metrics by region and join map geometry or lookup tables | Regional metrics and identifiers | Map-ready data | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `prepare_map_summary(data, region_col, value_col)`
- `plot_geographic_metric(map_data, value_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore geographic variation in squirrels in NYC through joins, summarization, and visualization
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, mapping, modeling, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `7 | prepare_geographic_summary | Aggregate to the geographic unit available in the new dataset and rebuild the map join`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `tennis_tournaments`

- `transcript_title`: Analyzing tennis tournaments in R
- `transcript_file`: `raw-data/inspiration/Analyzing tennis tournaments in R.txt`
- `code_file`: `data-screencasts/grand-slams.Rmd`
- `data_source`: TidyTuesday 2019-04-09 source files
- `analysis_intent`: Explore distributions, group differences, and notable patterns in tennis tournaments through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_trend_compare_visualize`
- `adaptation_hint`: Reuse for messy multi-table datasets that need reshaping, enrichment, and grouped summaries before plotting
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of tennis tournaments with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | spread, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_line | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in tennis tournaments through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `bechdel_test`

- `transcript_title`: Analyzing the Bechdel test in R
- `transcript_file`: `raw-data/inspiration/Analyzing the Bechdel test in R.txt`
- `code_file`: `data-screencasts/2021_03_09_bechdel_test.Rmd`
- `data_source`: TidyTuesday 2021-03-09 dataset
- `analysis_intent`: Predict or estimate outcomes in the Bechdel test using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `pattern_signature`: `load_inspect_reshape_join_tokenize_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for tabular datasets with a clear outcome column, engineered features, and model evaluation needs
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of the Bechdel test with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count, glimpse | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | spread, separate_rows, unnest | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | unnest_tokens, anti_join | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | lm, glm, fit | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Predict or estimate outcomes in the Bechdel test using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `big_mac_index`

- `transcript_title`: Analyzing the Big Mac index in R
- `transcript_file`: `raw-data/inspiration/Analyzing the Big Mac index in R.txt`
- `code_file`: `data-screencasts/2020_12_22_big_mac_index.Rmd`
- `data_source`: TidyTuesday 2020-12-22 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in the Big Mac index through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of the Big Mac index with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count, glimpse | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | pivot_longer | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in the Big Mac index through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `great_american_beer_festival`

- `transcript_title`: Analyzing the Great American Beer Festival
- `transcript_file`: `raw-data/inspiration/Analyzing the Great American Beer Festival.txt`
- `code_file`: `data-screencasts/2020_10_20_beer_awards.Rmd`
- `data_source`: TidyTuesday 2020-10-20 dataset
- `analysis_intent`: Explore and compare language patterns in the Great American Beer Festival using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_reshape_join_tokenize_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of the Great American Beer Festival with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | pivot_wider, unnest, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | bind_log_odds | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | lm, glm | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in the Great American Beer Festival using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, tokenization, term comparison, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `kenya_census`

- `transcript_title`: Analyzing the Kenya census in R
- `transcript_file`: `raw-data/inspiration/Analyzing the Kenya census in R.txt`
- `code_file`: `data-screencasts/2021_01_19_kenya_census.Rmd`
- `data_source`: TidyTuesday 2021-01-19 dataset
- `analysis_intent`: Explore geographic and temporal variation in the Kenya census through joins, summarization, and mapping
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_join_map_trend_compare_visualize`
- `adaptation_hint`: Reuse for geographic datasets with region codes, time fields, and map-ready joins
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of the Kenya census with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Translate the analytical result into geographic views to reveal regional variation and outliers. | Spatial joins or mapping code`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, spread, left_join, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_sf, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Analytical summaries with geographic identifiers | Join map geometry or region lookup data | Map-ready plotting table | Display geographic variation`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `prepare_geographic_summary | Aggregate metrics by region and join map geometry or lookup tables | Regional metrics and identifiers | Map-ready data | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_map_summary(data, region_col, value_col)`
- `plot_geographic_metric(map_data, value_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore geographic and temporal variation in the Kenya census through joins, summarization, and mapping
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, mapping, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `7 | prepare_geographic_summary | Aggregate to the geographic unit available in the new dataset and rebuild the map join`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `golden_age_television`

- `transcript_title`: Analyzing the golden age of television in R
- `transcript_file`: `raw-data/inspiration/Analyzing the golden age of television in R.txt`
- `code_file`: `data-screencasts/golden-age-tv.Rmd`
- `data_source`: TidyTuesday 2019-01-08 source files
- `analysis_intent`: Explore, explain, and model patterns in the golden age of television using engineered features and comparative summaries
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_reshape_join_trend_model_evaluate_visualize`
- `adaptation_hint`: Reuse for structured datasets where descriptive analysis leads into explanatory or predictive models
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of the golden age of television with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, spread, inner_join | Convert messy inputs into analysis-ready tables`
- `T6 | Modeling and evaluation | lm, glm, fit, predict | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_point, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore, explain, and model patterns in the golden age of television using engineered features and comparative summaries
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, reshaping, table joins, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `tidying_phds`

- `transcript_title`: Analyzing tidying and analyzing US PhDs in R
- `transcript_file`: `raw-data/inspiration/Analyzing tidying and analyzing US PhDs in R.txt`
- `code_file`: `data-screencasts/us_phds.Rmd`
- `data_source`: Dataset inferred from us_phds.Rmd
- `analysis_intent`: Explore distributions, group differences, and notable patterns in tidying and analyzing US PhDs through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of tidying and analyzing US PhDs with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | episode-specific dplyr and ggplot verbs | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather, spread | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in tidying and analyzing US PhDs through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `tidytuesday_rstats_tweets`

- `transcript_title`: Analyzing tidytuesday and rstats tweets in R
- `transcript_file`: `raw-data/inspiration/Analyzing tidytuesday and rstats tweets in R.txt`
- `code_file`: `data-screencasts/tidytuesday-tweets.Rmd`
- `data_source`: External sources used in episode: https://github.com/rfordatascience/tidytuesday/blob/master/data/2019/2019-01-01/rstats_tweets.rds?raw=true, https://github.com/rfordatascience/tidytuesday/blob/master/data/2019/2019-01-01/tidytuesday_tweets.rds?raw=true, ...
- `analysis_intent`: Explore and compare language patterns in tidytuesday and rstats tweets using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_scrape_join_tokenize_trend_compare_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of tidytuesday and rstats tweets with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T3 | Transform | Acquire or supplement source data from external web pages or APIs before analysis. | Presence of scraping or external-source code`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_html, count | Establish source shape, units, and comparison candidates`
- `T3 | External acquisition | read_html, GET | Build or enrich the dataset before analysis`
- `T4 | Structuring and enrichment | unnest, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | unnest_tokens, anti_join, bind_tf_idf | Identify terms that distinguish groups or documents`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, geom_line | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Collected | External web or JSON sources | Scrape or request supplemental records | Collected reference tables | Fill gaps not available in the initial source`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `scrape_supporting_reference_data | Pull structured records from HTML or JSON before analysis | External source url and parsing rules | Supplemental reference table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `scrape_reference_table(url, css_selector)`
- `collect_episode_source_records(urls, parser)`
- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in tidytuesday and rstats tweets using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, web or API data collection, table joins, tokenization, term comparison, time-aware comparison, visualization
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `2 | scrape_supporting_reference_data | Rebuild any missing lookup or metadata tables from the relevant external source`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `train_delays_france`

- `transcript_title`: Analyzing train delays in France in R
- `transcript_file`: `raw-data/inspiration/Analyzing train delays in France in R.txt`
- `code_file`: `data-screencasts/french-trains.Rmd`
- `data_source`: TidyTuesday 2019-02-26 source files
- `analysis_intent`: Explore distributions, group differences, and notable patterns in train delays in France through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of train delays in France with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv | Establish source shape, units, and comparison candidates`
- `T6 | Group comparison | group_by, summarize, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_line, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in train delays in France through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `transit_costs`

- `transcript_title`: Analyzing transit costs in R
- `transcript_file`: `raw-data/inspiration/Analyzing transit costs in R.txt`
- `code_file`: `data-screencasts/2021_01_05_transit_costs.Rmd`
- `data_source`: TidyTuesday 2021-01-05 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in transit costs through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of transit costs with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_point, geom_line | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in transit costs through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `volcano_eruptions`

- `transcript_title`: Analyzing volcano eruptions in R
- `transcript_file`: `raw-data/inspiration/Analyzing volcano eruptions in R.txt`
- `code_file`: `data-screencasts/volcano-eruptions.Rmd`
- `data_source`: TidyTuesday 2020-05-12 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in volcano eruptions through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of volcano eruptions with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | gather | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_point | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in volcano eruptions through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `water_access_points`

- `transcript_title`: Analyzing water access points in R
- `transcript_file`: `raw-data/inspiration/Analyzing water access points in R.txt`
- `code_file`: `data-screencasts/2021_05_04_water_access.Rmd`
- `data_source`: TidyTuesday 2021-05-04 dataset
- `analysis_intent`: Explore distributions, group differences, and notable patterns in water access points through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_reshape_trend_compare_visualize`
- `adaptation_hint`: Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of water access points with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T4 | Structuring and enrichment | unnest | Convert messy inputs into analysis-ready tables`
- `T6 | Group comparison | group_by, summarize, count, mutate | Compare categories, time periods, or entities`
- `T7 | Visualization | ggplot, geom_col, geom_point, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore distributions, group differences, and notable patterns in water access points through cleaning, summarization, and visualization
- `analysis_type`: EDA
- `primary_techniques`: schema inspection, grouped summaries, reshaping, time-aware comparison, visualization
- `data_complexity_level`: low-medium
- `reusable_difficulty_score`: 2

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `wealth_income`

- `transcript_title`: Analyzing wealth and income in R
- `transcript_file`: `raw-data/inspiration/Analyzing wealth and income in R.txt`
- `code_file`: `data-screencasts/2021_05_18_salary_survey.Rmd`
- `data_source`: TidyTuesday 2021-05-18 dataset
- `analysis_intent`: Predict or estimate outcomes in wealth and income using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `pattern_signature`: `load_inspect_trend_simulate_model_evaluate_visualize`
- `adaptation_hint`: Reuse for tabular datasets with a clear outcome column, engineered features, and model evaluation needs
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of wealth and income with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates`
- `T6 | Modeling and evaluation | lm, recipe, fit, vfold_cv, tune_grid | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_line | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready`
- `Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Predict or estimate outcomes in wealth and income using cleaned features, exploratory analysis, and model evaluation
- `analysis_type`: Predictive
- `primary_techniques`: schema inspection, grouped summaries, modeling, time-aware comparison, visualization
- `data_complexity_level`: medium
- `reusable_difficulty_score`: 3

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

### `analyzng_scraping_ramen_reviews`

- `transcript_title`: Analyzng scraping and analyzing ramen reviews in R
- `transcript_file`: `raw-data/inspiration/Analyzng scraping and analyzing ramen reviews in R.txt`
- `code_file`: `data-screencasts/ramen-ratings.Rmd`
- `data_source`: TidyTuesday 2019-06-04 source files
- `analysis_intent`: Explore and compare language patterns in scraping and analyzing ramen reviews using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: Modeling
- `pattern_signature`: `load_inspect_scrape_reshape_join_tokenize_model_evaluate_visualize`
- `adaptation_hint`: Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis
- `ker_status`: extracted

Thought Process Map:

- `T1 | Context | Frame the episode as exploratory analysis of scraping and analyzing ramen reviews with limited advance knowledge of the data. | Transcript title and opening context`
- `T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints`
- `T3 | Transform | Acquire or supplement source data from external web pages or APIs before analysis. | Presence of scraping or external-source code`
- `T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd`
- `T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode`
- `T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code`
- `T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow`
- `T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern`

Code Mapping Table:

- `T1 | Data load and inspection | read_csv, read_html, count | Establish source shape, units, and comparison candidates`
- `T3 | External acquisition | read_html, html_nodes, GET | Build or enrich the dataset before analysis`
- `T4 | Structuring and enrichment | gather, unnest, inner_join | Convert messy inputs into analysis-ready tables`
- `T5 | Text comparison | unnest_tokens, anti_join | Identify terms that distinguish groups or documents`
- `T6 | Modeling and evaluation | lm, predict | Test explanatory or predictive relationships after EDA`
- `T7 | Visualization | ggplot, geom_col, geom_point, facet_wrap | Communicate the core result visually`

Data Transformation Flow:

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Collected | External web or JSON sources | Scrape or request supplemental records | Collected reference tables | Fill gaps not available in the initial source`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

Reusable Patterns:

- `inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y`
- `scrape_supporting_reference_data | Pull structured records from HTML or JSON before analysis | External source url and parsing rules | Supplemental reference table | Y`
- `reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y`
- `join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y`
- `compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y`
- `build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y`
- `plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y`

Function Candidates:

- `scrape_reference_table(url, css_selector)`
- `collect_episode_source_records(urls, parser)`
- `reshape_episode_inputs(data, ...)`
- `join_episode_context(primary_data, lookup_data, by)`
- `prepare_text_tokens(data, text_column)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = 'n')`
- `build_predictive_pipeline(data, formula, ...)`
- `evaluate_episode_model(model, test_data, outcome_col)`
- `plot_comparative_story(data, x_col, y_col, group_col = NULL)`

Episode Signature:

- `analysis_intent`: Explore and compare language patterns in scraping and analyzing ramen reviews using tokenization, grouped counts, and discriminative text analysis
- `analysis_type`: Modeling
- `primary_techniques`: schema inspection, grouped summaries, web or API data collection, reshaping, table joins, tokenization, term comparison, modeling, visualization
- `data_complexity_level`: high
- `reusable_difficulty_score`: 5

Adaptation Plan:

- `1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything`
- `2 | scrape_supporting_reference_data | Rebuild any missing lookup or metadata tables from the relevant external source`
- `3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure`
- `4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements`
- `5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents`
- `6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable`
- `8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready`

## Reviewed episodes

### `himalayan_climbers`

- `transcript_title`: Analyzing Himalayan climbers in R
- `transcript_file`: `raw-data/inspiration/Analyzing Himalayan climbers in R.txt`
- `code_file`: `data-screencasts/2020_09_22_himalayan_climbers.Rmd`
- `data_source`: TidyTuesday 2020-09-22 Himalayan climbers data with `peaks`, `expeditions`, and `members`
- `analysis_intent`: Explore expedition outcomes, duration, mortality, and peak-level danger while discovering the dataset structure live
- `analysis_type`: EDA
- `pattern_signature`: `load_inspect_recode_summarize_compare_visualize`
- `adaptation_hint`: Reuse for expedition, journey, incident, or operations datasets with outcome labels, elapsed time, exposure counts, and subgroup risk rates
- `ker_status`: reviewed

Thought Process Map:

- `H1 | Context | Start with minimal prior knowledge and frame the session as live discovery of an unknown Himalayan climbing dataset. | Weekly TidyTuesday topic and transcript opening`
- `H2 | Inspect | Inspect three linked tables, verify what each table represents, and notice missing map-ready fields plus useful peak and expedition fields. | Initial `tt_load()` result with `peaks`, `expeditions`, and `members``
- `H3 | Hypothesis | Generate candidate questions around tallest peaks, successful climbs, climb duration, death rates, and dangerous mountains. | Column scan of peak status, expedition termination reasons, and death counts`
- `H4 | Transform | Recode termination outcomes into usable categories and derive elapsed time to the high point to make comparison possible. | Messy raw expedition outcome fields and dates`
- `H5 | Compare | Aggregate climbs and deaths by peak, then compare raw rates while noticing small-sample instability. | Peak-level summaries and noisy low-count mountains`
- `H6 | Reflect | Shift from raw death rates to empirical Bayes estimates because naive rates overreact to sparse data. | Recognition that small peaks produce misleading extremes`
- `H7 | Visualize | Use peak charts, duration boxplots, uncertainty plots, and Everest decade trends to turn the summaries into interpretable stories. | Prepared peak, expedition, and Everest subsets`
- `H8 | Reflect | Narrow to Everest and test member-level death predictors with a binomial model once the broad EDA identifies a strong focal case. | Everest prominence plus available member-level fields`

Code Mapping Table:

- `H2 | Load / object inspection | `tt_load()`, `rename()`, `count()`, `View()`-style inspection | Understand table roles, key variables, and early constraints`
- `H3 | Peak overview plot | `arrange()`, `slice_head()`, `fct_reorder()`, `geom_col()` | Establish scale, tallest peaks, and unclimbed status`
- `H4 | Expedition outcome preparation | `case_when()`, `str_detect()`, date subtraction in `mutate()` | Convert raw expedition records into reusable success and duration features`
- `H5 | Peak summary construction | `group_by()`, `summarize()`, `across()`, `inner_join()` | Build peak-level climb, member, and mortality summaries`
- `H6 | Rate stabilization | `add_ebb_estimate()` from `ebbr` | Adjust sparse death rates before ranking peaks`
- `H7 | Focused visual comparison | `geom_boxplot()`, `geom_point()`, `geom_errorbarh()`, `geom_line()` | Compare durations, danger, and Everest trends over time`
- `H8 | Member-level modeling | `glm(..., family = "binomial")`, `broom::tidy()` | Estimate which Everest member attributes align with higher death probability`

Data Transformation Flow:

- `Raw | `tt$peaks` | Rename `height_metres` to `height_meters` | Peak table with plotting-ready height field | Standardize naming for downstream use`
- `Raw -> Clean | `tt$expeditions` | Recode `termination_reason` into `success` categories and compute `days_to_highpoint` | Expedition table with normalized outcome and duration features | Make expedition outcomes comparable`
- `Clean -> Analytical | Prepared expeditions | Group by `peak_id`, `peak_name` and summarize climbs, members, deaths, and success rates | `peaks_summarized` | Create group-level risk and activity summaries`
- `Analytical -> Stabilized | `peaks_summarized` | Filter by exposure threshold and apply empirical Bayes estimation | `peaks_eb` | Reduce small-sample noise in death-rate comparisons`
- `Analytical -> Focused | Prepared expeditions | Filter to Everest and aggregate by decade | `everest_by_decade` | Tell a single-entity trend story after the broad scan`
- `Raw -> Modeling | `tt$members` filtered to Everest | Derive role flags and fit binomial model | `tidied` coefficient table | Test member-level death associations`

Reusable Patterns:

- `inspect_multi_table_dataset | Quickly identify table roles, key joins, and missing fields in an unfamiliar weekly dataset | Multi-table list input | Candidate questions and table priorities | Y`
- `recode_sparse_outcomes | Collapse noisy free-text termination states into a small decision-ready outcome taxonomy | Outcome text plus exclusion rules | Comparable outcome labels | Y`
- `summarize_group_risk_rates | Aggregate events, exposure counts, and subgroup deaths for each entity | Event table with counts | Group-level risk summary table | Y`
- `stabilize_sparse_rates | Replace raw rate ranking with empirical Bayes or partial pooling when denominators are uneven | Counts and exposures by group | Noise-adjusted rate estimates and intervals | Y`
- `zoom_from_global_to_case_study | Start broad, find a notable entity, then analyze that entity through time or at member level | Group summary plus focal entity id | Focused subset workflow | Y`

Function Candidates:

- `prepare_expedition_outcomes(data, termination_col, start_date_col, end_date_col)`
- `summarize_group_risk_rates(data, group_cols, exposure_cols, death_cols)`
- `estimate_empirical_bayes_rates(data, event_col, total_col, min_total = 20)`
- `analyze_entity_trend(data, entity_col, time_col, outcome_cols)`

Episode Signature:

- `analysis_intent`: discover what makes peaks dangerous and how expedition outcomes vary across mountains and time
- `analysis_type`: EDA with a modeling tail
- `primary_techniques`: live schema inspection, feature engineering, grouped risk summaries, empirical Bayes shrinkage, case-study deep dive, binomial modeling
- `data_complexity_level`: high
- `reusable_difficulty_score`: 5

Adaptation Plan:

- `1 | inspect_multi_table_dataset | Map each incoming table to entity, event, and participant roles before plotting anything`
- `2 | recode_sparse_outcomes | Replace domain-specific termination text with reusable outcome buckets for success, failure, and missing-like states`
- `3 | summarize_group_risk_rates | Aggregate events and deaths by destination, route, facility, or team instead of by mountain`
- `4 | stabilize_sparse_rates | Use empirical Bayes or another shrinkage method whenever denominators vary sharply across groups`
- `5 | zoom_from_global_to_case_study | After ranking groups, pick one focal entity for time-trend or participant-level follow-up analysis`

### `beyonce_taylor_swift_lyrics`

- `transcript_title`: Analyzing Beyonce and Taylor Swift lyrics in R
- `transcript_file`: `raw-data/inspiration/Analyzing Beyonce and Taylor Swift lyrics in R.txt`
- `code_file`: `data-screencasts/2020_09_29_taylor_swift_beyonce.Rmd`
- `data_source`: TidyTuesday 2020-09-29 `beyonce_lyrics`, `taylor_swift_lyrics`, `sales`, and `charts`
- `analysis_intent`: Compare artist and album language patterns using text analysis while reconciling mismatched source schemas and adding sales context
- `analysis_type`: EDA
- `pattern_signature`: `text_tokenize_compare_tf_idf_log_odds_visualize`
- `adaptation_hint`: Reuse for multi-source text corpora where one dataset needs reshaping or standardization before cross-group vocabulary comparison
- `ker_status`: reviewed

Thought Process Map:

- `B1 | Context | Start with known domain context, expected audience interest, and a plan to compare two artists plus Taylor Swift albums. | Topic familiarity and transcript framing`
- `B2 | Inspect | Inspect all four inputs and immediately notice the key schema mismatch: Beyonce is one row per lyric line while Taylor Swift is one row per song. | Manual `read_csv()` load and early counts`
- `B3 | Hypothesis | Decide to compare sales first for context, then move into text analysis for album and artist-level language differences. | Availability of sales, charts, and lyric text sources`
- `B4 | Transform | Standardize column names, tokenize lyrics, remove stop words, and enrich Taylor Swift tokens with release dates from chart metadata. | Mismatched text formats and missing timeline structure`
- `B5 | Compare | Compare albums within Taylor Swift using tf-idf and weighted log-odds to find distinguishing vocabulary and filler-word shifts. | Prepared album-word counts`
- `B6 | Transform | Harmonize the two artists into a shared artist-song-word structure so they can be compared on common terms. | Need for cross-artist rather than within-artist comparison`
- `B7 | Compare | Use weighted log-odds and usage-rate scatterplots to identify words that most distinguish Beyonce and Taylor Swift. | Shared artist-term counts and totals`
- `B8 | Reflect | Note additional extensions such as sentiment analysis and supervised learning once the descriptive comparisons are established. | Successful completion of core comparison workflow`

Code Mapping Table:

- `B2 | Manual data loading and schema checks | `readr::read_csv()`, `count()`, `distinct()` | Confirm source shape, album coverage, and cross-file comparability`
- `B3 | Sales context | `filter()`, `fct_reorder()`, `geom_col()` | Compare album sales before deeper text work`
- `B4 | Album token preparation | `rename_all()`, `unnest_tokens()`, `anti_join()`, `inner_join()` | Build a clean album-word corpus with release order`
- `B5 | Within-artist text comparison | `bind_tf_idf()`, `bind_log_odds()`, `reorder_within()`, faceting | Surface album-specific vocabulary and stylistic drift`
- `B6 | Cross-artist corpus harmonization | `bind_rows()`, `count()`, `group_by()`, `summarize()` | Create one comparable artist-song-word table`
- `B7 | Cross-artist discriminative comparison | `bind_log_odds()`, `pivot_wider()`, `clean_names()`, log-scale plots | Quantify which words separate the two artists and by how much`

Data Transformation Flow:

- `Raw | `sales` and `charts` | Filter to `US`, `World`, or `WW` and reorder albums by sales | Context tables for popularity comparison | Establish commercial framing before text analysis`
- `Raw -> Clean | `taylor_swift_lyrics` | Lowercase names, drop constant artist column, tokenize lyrics, remove stop words | `taylor_swift_words` corpus base | Normalize song text into comparable terms`
- `Clean -> Enriched | Taylor Swift tokens plus chart metadata | Join `release_dates` and reorder albums chronologically | Album-aware token table | Support across-album comparison`
- `Enriched -> Analytical | Album-word counts | Compute tf-idf and weighted log-odds | `ts_tf_idf` and `ts_lo` | Find album-distinguishing vocabulary`
- `Raw -> Harmonized | Beyonce line-level lyrics plus Taylor song-level lyrics | Rename fields, bind rows, tokenize, and count by artist-song-word | `artist_song_words` | Standardize mismatched corpora for cross-artist comparison`
- `Analytical -> Comparative | Artist-word summaries | Compute weighted log-odds and wide-form usage rates | `word_differences` and `comparison` | Identify artist-distinguishing language patterns`

Reusable Patterns:

- `profile_before_text_analysis | Use non-text metadata first so later text findings have commercial, temporal, or domain context | Metadata tables plus entity ids | Context plots and ranking tables | Y`
- `normalize_mismatched_text_sources | Reconcile corpora with different row granularities before tokenization | Multiple text tables with divergent schemas | Shared text corpus schema | Y`
- `build_time_aware_token_corpus | Add release or time metadata before comparing vocabulary within a creator or series | Text table plus release-date lookup | Chronologically ordered token corpus | Y`
- `compare_group_vocabulary | Use tf-idf and weighted log-odds for within-group and cross-group language contrasts | Group-term counts | Ranked distinguishing terms | Y`
- `visualize_relative_term_usage | Combine odds-based ranking with scatter or ratio plots to interpret effect size and baseline frequency together | Term comparison table | Interpretable comparison visuals | Y`

Function Candidates:

- `prepare_time_aware_tokens(data, text_col, group_col, lookup_table, lookup_key, order_col)`
- `compare_group_vocabulary(data, group_col, term_col, count_col = "n")`
- `build_relative_term_usage_plot(data, x_col, y_col, label_col, total_col)`
- `harmonize_text_sources(primary_data, secondary_data, field_map)`

Episode Signature:

- `analysis_intent`: understand how two superstar artists and Taylor Swift albums differ in vocabulary, style, and commercial context
- `analysis_type`: EDA with text analysis
- `primary_techniques`: schema reconciliation, tokenization, stopword removal, tf-idf, weighted log-odds, cross-source corpus harmonization, comparative plotting
- `data_complexity_level`: medium-high
- `reusable_difficulty_score`: 4

Adaptation Plan:

- `1 | profile_before_text_analysis | Start with non-text metadata such as sales, engagement, or release tables to establish group context`
- `2 | normalize_mismatched_text_sources | Convert each source into the same entity-text schema before comparing vocabulary`
- `3 | build_time_aware_token_corpus | Join release, season, or version metadata so within-group text change can be ordered meaningfully`
- `4 | compare_group_vocabulary | Use tf-idf for within-group distinctiveness and weighted log-odds for head-to-head comparison`
- `5 | visualize_relative_term_usage | Pair ranked term plots with scatter or ratio views so distinctive words are interpretable in context`

## Next steps

- Use `prompts.md` to run the master prompt against each row in `control_table.csv`.
- Write summary metadata back to `control_table.csv` after each extraction pass.
- Append the full episode record to this file.
- Track episodes that go beyond EDA into predictive or modeling work.
- Document new helper functions and the episode patterns they support.
- Identify repeated helper functions and move them into shared R code.
- Keep the KER and prompt pack aligned as the control table evolves.

---

# PRODUCTION KNOWLEDGE REGISTER — ndexr.io Console

Source: `/home/ubuntu/console/src/r/` — production R/Shiny codebase
Date: 2026-04-17

This section captures production patterns that complement the TidyTuesday analytical knowledge.
The analytical track teaches HOW to explore data. The production track teaches HOW to ship it.

---

## PKR-001: Multi-Tenant Shiny Architecture

### Thought Process Map
**Question:** How do you serve multiple apps from a single Shiny process?
**Answer:** Subdomain-based routing via HTTP_HOST header inspection.

### Pattern
```r
# sites_base.r — registry pattern
.SITE_REGISTRY <- list()
add_site <- function(host, ui_fn, server_fn) {
  .SITE_REGISTRY[[host]] <<- list(ui = ui_fn, server = server_fn)
}

# In app.r — dispatch
host <- session$request$HTTP_HOST
site <- .SITE_REGISTRY[[host]]
site$ui(id, data)
```

### Data Transformation Flow
```
HTTP request → nginx (SSL termination) → Shiny container
  → session$request$HTTP_HOST → registry lookup → module dispatch
  → module renders UI + server within ns() isolation
```

### Reusable Pattern
Any Shiny app can serve multiple "sites" from one codebase. Each site is a box module
with ui_ and server_ exports. The router is a named list keyed by hostname.

### WORKS WHEN
- Each subdomain maps to exactly one ui/server pair
- nginx passes the Host header correctly

### FAILS WHEN
- Direct IP access (no Host header)
- New subdomain not registered in the registry

---

## PKR-002: inputs/inputs.r — The Shared Utility Surface

### Thought Process Map
**Question:** How do you avoid duplicating Bootstrap patterns across 50+ R modules?
**Answer:** Centralize into one file (inputs.r) that every module imports.

### Pattern
```r
# In any module:
box::use(../inputs/inputs)

# Use helpers:
inputs$setDefault(value, fallback)
inputs$actionButton(ns("btn"), "Click", class = "btn btn-primary")
inputs$field("Label", inputs$txt(ns, "field", value = ""), class = "col-md-6")
inputs$pan("Loading...")
inputs$modal_transition("Please wait")
```

### Key Decisions
- `setDefault()` replaces ALL null-coalesce patterns (no %||%, no if/else)
- `actionButton()` always adds `action-button` class (raw tags$button breaks Shiny binding)
- Form helpers (txt, sel, num) use `form-control-sm` by default (saves screen space)
- `create_tabset_panel(sidebar=TRUE)` — only ONE level of sidebar allowed

### Reusable Pattern
Every production Shiny app benefits from a single utility file that wraps:
- Null handling
- Form controls (with consistent sizing)
- Modals (loading, error, info)
- Notifications (toast)
- Layout builders (tabs, cards, accordions)

### WORKS WHEN
- Entire team uses the same helpers consistently
- Helpers are Bootstrap-aligned (no custom CSS needed)

### FAILS WHEN
- Helper grows to cover edge cases that should be inline
- Helper only used once (inline it or delete it)

---

## PKR-003: State Management (Storr + Postgres)

### Thought Process Map
**Question:** How do you persist arbitrary R objects per-user across sessions?
**Answer:** Dual storage: storr_dbi (serialized R objects) + Postgres (relational).

### Pattern
```r
# Store arbitrary R object by key:
state$store_state(ns_common_store_user("rbox_init"), reactiveValuesToList(input))

# Retrieve:
saved <- state$get_state(ns_common_store_user("rbox_init"))
# Returns list() on error (never crashes)

# Relational (login tracking):
postgres$table_create_or_upsert(
  data.frame(email = user$email, status = "active"),
  where_cols = "email"
)
```

### Data Transformation Flow
```
User action → reactiveValuesToList(input) → JSON serialization
  → storr_dbi INSERT (key = ns_common_store_user("module_name"))
  → Postgres table (tblData/tblKeys)

Next session → storr_dbi GET → deserialize → populate input defaults
```

### WORKS WHEN
- Need to remember form state, preferences, or config across sessions
- Per-user isolation via namespace keys

### FAILS WHEN
- Object too large for serialization
- Namespace key collision (always use ns_common_store_user)

---

## PKR-004: AWS Client Factory (Reticulate + Boto3)

### Thought Process Map
**Question:** How does an R app talk to AWS services?
**Answer:** Python boto3 via reticulate, with per-user credentials from secret store.

### Pattern
```r
# Create client with user's stored credentials:
ec2 <- client$client("ec2", ns_common_store_user = data$ns_common_store_user)

# Use it like Python boto3:
instances <- ec2$describe_instances()
keypairs <- ec2$describe_key_pairs()

# For services that need specific regions:
route53 <- client$client("route53domains", ns_common_store_user = ns, region = "us-east-1")
```

### Key Decision
R doesn't have a production-grade AWS SDK. Using reticulate + boto3 gives full AWS coverage
without maintaining R wrappers for every service.

### WORKS WHEN
- reticulate Python env is configured with boto3
- User has stored AWS credentials via the secrets module

### FAILS WHEN
- Python env not initialized
- Credentials expired or missing
- Wrong region for region-specific services

---

## PKR-005: Authentication Flow (Google OAuth + Cognito)

### Thought Process Map
**Question:** How do you authenticate users in a deployed Shiny app?
**Answer:** Google OAuth 2.0 code flow (deployed) or AWS Cognito (interactive/local).

### Pattern
```r
# Deployed path (login_user.r → login_auth):
# 1. Check cookies for existing session
# 2. If no cookie: redirect to Google OAuth
# 3. Exchange auth code for access token
# 4. Fetch userinfo from Google API
# 5. Store user JSON in cookie (30-min TTL)
# 6. Call login_processing() for post-auth setup

# Post-auth (login_processing.r):
# 1. Log login event to Postgres
# 2. Set up per-user namespace (shiny$NS(email))
# 3. Fetch AWS resources (EC2, SG, keypairs, Route53)
# 4. Check Stripe subscription status
# 5. Determine admin flag
# 6. Return enriched session object
```

### WORKS WHEN
- App is behind nginx with HTTPS
- .googauth credentials file present
- Google OAuth redirect URIs configured correctly

### FAILS WHEN
- redirect_uri mismatch between Google console and app
- Cookie domain/path mismatch
- Cognito path: login_user() missing box::use import (currently broken)

---

## PKR-006: Docker Deploy Pipeline

### Thought Process Map
**Question:** How do you deploy changes to a live R/Shiny app?
**Answer:** Docker Compose build + scale pattern.

### Pattern
```bash
cd /home/ubuntu/console

# Full deploy:
npm run build          # docker compose build (all services)
npm run down           # docker compose down
npm run up             # docker compose up -d
npm run scale:console  # docker compose scale console=10

# Or all at once:
npm run build && npm run down && npm run up && npm run scale:console
```

### Data Transformation Flow
```
Code change → docker compose build (Dockerfile: rocker/verse + renv::restore())
  → new image with updated R code
  → docker compose down (stop old containers)
  → docker compose up -d (start new containers)
  → docker compose scale console=10 (10 instances behind nginx)
  → nginx upstream auto-discovers new containers
```

### Key Decision
renv.lock is copied into the Docker image. Package installation happens at build time,
not runtime. This makes container startup fast and reproducible.

### WORKS WHEN
- renv.lock is up to date (renv::snapshot() before build)
- System deps declared in Dockerfile (libpq, libxml2, gdal, etc.)

### FAILS WHEN
- renv.lock out of sync with actual imports
- System library missing for a new R package
- Git pull fails (SSH key issue) — skip pull, build from local

---
