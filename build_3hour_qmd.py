"""
build_3hour_qmd.py — Generate 3-hour episode QMDs for TheDataShrink™ marathon.

For each episode in output/episodes/, generates three Quarto documents:
  h1_eda_<fn>.qmd          — Hour 1: EDA (reproduce + extend David's work)
  h2_modeling_<fn>.qmd     — Hour 2: Modeling (go deeper)
  h3_communicate_<fn>.qmd  — Hour 3: Communication (Quarto/Shiny/D3, publishable online)

TheDataShrink™ concept system:
  - Each QMD includes FAILS_WHEN + WORKS_WHEN callout blocks
  - Atomic concepts listed as cross-reference anchors
  - Brand: TheDataShrink™

Usage:
  python3 build_3hour_qmd.py                    # all episodes
  python3 build_3hour_qmd.py --episode 001      # single episode by prefix
  python3 build_3hour_qmd.py --hour h1          # only h1_eda for all episodes
  python3 build_3hour_qmd.py --force            # overwrite existing
"""

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EPISODES_ROOT = ROOT / "output" / "episodes"

BRAND = "TheDataShrink™"
BRAND_URL = "https://thedatashrink.com.au"
BRAND_TAGLINE = "Data stories worth sharing."


# ─── Template helpers ────────────────────────────────────────────────────────

def yaml_header(title: str, subtitle: str, hour: str) -> str:
    theme_map = {"h1": "flatly", "h2": "cosmo", "h3": "litera"}
    theme = theme_map.get(hour, "flatly")
    return f"""---
title: "{title}"
subtitle: "{subtitle}"
author: "{BRAND}"
date: today
format:
  html:
    theme: {theme}
    toc: true
    toc-depth: 3
    code-fold: show
    code-summary: "Show code"
    number-sections: true
    embed-resources: true
execute:
  echo: true
  warning: false
  message: false
editor: visual
---
"""


def brand_header(fn: str) -> str:
    return f"""
::: {{.callout-tip}}
## {BRAND} — {BRAND_TAGLINE}
Episode: `{fn}` | [All episodes]({BRAND_URL}/tidytuesday) | [YouTube](#) | [Instagram](#)
:::

"""


def concept_callout(concepts: list[str]) -> str:
    if not concepts:
        return ""
    concept_list = "\n".join(f"- `{c}`" for c in concepts)
    return f"""
::: {{.callout-note collapse="true"}}
## TheDataShrink™ Concept Index
These reusable concepts are demonstrated in this episode. See `CONCEPT_INDEX.md`.

{concept_list}
:::

"""


def fails_works_callout(fails: list[str], works: list[str]) -> str:
    fails_md = "\n".join(f"- {f}" for f in fails) if fails else "- No specific failure conditions identified"
    works_md = "\n".join(f"- {w}" for w in works) if works else "- Generally applicable"
    return f"""
::: {{.callout-warning collapse="true"}}
## FAILS WHEN
{fails_md}
:::

::: {{.callout-important collapse="true"}}
## WORKS WHEN
{works_md}
:::

"""


def r_chunk(label: str, code: str, eval_chunk: bool = False) -> str:
    eval_str = "true" if eval_chunk else "false"
    return f"""
```{{r}}
#| label: {label}
#| eval: {eval_str}
{code.strip()}
```
"""


# ─── Hour 1: EDA ─────────────────────────────────────────────────────────────

def build_h1(data: dict, folder: Path, force: bool) -> Path:
    fn = data["function_name"]
    title_raw = data.get("transcript_title", fn)
    out_path = folder / f"h1_eda_{fn}.qmd"

    if out_path.exists() and not force:
        print(f"  SKIP (exists): {out_path.name}")
        return out_path

    arch = data.get("hour_architecture", {}).get("h1_eda", {})
    steps = arch.get("steps", [])
    steps_md = "\n".join(f"- [ ] {s}" for s in steps)

    transcript_preview = ""
    tf = data.get("source_files", {}).get("transcript_file", "")
    if tf:
        tp = ROOT / tf
        if tp.exists():
            raw = tp.read_text(encoding="utf-8", errors="ignore")
            transcript_preview = raw[:600].replace("`", "'") + "..."

    data_files = data.get("local_data_files", [])
    data_load_code = ""
    if data_files:
        data_load_code = "# Local TidyTuesday data\n"
        for df in data_files[:3]:
            varname = Path(df).stem.replace("-", "_")
            data_load_code += f'{varname} <- read_csv(here::here("{df}"))\n'
    else:
        ds = data.get("data_source", "")
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", ds)
        if date_match:
            data_load_code = f'tt <- tidytuesdayR::tt_load("{date_match.group(1)}")\n'
        else:
            data_load_code = "# TODO: load data for this episode\n"

    packages = data.get("required_packages", [])
    pkg_code = "\n".join(f"library({p})" for p in sorted(set(["tidyverse", "here"] + packages)))

    features = data.get("features", {})
    extension_ideas = []
    if features.get("time"):
        extension_ideas.append("Add a rolling 12-month average to smooth the trend line")
    if features.get("text_analysis"):
        extension_ideas.append("Compute log-odds ratio between the two largest groups")
    if features.get("joins"):
        extension_ideas.append("Enrich with a population denominator to produce per-capita rates")
    if features.get("maps"):
        extension_ideas.append("Add a second map showing year-over-year change (delta choropleth)")
    if not extension_ideas:
        extension_ideas = [
            "Reorder factor levels by median rather than alphabetical",
            "Add 95% confidence intervals to group comparisons using broom::tidy()",
        ]
    ext_md = "\n".join(f"- {e}" for e in extension_ideas)

    content = yaml_header(
        title=f"Hour 1 — EDA: {title_raw}",
        subtitle=f"Reproduce + extend David Robinson's original analysis | {BRAND}",
        hour="h1",
    )
    content += brand_header(fn)
    content += concept_callout(data.get("atomic_concepts", []))
    content += fails_works_callout(data.get("fails_when", []), data.get("works_when", []))
    content += f"""
## Episode Context

- **Original:** `{title_raw}`
- **Analysis type:** `{data.get("analysis_type", "EDA")}`
- **Pattern:** `{data.get("pattern_signature", "")}`
- **Data:** {data.get("data_source", "TidyTuesday")}
- **Hour 1 goal:** Reproduce David's core story, then extend with one new angle

::: {{.callout-note collapse="true"}}
## Original Transcript (preview)
```
{transcript_preview}
```
:::

## Hour 1 Checklist
{steps_md}

## Setup
"""
    content += r_chunk("setup", pkg_code, eval_chunk=False)
    content += "\n## Load Data\n"
    content += r_chunk("load-data", data_load_code, eval_chunk=False)
    content += f"""
## Schema Inspection

```{{r}}
#| label: inspect
#| eval: false
# What columns do we have? What are the types? What is the grain?
glimpse(YOUR_DATA_HERE)
skimr::skim(YOUR_DATA_HERE)
```

## Core EDA

> Reproduce David's 3-4 key charts here. Follow the pattern_signature:
> `{data.get("pattern_signature", "")}`

```{{r}}
#| label: eda-core
#| eval: false
# YOUR EDA CODE HERE
# Follow the episode_source.R in this folder as your scaffold
```

## Extension: One New Angle

{ext_md}

```{{r}}
#| label: eda-extension
#| eval: false
# YOUR EXTENSION CODE HERE
```

## Hour 1 Narrative

> Write 150 words: what does the data show? One sentence per chart.
> This becomes the YouTube intro and Instagram carousel slide 2.

*[Write narrative here]*

## Next Steps

- Hour 2: `h2_modeling_{fn}.qmd` — go deeper with a model
- Hour 3: `h3_communicate_{fn}.qmd` — publish to {BRAND}
"""

    out_path.write_text(content, encoding="utf-8")
    print(f"  WRITE: {out_path.name}")
    return out_path


# ─── Hour 2: Modeling ─────────────────────────────────────────────────────────

def build_h2(data: dict, folder: Path, force: bool) -> Path:
    fn = data["function_name"]
    title_raw = data.get("transcript_title", fn)
    out_path = folder / f"h2_modeling_{fn}.qmd"

    if out_path.exists() and not force:
        print(f"  SKIP (exists): {out_path.name}")
        return out_path

    arch = data.get("hour_architecture", {}).get("h2_modeling", {})
    steps = arch.get("steps", [])
    steps_md = "\n".join(f"- [ ] {s}" for s in steps)
    atype = data.get("analysis_type", "EDA")

    if atype in ("Predictive", "Modeling"):
        modeling_scaffold = """
## Feature Engineering

```{r}
#| label: features
#| eval: false
# Build features from EDA findings
# Use recipes::recipe() to encode categoricals and impute
```

## Train / Test Split

```{r}
#| label: split
#| eval: false
library(tidymodels)
set.seed(42)
split <- initial_split(data, prop = 0.8, strata = outcome)
train <- training(split)
test  <- testing(split)
folds <- vfold_cv(train, v = 5, strata = outcome)
```

## Baseline Model

```{r}
#| label: baseline
#| eval: false
# Fit a simple linear/logistic model as the baseline
# Compare to null model AUC / RMSE
```

## Tuned Model (LASSO / XGBoost)

```{r}
#| label: tuned-model
#| eval: false
# Use tune_grid() or tune_bayes() to find optimal hyperparameters
```

## Model Interpretation

```{r}
#| label: vip
#| eval: false
library(vip)
# Variable importance plot
# SHAP values if tree model
```
"""
    elif "text" in data.get("pattern_signature", "").lower() or data.get("features", {}).get("text_analysis"):
        modeling_scaffold = """
## TF-IDF Comparison

```{r}
#| label: tfidf
#| eval: false
library(tidytext)
# bind_tf_idf() on grouped token counts
```

## Log-Odds Ratio

```{r}
#| label: log-odds
#| eval: false
library(tidylo)
# bind_log_odds() for statistically grounded group comparison
```

## Topic Model (optional)

```{r}
#| label: topic-model
#| eval: false
library(stm)
# Fit STM / LDA if corpus is large enough
# k = 5-10 topics, display top terms per topic
```
"""
    else:
        modeling_scaffold = """
## Statistical Model

```{r}
#| label: model
#| eval: false
# Fit linear model on main numeric outcome
# Use broom::tidy() + broom::glance() for clean output
```

## Bootstrap Confidence Intervals

```{r}
#| label: bootstrap
#| eval: false
library(rsample)
# boot <- bootstraps(data, times = 1000)
# Calculate statistic of interest, extract CI
```

## Interaction Effects

```{r}
#| label: interaction
#| eval: false
# Test top 2 grouping variable interactions
# Plot with interaction plots or faceted model output
```
"""

    content = yaml_header(
        title=f"Hour 2 — Modeling: {title_raw}",
        subtitle=f"Go deeper with statistics and models | {BRAND}",
        hour="h2",
    )
    content += brand_header(fn)
    content += concept_callout(data.get("atomic_concepts", []))
    content += fails_works_callout(data.get("fails_when", []), data.get("works_when", []))
    content += f"""
## Episode Context

- **Analysis type:** `{atype}` — this shapes the modeling approach below
- **Pattern:** `{data.get("pattern_signature", "")}`
- **Hour 2 goal:** Go deeper than David went in the original screencast

## Hour 2 Checklist
{steps_md}

{modeling_scaffold}

## Model Story

> What does the model reveal that raw EDA couldn't?
> One paragraph for the YouTube "deep dive" section.

*[Write model narrative here]*

## Cross-Reference

- [← Hour 1 EDA](h1_eda_{fn}.qmd)
- [Hour 3 Communicate →](h3_communicate_{fn}.qmd)
"""

    out_path.write_text(content, encoding="utf-8")
    print(f"  WRITE: {out_path.name}")
    return out_path


# ─── Hour 3: Communicate ─────────────────────────────────────────────────────

def build_h3(data: dict, folder: Path, force: bool) -> Path:
    fn = data["function_name"]
    title_raw = data.get("transcript_title", fn)
    out_path = folder / f"h3_communicate_{fn}.qmd"

    if out_path.exists() and not force:
        print(f"  SKIP (exists): {out_path.name}")
        return out_path

    arch = data.get("hour_architecture", {}).get("h3_communicate", {})
    steps = arch.get("steps", [])
    steps_md = "\n".join(f"- [ ] {s}" for s in steps)
    ds = data.get("data_source", "TidyTuesday dataset")

    content = yaml_header(
        title=f"Hour 3 — Communicate: {title_raw}",
        subtitle=f"From analysis to publication | {BRAND}",
        hour="h3",
    )
    content += brand_header(fn)
    content += f"""
## Publication Goal

Turn the EDA + modeling work into content publishable under **{BRAND}**:

| Channel | Format | Goal |
|---------|--------|------|
| YouTube | 15-20 min video | Full walkthrough, show code |
| Instagram | 5-slide carousel | Hook → Data → Insight → Method → CTA |
| Facebook | Text post + hero chart | 3 bullet insights + link |
| Website | Quarto HTML page | Embedded interactive, SEO-optimised |

## Hour 3 Checklist
{steps_md}

## Hero Chart (1200×628)

> The single best chart from Hour 1 or 2, sized for social sharing.

```{{r}}
#| label: hero-chart
#| eval: false
#| fig-width: 12.5
#| fig-height: 6.54
# YOUR HERO CHART CODE HERE
# Save with ggsave("hero_{fn}.png", width = 12.5, height = 6.54, dpi = 150)
```

## Instagram Carousel Copy

**Slide 1 — Hook**
> "What does {ds} tell us? 🧵"

**Slide 2 — Data**
> [Key finding #1 in one sentence]

**Slide 3 — Insight**
> [The surprising thing the data revealed]

**Slide 4 — Method**
> "Built in R with tidyverse + [main packages]. Code at {BRAND_URL}"

**Slide 5 — CTA**
> "Full analysis on YouTube 👆 Follow @thedatashrink for weekly data stories"

## YouTube Chapter Timestamps

```
0:00 Intro — What question are we asking?
2:00 Load the data
5:00 EDA — Key patterns
12:00 Modeling — Going deeper
18:00 What does this mean?
20:00 Wrap up + next week
```

## Interactive Element (Shiny / Observable)

```{{r}}
#| label: interactive
#| eval: false
library(shiny)
# OR: use ojs_define() + Observable JS for zero-server interactivity

# Minimal Shiny: one selectInput to filter by group, one reactive ggplot
# Embed in Quarto with: shiny::shinyApp(ui, server)
```

## SEO Metadata

```yaml
# Add to Quarto YAML for the published page:
description: "{title_raw} — a {BRAND} data story"
keywords: ["R", "TidyTuesday", "data science", "{data.get("analysis_type", "EDA")}", "tidyverse"]
image: "hero_{fn}.png"
```

## Facebook Post Template

```
📊 {title_raw}

[Finding 1 in one sentence]
[Finding 2 in one sentence]
[Finding 3 in one sentence]

Full analysis + code: {BRAND_URL}/tidytuesday/{fn}

#DataScience #RStats #TidyTuesday #TheDataShrink
```

## Cross-Reference

- [← Hour 1 EDA](h1_eda_{fn}.qmd)
- [← Hour 2 Modeling](h2_modeling_{fn}.qmd)
"""

    out_path.write_text(content, encoding="utf-8")
    print(f"  WRITE: {out_path.name}")
    return out_path


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build 3-hour episode QMDs")
    parser.add_argument("--episode", help="Episode prefix to process (e.g. 001)")
    parser.add_argument("--hour", choices=["h1", "h2", "h3"], help="Only build this hour")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    folders = sorted(EPISODES_ROOT.iterdir())
    if args.episode:
        folders = [f for f in folders if f.name.startswith(args.episode)]

    total = 0
    for folder in folders:
        if not folder.is_dir():
            continue
        manifest_path = folder / "episode_manifest.json"
        if not manifest_path.exists():
            print(f"  NO MANIFEST: {folder.name}")
            continue

        data = json.loads(manifest_path.read_text(encoding="utf-8"))

        # Require DataX enrichment first
        if "atomic_concepts" not in data:
            print(f"  SKIP (not enriched — run enrich_datax.py first): {folder.name}")
            continue

        print(f"\n--- {folder.name} ---")
        if not args.hour or args.hour == "h1":
            build_h1(data, folder, args.force)
            total += 1
        if not args.hour or args.hour == "h2":
            build_h2(data, folder, args.force)
            total += 1
        if not args.hour or args.hour == "h3":
            build_h3(data, folder, args.force)
            total += 1

    print(f"\n✓ Done — {total} QMD files written")
    print("Next: open any episode folder and render with `quarto render <file>.qmd`")


if __name__ == "__main__":
    main()
