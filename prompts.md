# Function Builder Prompt Pack

This prompt pack defines the controlled prompt structure for turning transcript intent, code, and data pairs into reusable R functions in the `sa-tidy-tuesday` workspace.

## Metadata

| Field | Value |
|-------|-------|
| Project | Data Screencast Transcript Intent Functions |
| Repository | `c:\Users\mstoian\R\sa-tidy-tuesday` |
| Status | Prompt contract for control-table-driven extraction |
| Date | 2026-04-16 |
| Purpose | Drive reusable R function extraction from screencast transcript, code, and data relationships |

## Purpose

Use these prompts to analyze each transcript, the matched R Markdown code, and the underlying dataset, then extract reusable reasoning patterns for future datasets.

## Control table contract

`control_table.csv` is the work queue for the project, not just a lookup table. Each row represents one episode and should carry the minimum metadata needed to iterate the extraction workflow.

Recommended columns:

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

Column roles:

- Keep `transcript_title`, `transcript_file`, `code_file`, and `function_name` as the row identity.
- Store concise reusable metadata in the control table.
- Store long-form outputs such as thought maps, code mapping tables, and transformation flows in `knowledge register.md`.

Suggested `ker_status` values:

- `needs_mapping`
- `mapped`
- `extracted`
- `implemented`
- `reviewed`

## Iteration loop

Use the control table row by row:

1. Select the next row from `control_table.csv` where `ker_status` is not `reviewed`.
2. Read the transcript file, matched `code_file`, and the dataset evidence from the Rmd.
3. Run the master prompt in this file against that row.
4. Write back summary metadata to `control_table.csv`:
   - `data_source`
   - `analysis_intent`
   - `analysis_type`
   - `pattern_signature`
   - `adaptation_hint`
   - `ker_status`
5. Append the full episode output to `knowledge register.md`.
6. Update stubs or implementations in `R/` when a reusable function is identified.

## How to use

1. Start with `control_table.csv` to identify the transcript, code pair, and target function name.
2. Use `knowledge register.md` to capture the full episode-level reasoning, reusable patterns, and transfer notes.
3. Apply the prompt pack below to extract intent, categorize the analysis, and produce a function implementation plan.
4. Store summary metadata in `control_table.csv`, store long-form reasoning in `knowledge register.md`, and implement the resulting stubs in `R/screencast_intent_stubs.R` or selected episode implementations in `R/screencast_implementations.R`.

## Prompt contract format

Every controlled prompt should include:

1. Module
2. Job
3. Reads from
4. Produces
5. Constraints

If the prompt cannot be written this way, it is too vague.

## Recommended sequence

1. Map transcript, code, and data
2. Extract episode intent
3. Identify reusable EDA and modeling patterns
4. Generate function stubs and signatures
5. Transfer learned patterns to new datasets
6. Maintain the knowledge repository

---

## PROMPT 1 - Map transcript, code, and data

**Module:** dataset mapping

**Job:** confirm the correct mapping between transcript text, screencast code, and the dataset used by the episode.

**Reads from:**

- `control_table.csv`
- `raw-data/inspiration/*.txt`
- `data-screencasts/*.Rmd`

**Produces:**

- confirmed `transcript_file`, `code_file`, and `data_source`
- updated `control_table.csv` with exact data source or dataset name
- episode notes for ambiguous or approximate mappings

**Constraints:**

- preserve exact transcript titles
- infer the data source only from code or transcript evidence
- do not create mappings when the dataset is unknown

---

## PROMPT 2 - Extract transcript intent

**Module:** intent extraction

**Job:** identify the main analysis question or story behind each transcript and match it to the R code behavior.

**Reads from:**

- `control_table.csv`
- `raw-data/inspiration/*.txt`
- `data-screencasts/*.Rmd`

**Produces:**

- `analysis_intent` text for each episode
- `analysis_type` category such as `EDA`, `Visualization`, `Data Cleaning`, `Predictive`, `Modeling`, `Scraping`, or `Summary`
- updated episode metadata in `control_table.csv`

**Constraints:**

- preserve the transcript wording where possible
- infer intent only from the transcript and code
- do not assign predictive labels unless the code includes modeling behavior

---

## PROMPT 3 - Identify reusable EDA and helper patterns

**Module:** pattern extraction

**Job:** analyze code for repeated behavior and capture reusable helper functions for future episodes.

**Reads from:**

- `data-screencasts/*.Rmd`
- `raw-data/inspiration/*.txt`
- `R/screencast_intent_stubs.R`
- `knowledge register.md`

**Produces:**

- a list of reusable EDA helper functions
- generalizable code patterns for loading, cleaning, summarizing, and visualizing data
- a set of episode tags that follow the same workflow patterns

**Constraints:**

- focus on behavior across multiple episodes
- capture function intent rather than file-specific details
- generalize inputs and outputs to support new datasets

---

## PROMPT 4 - Build function stubs from episode intent

**Module:** function generation

**Job:** create or update reusable R function stubs that reflect the transcript intent and matched code.

**Reads from:**

- `control_table.csv`
- `knowledge register.md`
- `R/intents.R`
- `R/screencast_intent_stubs.R`

**Produces:**

- generated R function stubs with clear names and signatures
- stub comments documenting transcript intent, dataset, analysis type, and matched code file
- updated `R/screencast_intent_stubs.R`

**Constraints:**

- use consistent naming conventions across functions
- map each function to a single transcript intent
- leave implementation details as TODOs when the episode is not fully coded yet

---

## PROMPT 5 - Identify predictive or modeling episodes

**Module:** predictive episode identification

**Job:** flag episodes where the code moves beyond descriptive EDA into predictive or modeling analysis.

**Reads from:**

- `raw-data/inspiration/*.txt`
- `data-screencasts/*.Rmd`
- `control_table.csv`

**Produces:**

- episodes tagged as `Predictive` or `Modeling`
- a short summary of the predictive objective
- recommended helper function names for model training and evaluation

**Constraints:**

- only tag episodes when the code clearly supports modeling or prediction
- keep predictive labels distinct from descriptive analysis
- preserve the dataset intent

---

## PROMPT 6 - Transfer learned patterns to a new dataset

**Module:** transfer learning

**Job:** use prior episode patterns to propose a reusable function for a new dataset or transcript.

**Reads from:**

- `control_table.csv`
- `knowledge register.md`
- `R/screencast_intent_stubs.R`
- new dataset metadata or transcript summary

**Produces:**

- a proposed function signature for the new dataset
- a reusable analysis workflow plan based on prior episodes
- references to existing helper functions to reuse

**Constraints:**

- base the proposal on learned patterns
- do not assume the new dataset shares the same schema as previous episodes
- focus on intent and behavior rather than exact variable names

---

## PROMPT 7 - Maintain the KER and prompt pack

**Module:** knowledge repository maintenance

**Job:** keep the knowledge register and prompt pack aligned with the actual transcript/code repository.

**Reads from:**

- `control_table.csv`
- `knowledge register.md`
- `prompts.md`
- `R/screencast_intent_stubs.R`

**Produces:**

- updated guidance for using the KER and prompt pack
- a list of missing episode mappings or unmatched code-only files
- versioned notes on new episodes and function patterns
- documented new shared helper functions discovered during episode implementation

**Constraints:**

- keep the KER and prompt pack in sync
- explicitly track both EDA and predictive behavior
- do not blur the line between current mapped episodes and future roadmap

---

## MASTER PROMPT - Thought -> Code -> Data Extraction Engine

**Module:** Cognitive Pattern Extraction Engine

**Job:** analyze the author's screencast transcript, narration, and R Markdown code together to extract:

1. the thinking process
2. the data manipulation logic
3. the reusable analytical patterns

Then convert these into reusable functions and transferable workflows for future episodes.

**Reads from:**

- transcript text (raw narration or screencast)
- R Markdown code (`data-screencasts/*.Rmd`)
- dataset(s) used in the episode
- existing knowledge register (`knowledge register.md`)
- `control_table.csv` mapping

**Produces:**

1. Structured Thought Process Map
2. Code-to-Thought Mapping
3. Data Transformation Graph
4. Reusable Function Candidates
5. Episode Pattern Signature
6. Adaptation Blueprint for next dataset

**Constraints:**

- do not describe code line by line
- focus on reasoning -> transformation -> reuse
- generalize variable names
- capture why decisions were made
- prefer reusable abstractions over episode-specific logic

### Step 1 - Extract thought process

From the transcript, identify:

- initial framing
- observations
- explicit and implicit questions
- decision points
- iterations

Output:

`Thought_ID | Step_Type | Description | Trigger`

Allowed `Step_Type` values:

- `Context`
- `Inspect`
- `Hypothesis`
- `Transform`
- `Compare`
- `Visualize`
- `Reflect`

### Step 2 - Map thought to code

From the Rmd, link each code block to a `Thought_ID`.

Output:

`Thought_ID | Code_Block | Function_Used | Purpose`

Constraints:

- map intent, not just syntax
- group repeated patterns such as `count -> mutate -> ggplot`

### Step 3 - Extract data transformations

Track how data evolves:

- raw
- clean
- structured
- analytical
- visual

Output:

`Stage | Input | Operation | Output | Purpose`

Include:

- joins
- reshaping
- tokenization
- aggregation

### Step 4 - Identify reusable patterns

Detect repeated logic such as:

- load -> inspect -> count
- tokenize -> remove stopwords
- compare groups with tf-idf or log-odds
- reorder factors for visualization

Output:

`Pattern_Name | Description | Inputs | Outputs | Reusable (Y/N)`

### Step 5 - Generate function candidates

Convert repeated patterns into functions.

Output:

`function_name`

- `purpose`
- `inputs`
- `outputs`
- `steps`
- `dependencies`

Example candidates:

- `prepare_text_tokens(data, text_column)`
- `compute_log_odds(data, group_col, feature_col)`

### Step 6 - Episode signature

Summarize the episode as:

- `analysis_intent`
- `analysis_type`
- `primary_techniques`
- `data_complexity_level`
- `reusable_difficulty_score`
- `pattern_signature`

### Step 7 - Adaptation blueprint

Given a new dataset, map previous episode patterns to the new schema.

Output:

`Step | Reused Pattern | Adaptation Required`

Then propose:

- `function_name`
- `based_on_patterns`
- `required_changes`

### Final output format

1. Thought Process Map
2. Code Mapping Table
3. Data Transformation Flow
4. Reusable Patterns
5. Function Candidates
6. Episode Signature
7. Adaptation Plan

---

## Control-table-driven execution protocol

When running the master prompt, always start from one row in `control_table.csv`.

Use the row fields this way:

- `transcript_file` gives the transcript input
- `code_file` gives the Rmd input
- `function_name` gives the reusable function target
- `notes` carries mapping caveats
- `data_source`, `analysis_intent`, `analysis_type`, `pattern_signature`, `adaptation_hint`, and `ker_status` are updated after extraction

Minimal write-back rules:

- Write concise summary fields to `control_table.csv`
- Write the full thought, code, transformation, and adaptation outputs to `knowledge register.md`
- Move `ker_status` forward one step after each pass

Recommended transition:

1. `needs_mapping` -> `mapped`
2. `mapped` -> `extracted`
3. `extracted` -> `implemented`
4. `implemented` -> `reviewed`

---

## Architecture notes

- `control_table.csv` = iteration queue and compact metadata layer
- `knowledge register.md` = long-form semantic memory
- `Patterns` = transformation templates and workflow signatures
- `Functions` = execution layer in R
- `Prompt` = orchestration layer that maps thought to code

This is a "dbt for human thinking" workflow: capture the reasoning, standardize the pattern, and then generate reusable analysis code from it.
