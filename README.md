# sa-tidy-tuesday

A structured knowledge-extraction system built on top of the [TidyTuesday](https://github.com/rfordatascience/tidytuesday) screencasts — turning episode transcripts, code, and datasets into a reusable library of R analysis patterns.

---

## What this is

Each week, TidyTuesday releases a new dataset and the community explores it live. This repo takes those screencasts and does something more deliberate: it extracts the **reasoning patterns** behind the code — how data gets loaded, reshaped, joined, modelled, and visualised — and captures them as reusable, documented R functions.

The result is a structured knowledge register that grows one episode at a time, covering everything from EDA and text analysis to predictive modelling and bootstrapping.

---

## Structure

```
sa-tidy-tuesday/
├── R/
│   ├── screencast_helpers.R          # Shared helpers (incl. local-first data loader)
│   ├── screencast_implementations.R  # Implemented episode functions
│   ├── screencast_intent_stubs.R     # Auto-generated stubs for all mapped episodes
│   └── intents.R                     # Control-table utilities
├── output/
│   ├── episodes/                     # One folder per episode: guide, R script, manifest
│   ├── super_qmd/                    # Cognition-first guided analysis documents
│   └── reproduction_index.csv        # Flat queue summary for automation
├── control_table.csv                 # Master mapping: transcripts → functions → status
├── knowledge register.md             # Long-form intent, patterns, and adaptation hints
├── prompts.md                        # Extraction prompt pack
└── build_*.py / build_*.ps1          # Automation scripts
```

---

## Episodes

80 episodes processed and counting, spanning datasets across sport, culture, science, and policy.

| Status | Count |
|---|---|
| Ready (local data) | 57 |
| Ready (external steps needed) | 5 |
| Needs external sources | 16 |
| Needs data review | 1 |

A sample of what's covered:

- African American achievements & history
- Predicting horror movie ratings
- GDPR violations (EDA + trend analysis)
- Beyoncé & Taylor Swift lyrics (text analysis)
- Bird collision bootstrapping
- Board games, coffee ratings, college income, Broadway shows, and more

Each episode folder under `output/episodes/` contains:
- a step-by-step reproduction guide
- an extracted R script
- a structured manifest (analysis intent, pattern signature, required packages, data files)

---

## The Control Table

`control_table.csv` is the backbone of the system. Every row is an episode with fields for:

- transcript and code file paths
- extracted function name
- analysis intent and type (EDA vs predictive)
- pattern signature (e.g. `load_inspect_reshape_join_trend_compare_visualize`)
- adaptation hints for applying the pattern to new datasets
- extraction status (`needs_mapping` → `mapped` → `extracted` → `implemented` → `reviewed`)

---

## Key Workflows

**Load TidyTuesday data locally** (avoids GitHub PAT):
```r
load_tidyweek_data("2020-04-21")
```

**Regenerate intent stubs from control table:**
```powershell
./build_intent_stubs.ps1
```

**Batch-generate knowledge register entries:**
```bash
py -3 build_ker_entries.py
```

**Generate a super QMD guided analysis doc:**
```bash
py -3 build_super_qmd.py --queue-position 31
```

---

## Data

The `tidytuesday/data/` folder is excluded from this repo (large dataset mirror). Clone the [TidyTuesday repo](https://github.com/rfordatascience/tidytuesday) alongside this one and the local loader will find the data automatically.

---

## Goals

- Capture the *reasoning* behind EDA and predictive workflows, not just the syntax
- Build a searchable library of R patterns indexed by dataset type and analytical intent
- Make it easy to adapt prior episode knowledge to new datasets and screencasts
- Produce cognition-first documents that bridge reproduction and guided analysis
