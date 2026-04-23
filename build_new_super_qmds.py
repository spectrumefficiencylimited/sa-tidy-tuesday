"""
build_new_super_qmds.py
-----------------------
For every row in control_table_full.csv that:
  - has ker_status == "needs_mapping"
  - has a transcript_file set (run build_transcripts.py first)

This script generates a super QMD in output/super_qmd/ following the
exact same format as the existing 001_..._super.qmd files.

The queue_position for new entries starts at 81 (after the existing 80).
"""

import csv
import os
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CT_PATH    = SCRIPT_DIR / "control_table.csv"
OUT_DIR    = SCRIPT_DIR / "output" / "super_qmd"
TT_DATA    = SCRIPT_DIR / "tidytuesday" / "data"

OUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def extract_date(data_source: str) -> str | None:
    m = re.search(r"(\d{4}-\d{2}-\d{2})", data_source)
    return m.group(1) if m else None


def find_data_files(date_str: str) -> list[str]:
    if not date_str:
        return []
    year = date_str[:4]
    folder = TT_DATA / year / date_str
    if not folder.exists():
        return []
    exts = ("*.csv", "*.tsv", "*.rds", "*.RDS", "*.xlsx")
    files = []
    for ext in exts:
        files.extend(folder.glob(ext))
    return [str(f.relative_to(SCRIPT_DIR)).replace("\\", "/") for f in sorted(files)]


def infer_analysis_type(data_files: list[str], topic: str) -> str:
    topic_lower = topic.lower()
    if any(k in topic_lower for k in ("predict", "model", "rating", "price", "salary")):
        return "Predictive"
    if any(k in topic_lower for k in ("tweet", "lyric", "text", "dialogue", "article",
                                       "review", "language", "sentiment")):
        return "Text"
    return "EDA"


def infer_pattern(analysis_type: str, has_time: bool, is_text: bool) -> str:
    if is_text:
        return "load_inspect_tokenize_trend_compare_visualize"
    if analysis_type == "Predictive":
        return "load_inspect_reshape_join_trend_model_evaluate_visualize"
    if has_time:
        return "load_inspect_recode_summarize_trend_compare_visualize"
    return "load_inspect_summarize_compare_visualize"


def infer_intent(topic: str, analysis_type: str, data_files: list[str]) -> str:
    topic_lower = topic.lower()
    if analysis_type == "Text":
        return (f"Explore and compare language patterns in {topic} using "
                f"tokenization, grouped counts, and discriminative text analysis")
    if analysis_type == "Predictive":
        return (f"Predict or estimate outcomes in {topic} using cleaned features, "
                f"exploratory analysis, and model evaluation")
    return (f"Explore distributions, group differences, and notable patterns "
            f"in {topic} through cleaning, summarization, and visualization")


_BOILERPLATE = re.compile(
    r"David Robinson.*?(?=I['']ll |I will |Today |In this |Let['']s |We['']re |So |This week)",
    re.IGNORECASE | re.DOTALL,
)

def parse_transcript_preview(transcript_file: str, length: int = 300) -> str:
    p = SCRIPT_DIR / transcript_file
    if not p.exists():
        return "[transcript not available]"
    text = p.read_text(encoding="utf-8", errors="ignore")
    text = _BOILERPLATE.sub("", text)
    flat = " ".join(text.split())
    return flat[:length] + "..."


def get_existing_count() -> int:
    """Count how many super QMDs already exist to determine start position."""
    return len(list(OUT_DIR.glob("*.qmd")))


def cognitive_signature(analysis_type: str, has_time: bool) -> list[str]:
    base = [
        "Start by naming the question and the unit of analysis before choosing plots or metrics.",
        "Use schema inspection to decide which columns carry the main story.",
        "Build one analysis-ready table before comparing groups.",
    ]
    if has_time:
        base.append("Start broad with time or trend structure when it helps explain which later comparisons are fair.")
    if analysis_type == "Predictive":
        base.append("Do descriptive work before modeling; the model should organize what exploratory work already suggested.")
    if analysis_type == "Text":
        base.append("Tokenize first at the word level, then zoom in on discriminative terms using tf-idf or log-odds.")
    base.append("End with one communication-ready chart or table that carries the episode's main claim.")
    return base


def thought_process_map(topic: str, analysis_type: str, has_time: bool) -> list[str]:
    steps = [
        f"T1 | Context | Frame the episode as exploratory analysis of {topic} with limited advance knowledge of the data. | Transcript title and opening context",
        f"T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints",
        f"T3 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations",
    ]
    if has_time:
        steps.append("T4 | Trend | Identify temporal patterns and seasonal variation before comparing sub-groups. | Time-based grouping and line charts")
    if analysis_type == "Text":
        steps.append("T4 | Tokenize | Split text into tokens, remove stop words, and compute term frequencies or tf-idf. | tidytext or tokenizers workflow")
    if analysis_type == "Predictive":
        steps.append("T5 | Model | Move from cleaned features to fitted models and evaluation outputs. | lm / glm / tidymodels workflow")
    steps += [
        "T6 | Compare | Summarize groups in a way that reveals differences, rankings, or trends. | group_by + summarise + arrange pattern",
        "T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow",
        "T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern",
    ]
    return steps


def code_mapping(analysis_type: str, has_time: bool) -> list[str]:
    rows = [
        "T1 | Data load and inspection | tt_load, count | Establish source shape, units, and comparison candidates",
        "T3 | Structuring and enrichment | mutate, left_join, pivot_longer | Convert messy inputs into analysis-ready tables",
    ]
    if has_time:
        rows.append("T4 | Temporal summary | group_by year/month, summarise, geom_line | Show trend over time")
    if analysis_type == "Text":
        rows.append("T4 | Tokenization | unnest_tokens, count, bind_tf_idf | Surface discriminative vocabulary")
    if analysis_type == "Predictive":
        rows.append("T5 | Modeling and evaluation | lm, glm, fit | Test explanatory or predictive relationships after EDA")
    rows.append("T7 | Visualization | ggplot, geom_col, geom_point, geom_line | Communicate the core result visually")
    return rows


def reusable_patterns(analysis_type: str) -> list[str]:
    base = [
        "inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y",
        "count_and_rank | Count and rank categorical variables to find the dominant groups | Any categorical column | Ranked frequency table | Y",
        "plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y",
    ]
    if analysis_type == "Predictive":
        base.append("build_predictive_pipeline | Move from cleaned features to fitted models and evaluation | Feature table and outcome | Model object and diagnostics | Y")
    if analysis_type == "Text":
        base.append("tokenize_and_tfidf | Tokenize text, remove stop words, compute tf-idf | Text column | Term-importance table | Y")
    return base


def function_candidates(analysis_type: str) -> list[str]:
    base = [
        "reshape_episode_inputs(data, ...)",
        "summarize_by_group(data, group_col, metric_col)",
        "plot_comparative_story(data, x_col, y_col, group_col = NULL)",
    ]
    if analysis_type == "Predictive":
        base += [
            "build_predictive_pipeline(data, formula, ...)",
            "evaluate_episode_model(model, test_data, outcome_col)",
        ]
    if analysis_type == "Text":
        base += [
            "tokenize_and_clean(data, text_col, stop_words)",
            "compute_tfidf_by_group(tokens_tbl, group_col)",
        ]
    return base


def adaptation_layer(analysis_type: str) -> list[str]:
    base = [
        "1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything",
        "3 | reshape_for_analysis | Pivot, join, or unnest only enough to make the next comparison possible",
        "6 | count_and_rank | Surface the dominant categories before building the comparative chart",
        "8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready",
    ]
    if analysis_type == "Predictive":
        base.insert(3, "5 | build_predictive_pipeline | Fit and evaluate a baseline model after core feature engineering is stable")
    if analysis_type == "Text":
        base.insert(2, "4 | tokenize_and_tfidf | Tokenize text before any group comparison to enable vocabulary-level analysis")
    return base


# ---------------------------------------------------------------------------
# QMD template
# ---------------------------------------------------------------------------

def build_super_qmd(
    queue_position: int,
    row: dict,
    date_str: str,
    data_files: list[str],
) -> str:
    topic_raw   = row.get("transcript_title", "")
    fn_name     = row.get("function_name", "")
    data_source = row.get("data_source", "")
    transcript_file = row.get("transcript_file", "")

    # Derive topic display string
    topic = re.sub(r"^Analyzing\s+", "", topic_raw, flags=re.I)
    topic = re.sub(r"\s+in\s+R$", "", topic, flags=re.I).strip()

    analysis_type = infer_analysis_type(data_files, topic)
    has_time = bool(date_str)  # almost always true; refined below
    is_text  = analysis_type == "Text"

    # Check for time columns by looking at readme column names if available
    year = date_str[:4] if date_str else ""
    readme_path = TT_DATA / year / date_str / "readme.md" if date_str else None
    has_time_col = False
    if readme_path and readme_path.exists():
        text = readme_path.read_text(encoding="utf-8", errors="ignore")
        has_time_col = bool(re.search(r"\b(year|month|date|week|season|quarter)\b", text, re.I))

    pattern = row.get("pattern_signature", "").strip() or infer_pattern(analysis_type, has_time_col, is_text)
    intent  = row.get("analysis_intent", "").strip()  or infer_intent(topic, analysis_type, data_files)

    cog_sig  = cognitive_signature(analysis_type, has_time_col)
    tp_map   = thought_process_map(topic, analysis_type, has_time_col)
    code_map = code_mapping(analysis_type, has_time_col)
    reuse_p  = reusable_patterns(analysis_type)
    fn_cands = function_candidates(analysis_type)
    adapt_l  = adaptation_layer(analysis_type)

    local_assets = "\n".join(f"- `{f}`" for f in data_files) or "- *(data files not detected locally)*"

    # Setup chunk: list the data file names
    load_lines = []
    for f in data_files[:4]:
        df_name = Path(f).stem.replace("-", "_")
        load_lines.append(f'{df_name} <- tuesdata${df_name}  # or read from local path')
    if not load_lines:
        load_lines = ["# use names(tuesdata) to see available tables"]
    load_block = "\n".join(load_lines)

    # Source assets for transform stage
    source_assets = ", ".join(data_files) if data_files else "see tidytuesday readme"

    tp_map_str   = "\n".join(f"- `{s}`" for s in tp_map)
    _tp_steps    = [m for s in tp_map if (m := re.match(r"T(\d+) \| (\w+) \|", s))]
    tp_log_rows  = "\n".join(
        f'  "T{m.group(1)}", "{m.group(2).title()}", "",' for m in _tp_steps
    )
    code_map_str = "\n".join(f"- `{s}`" for s in code_map)
    cog_sig_str  = "\n".join(f"- {s}" for s in cog_sig)
    reuse_str    = "\n".join(f"- `{s}`" for s in reuse_p)
    fn_str       = "\n".join(f"- `{s}`" for s in fn_cands)
    adapt_str    = "\n".join(f"- `{s}`" for s in adapt_l)

    pos_str = f"{queue_position:03d}"

    # ── Detect flag columns (pivot_longer candidates) ──────────────────
    has_flag_cols = False
    cat1 = "category"
    cat2 = "group"
    num1 = "value"
    num2 = "value2"
    join_key = "id"
    model_predictors = "predictor1 + predictor2"
    if readme_path and readme_path.exists():
        readme_text = readme_path.read_text(encoding="utf-8", errors="ignore")
        flag_hits = re.findall(r"\|\s*(\w+)\s*\|\s*logical", readme_text, re.I)
        has_flag_cols = len(flag_hits) >= 3
        # Extract some column names for concrete scaffold
        char_hits = re.findall(r"\|\s*(\w+)\s*\|\s*(?:character|chr|factor)", readme_text, re.I)
        num_hits  = re.findall(r"\|\s*(\w+)\s*\|\s*(?:integer|int|double|dbl|numeric)", readme_text, re.I)
        if char_hits:
            cat1 = char_hits[0]
            cat2 = char_hits[1] if len(char_hits) > 1 else cat1
        if num_hits:
            num1 = num_hits[0]
            num2 = num_hits[1] if len(num_hits) > 1 else num1
        if flag_hits:
            join_key = flag_hits[0]
        # Simple predictor string for model
        predictors = char_hits[:2] + num_hits[:2]
        if predictors:
            model_predictors = " + ".join(predictors[:4])

    # ── Stage number plan ─────────────────────────────────────────────────
    # For text:       H2 stages 7-8 (tokenize, vocab), H3 starts at 9
    # For EDA+flags:  H2 stages 7-10 (pivot, multi-axis, outliers, corr), H3 starts at 11
    # For EDA:        H2 stages 7-9 (multi-axis, outliers, corr), H3 starts at 10
    s_multi   = 8 if has_flag_cols else 7
    s_outl    = s_multi + 1
    s_corr    = s_multi + 2
    s_h3_base = 9 if is_text else (s_corr + 1)
    s_model   = s_h3_base
    s_resid   = s_h3_base + 1
    s_final   = s_h3_base + 2
    s_ker     = s_h3_base + 3

    # ── Conditional stage blocks ──────────────────────────────────────────
    text_stage = ""
    if is_text:
        text_stage = f"""
---

## Hour 2 — Depth

### Stage 7: Tokenize

Split text into words, remove stop words, and compute term frequencies or tf-idf.

::: {{.callout-note}}
## Cognitive Move
Tokenize before any group comparison — vocabulary-level signals often explain group differences more cleanly than aggregate counts.

Trigger: unnest_tokens / tidytext workflow
:::

```{{r}}
#| label: stage_07_tokenize
#| eval: false

library(tidytext)

tokens_tbl <- analysis_tbl |>
  unnest_tokens(word, text_col) |>
  anti_join(stop_words, by = "word") |>
  count({cat1}, word, sort = TRUE)

# tf-idf
tokens_tbl |>
  bind_tf_idf(word, {cat1}, n) |>
  arrange(desc(tf_idf))
```

### Stage 8: Discriminative Vocabulary

Which words are most characteristic of each group?

::: {{.callout-note}}
## Cognitive Move
Use log-odds or tf-idf to find vocabulary that discriminates groups, not just frequency.

Trigger: bind_log_odds or bind_tf_idf
:::

```{{r}}
#| label: stage_08_discriminative_vocab
#| eval: false

library(tidylo)

tokens_tbl |>
  bind_log_odds({cat1}, word, n) |>
  group_by({cat1}) |>
  slice_max(log_odds_weighted, n = 10) |>
  ggplot(aes(log_odds_weighted, fct_reorder(word, log_odds_weighted), fill = {cat1})) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ {cat1}, scales = "free_y") +
  labs(title = "Most characteristic words per group",
       subtitle = "Log-odds weighted",
       x = "Log-odds", y = NULL)
```
"""

    pivot_stage = ""
    if has_flag_cols:
        flag_list = ", ".join(flag_hits[:5]) if flag_hits else "flag1, flag2, flag3"
        pivot_stage = f"""
### Stage 7: Pivot Flag Columns

The table has multiple logical tag columns ({flag_list}, ...) — pivot them long for grouped analysis.

::: {{.callout-note}}
## Cognitive Move
Wide boolean flags are hard to compare directly. Pivoting to long format makes each tag a row, enabling group_by(tag) comparisons.

Trigger: pivot_longer + filter(value == TRUE)
:::

```{{r}}
#| label: stage_07_pivot_flags
#| eval: false

tags_long <- analysis_tbl |>
  pivot_longer(
    cols = where(is.logical),
    names_to  = "tag",
    values_to = "has_tag"
  ) |>
  filter(has_tag == TRUE)

# now compare metric by tag
tags_long |>
  group_by(tag) |>
  summarise(
    n          = n(),
    median_{num1} = median({num1}, na.rm = TRUE)
  ) |>
  arrange(desc(median_{num1})) |>
  ggplot(aes(median_{num1}, fct_reorder(tag, median_{num1}))) +
  geom_col() +
  labs(title = "How does each tag relate to {num1}?",
       x = "Median {num1}", y = "Tag")
```
"""

    # ── Hour 3 block (always appended after Hour 2) ────────────────────────
    hour3_stages = f"""
---

## Hour 3 — Synthesis

### Stage {s_model}: Model

Fit a linear model to quantify what predicts {num1}.

::: {{.callout-note}}
## Cognitive Move
Move from "what differs" (descriptive) to "what explains" (inferential). The model should confirm the story the charts already suggested — not replace it.

Trigger: lm() + broom::tidy() + coefficient plot
:::

```{{r}}
#| label: stage_{s_model:02d}_model
#| eval: false

model_tbl <- analysis_tbl |>
  mutate(across(where(is.character), as.factor))

model_fit <- lm({num1} ~ {model_predictors}, data = model_tbl)

broom::tidy(model_fit, conf.int = TRUE) |>
  filter(term != "(Intercept)") |>
  mutate(term = fct_reorder(term, estimate)) |>
  ggplot(aes(estimate, term,
             xmin = conf.low, xmax = conf.high)) +
  geom_pointrange() +
  geom_vline(xintercept = 0, linetype = "dashed") +
  labs(title = "What predicts {num1}?",
       subtitle = "Linear model coefficients (95% CI)",
       x = "Estimate", y = NULL)
```

### Stage {s_resid}: Residuals

Which cases does the model get most wrong?

::: {{.callout-note}}
## Cognitive Move
Residuals reveal where the model's assumptions break down — often these are the most analytically interesting cases.

Trigger: broom::augment() + geom_point(.resid) + geom_text_repel
:::

```{{r}}
#| label: stage_{s_resid:02d}_residuals
#| eval: false

augmented_tbl <- broom::augment(model_fit, data = model_tbl)

ggplot(augmented_tbl, aes(.fitted, .resid, label = {cat1})) +
  geom_point(alpha = 0.4) +
  geom_smooth(method = "loess", se = FALSE, colour = "steelblue") +
  geom_hline(yintercept = 0, linetype = "dashed") +
  geom_text_repel(
    data = filter(augmented_tbl, abs(.resid) > quantile(abs(.resid), 0.95)),
    size = 3, max.overlaps = 15
  ) +
  labs(title = "Residuals: who over- or underperforms the model?",
       x = "Fitted {num1}", y = "Residual")
```

### Stage {s_final}: Final Communication Chart

One polished chart that carries the entire episode's story.

::: {{.callout-note}}
## Cognitive Move
The communication chart is not a summary of everything — it is the single clearest view of the main finding. Choose the encoding that requires the least explanation.

Trigger: After residuals and model are stable, step back and pick the clearest one-chart story
:::

```{{r}}
#| label: stage_{s_final:02d}_final_chart
#| eval: false

final_tbl <- analysis_tbl |>
  group_by({cat1}) |>
  summarise(
    median_{num1} = median({num1}, na.rm = TRUE),
    n = n(),
    .groups = "drop"
  ) |>
  filter(n >= 5) |>
  mutate({cat1} = fct_reorder({cat1}, median_{num1}))

ggplot(final_tbl,
       aes(x = {cat1}, y = median_{num1},
           fill = median_{num1})) +
  geom_col(show.legend = FALSE) +
  scale_fill_gradient2(
    low = "tomato", mid = "gray90", high = "steelblue",
    midpoint = median(analysis_tbl${num1}, na.rm = TRUE)
  ) +
  coord_flip() +
  labs(
    title    = "{topic}: {num1} by {cat1}",
    subtitle = "Median per group | colour = above/below overall median",
    caption  = "Source: TidyTuesday {date_str}",
    x = NULL, y = "Median {num1}"
  ) +
  theme_minimal(base_size = 13) +
  theme(plot.title = element_text(face = "bold"))
```

### Stage {s_ker}: Knowledge Extraction

Capture the reusable pattern for the KER.

::: {{.callout-note}}
## Cognitive Move
After the analysis is clear, abstract it: what is the general workflow that would work on any similar dataset? That is what goes into the KER and into a helper function.

Trigger: End of episode — write the function stub before closing the session
:::

```{{r}}
#| label: stage_{s_ker:02d}_ker_capture
#| eval: false

# Pattern: load -> inspect -> {("pivot_flags -> " if has_flag_cols else "")}join ->
#          multi-axis compare -> outlier detection -> model -> residuals -> final chart

# Candidate helper:
# compare_groups_by_outcome <- function(data, group_col, outcome_col,
#                                        secondary_group = NULL,
#                                        model = TRUE) {{
#   # 1. group_by + summarise
#   # 2. residual calculation
#   # 3. optional lm + broom::tidy
#   # 4. ggplot output
# }}
```
"""

    # ── Hour 2 stage block (always included) ──────────────────────────────
    if is_text:
        # For text analysis: Hour 2 = tokenize + discriminative vocab (already in text_stage)
        hour2_stages = text_stage + hour3_stages
    else:
        hour2_stages = f"""
---

## Hour 2 — Depth

{pivot_stage if has_flag_cols else ""}

### Stage {s_multi}: Multi-axis Comparison

Examine the interaction between two grouping variables rather than one at a time.

::: {{.callout-note}}
## Cognitive Move
One-dimensional summaries miss interaction effects. Cross two categoricals to see whether the relationship holds across all sub-groups or only some.

Trigger: group_by(cat1, cat2) + summarise + facet_wrap
:::

```{{r}}
#| label: stage_{s_multi:02d}_multiaxis
#| eval: false

cross_tbl <- analysis_tbl |>
  group_by({cat1}, {cat2}) |>
  summarise(
    n      = n(),
    median = median({num1}, na.rm = TRUE),
    .groups = "drop"
  ) |>
  filter(n >= 3)

ggplot(cross_tbl, aes(x = fct_reorder({cat1}, median), y = median, fill = {cat2})) +
  geom_col(position = "dodge") +
  coord_flip() +
  facet_wrap(~ {cat2}, scales = "free_x") +
  labs(title = "{topic}: {num1} by {cat1} and {cat2}",
       x = NULL, y = "Median {num1}")
```

### Stage {s_outl}: Outlier Investigation

Find cases that sit far from their group expectation.

::: {{.callout-note}}
## Cognitive Move
After the aggregate pattern is clear, the outliers are often the most interesting story — they show where the rule breaks down.

Trigger: group_by + mutate(residual = value - group_median) + slice_max(abs(residual))
:::

```{{r}}
#| label: stage_{s_outl:02d}_outliers
#| eval: false

residual_tbl <- analysis_tbl |>
  group_by({cat1}) |>
  mutate(
    group_median = median({num1}, na.rm = TRUE),
    residual     = {num1} - group_median
  ) |>
  ungroup() |>
  arrange(desc(abs(residual)))

# Label the top outliers
library(ggrepel)

ggplot(residual_tbl,
       aes(x = group_median, y = {num1}, label = {cat1})) +
  geom_point(alpha = 0.4) +
  geom_text_repel(
    data = slice_max(residual_tbl, abs(residual), n = 15),
    size = 3, max.overlaps = 20
  ) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed") +
  labs(title = "Who over- or underperforms their group median?",
       x = "Group median {num1}", y = "Observed {num1}")
```

### Stage {s_corr}: Correlation Structure

Examine how numeric columns relate to each other and to the outcome.

::: {{.callout-note}}
## Cognitive Move
Scatter plots with colour encoding reveal whether a confound explains the group difference, or whether the effect is additive.

Trigger: geom_point + geom_smooth(method = "lm") + color by group
:::

```{{r}}
#| label: stage_{s_corr:02d}_correlation
#| eval: false

ggplot(analysis_tbl,
       aes(x = {num2}, y = {num1}, colour = {cat1})) +
  geom_point(alpha = 0.5) +
  geom_smooth(method = "lm", se = FALSE) +
  scale_colour_viridis_d(end = 0.85) +
  labs(title = "Relationship between {num1} and {num2}",
       subtitle = "Coloured by {cat1}",
       x = "{num2}", y = "{num1}")
```
""" + hour3_stages

    qmd = f"""\
---
title: "Super QMD: {topic_raw}"
subtitle: "Cognition-first blueprint built from the episode guide and KER"
author: "Andrei Stoian"
format:
  html:
    theme: flatly
    toc: true
    toc-depth: 3
    code-fold: show
    code-summary: "Show scaffold code"
    number-sections: true
execute:
  echo: true
  warning: false
  message: false
editor: visual
---

## What This Document Is

This super QMD is the bridge between:

- the TidyTuesday dataset for `{date_str}`
- the KER entry for `{fn_name}`
- a final guided analysis document

The point is to preserve not only the code path, but the author's cognition:

- what question gets asked first
- how the dataset is inspected
- when transformation happens
- why one comparison is chosen before another
- which pieces should become reusable helpers

## Episode Snapshot

::: {{.callout-note}}
## Analysis Intent
{intent}
:::

| Field | Value |
|---|---|
| Queue | #{pos_str} |
| Function | `{fn_name}` |
| Analysis type | {analysis_type} |
| Data source | {data_source} |
| Status | `needs_mapping` |

**Analytical pattern:** `{pattern}`

## Cognitive Signature

{cog_sig_str}

## Data and Execution Context

### Local Assets

{local_assets}

### Execution Notes

- Use `load_tidyweek_data("{date_str}")` from `R/screencast_helpers.R` if local files are present
- Otherwise fall back to `tidytuesdayR::tt_load("{date_str}")`

### External Dependencies

- No external dependencies captured.

## Setup Scaffold

```{{r}}
#| label: setup
#| eval: false

library(tidyverse)
source("R/screencast_helpers.R")

# Optional episode packages:
# library(scales)
# library(tidytuesdayR)

tuesdata <- load_tidyweek_data("{date_str}")
names(tuesdata)

{load_block}
```

## Thought -> Code -> Data Bridge

### Thought Process Map

{tp_map_str}

```{{r}}
#| label: thought_execution_log
#| eval: false

# Fill in `finding` after completing each stage.
thought_log <- tibble::tribble(
  ~step,  ~move,        ~finding,
{tp_log_rows}
)
thought_log
```

### Code Mapping Table

{code_map_str}

### Data Transformation Flow

- `Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface`
- `Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison`
- `Clean -> Analytical | Feature table | Engineer predictors or compute group metrics | Summary or model outputs | Quantify relationships beyond descriptive summaries`
- `Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart`

## Guided Build Sequence

## Stage 1: Context

Frame the episode as exploratory analysis of {topic} with limited advance knowledge of the data.

::: {{.callout-note}}
## Cognitive Move
Define the analytical question, likely unit of analysis, and what would count as an interesting result.

Trigger:

- Transcript title and opening context


:::

```{{r}}
#| label: stage_01_context
#| eval: false

# Write the one-sentence analytical question for this episode.
# Topic: {topic}
# Unit of analysis:
# Main comparison axis:
# What would make the result interesting?
```
## Stage 2: Inspect

Load the data, inspect table shape, and identify the main entities, measures, and comparison axes.

::: {{.callout-note}}
## Cognitive Move
Inspect shape, columns, missingness, and table roles before committing to transformations.

Trigger:

- Initial data load and early counts or prints


:::

```{{r}}
#| label: stage_02_inspect
#| eval: false

# Start here once data is loaded.
# names(tuesdata)
# purrr::imap_dfr(tuesdata, ~ tibble(table = .y, rows = nrow(.x), cols = ncol(.x)))
# glimpse(analysis_tbl)
# skimr::skim(analysis_tbl)
```
## Stage 3: Transform

Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records.

::: {{.callout-note}}
## Cognitive Move
Reshape, join, or normalize only enough to make the next comparison possible.

Trigger:

- Join and reshaping operations in the source Rmd


:::

```{{r}}
#| label: stage_03_transform
#| eval: false

# Build the canonical analysis table for this episode.
# Source assets: {source_assets}
# Suggested verbs: mutate(), separate_rows(), pivot_longer(), left_join(), unnest()
# analysis_tbl <- raw_tbl %>%
#   ...
```
## Stage 4: Compare

Summarize groups or entities in a way that reveals differences, rankings, or trends.

::: {{.callout-note}}
## Cognitive Move
Summarize groups or entities in a way that reveals differences, rankings, or trends without overfitting the story.

Trigger:

- count() and group_by() + summarise() patterns

Additional guidance:

- If you plan to model, use this step to identify which predictors deserve to enter the first baseline model.
:::

```{{r}}
#| label: stage_04_compare
#| eval: false

# Summarize the comparison that best answers the question.
# comparison_tbl <- analysis_tbl %>%
#   count(category_col, sort = TRUE)   # or
#   group_by(group_col) %>%
#   summarise(metric = mean(value_col, na.rm = TRUE)) %>%
#   arrange(desc(metric))
```
## Stage 5: Visualize

Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view.

::: {{.callout-note}}
## Cognitive Move
Choose the plot after the summary table exists, then optimize for clarity rather than novelty.

Trigger:

- ggplot workflow

Additional guidance:

- When time is present, lead with the broad trend before showing narrower subgroup comparisons.
:::

```{{r}}
#| label: stage_05_visualize
#| eval: false

# Turn the comparison table into one clear communication plot.
# ggplot(comparison_tbl, aes(x = fct_reorder(category, metric), y = metric)) +
#   geom_col() +
#   coord_flip() +
#   labs(
#     title = "...",
#     subtitle = "Source: TidyTuesday {date_str}",
#     x = NULL, y = NULL
#   )
```
## Stage 6: Reflect

Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question.

::: {{.callout-note}}
## Cognitive Move
Translate the episode-specific move into a reusable function, helper, or workflow note.

Trigger:

- End-state of the analysis pattern


:::

```{{r}}
#| label: stage_06_reflect
#| eval: false

# Capture the reusable move after the analysis is clear.
# Candidate helper:
# - input:
# - output:
# - why it is reusable:
```
{hour2_stages}

## Reusable Layer

### Reusable Patterns

{reuse_str}

### Function Candidates

{fn_str}

## How To Finish This Super QMD

1. Replace each scaffold chunk with the real episode-specific analysis code.
2. After each major result, add a short callout explaining what changed in your thinking.
3. Keep one broad chart early, one comparison chart in the middle, and one final communication chart at the end.
4. Move any repeated transformation or comparison logic into `R/screencast_helpers.R`.
5. Once the document reads like a guided walkthrough instead of a reproduction note, promote it into a finished KER-guided analysis.

## Adaptation Layer

{adapt_str}
"""
    return qmd.strip()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(force: bool = False):
    with open(CT_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # When forcing, delete all existing needs_mapping QMDs first so queue
    # positions are recalculated cleanly from the existing 80 originals.
    if force:
        for p in sorted(OUT_DIR.glob("*.qmd")):
            # Only delete files from queue position 081 onward (new entries)
            stem = p.stem
            try:
                pos = int(stem.split("_")[0])
                if pos >= 81:
                    p.unlink()
            except (ValueError, IndexError):
                pass

    # Count remaining (original) super QMDs to set starting queue position
    existing_qmds = len(list(OUT_DIR.glob("*.qmd")))
    queue_pos = existing_qmds + 1

    generated = 0
    skipped   = 0

    for row in rows:
        if row.get("ker_status", "").strip() != "needs_mapping":
            continue
        if not row.get("transcript_file", "").strip():
            skipped += 1
            continue

        date_str   = extract_date(row.get("data_source", ""))
        data_files = find_data_files(date_str) if date_str else []
        fn_name    = row.get("function_name", "")

        # Check if QMD already exists (skip if not forcing)
        existing = list(OUT_DIR.glob(f"*_{fn_name}_super.qmd"))
        if existing and not force:
            skipped += 1
            continue

        out_path = OUT_DIR / f"{queue_pos:03d}_{fn_name}_super.qmd"

        qmd_content = build_super_qmd(
            queue_position=queue_pos,
            row=row,
            date_str=date_str or "",
            data_files=data_files,
        )

        out_path.write_text(qmd_content, encoding="utf-8")
        queue_pos += 1
        generated += 1

    print(f"Super QMDs generated : {generated}")
    print(f"Skipped              : {skipped}")
    print(f"Next queue position  : {queue_pos}")


if __name__ == "__main__":
    import sys
    force = "--force" in sys.argv
    main(force=force)
