#!/usr/bin/env python3
"""
auto_build_episodes.py
Build fully executable h1/h2/h3 QMDs for all episodes by injecting
source Rmd code into the TheDataShrink™ 3-hour template.

Usage:
  python3 auto_build_episodes.py              # all episodes
  python3 auto_build_episodes.py --ep 001     # single episode
  python3 auto_build_episodes.py --force      # overwrite existing built QMDs
"""

import json, os, re, sys, glob, textwrap, argparse

BASE     = "/Users/stoiana/sa-tidy-tuesday"
EPS_ROOT = os.path.join(BASE, "output/episodes")
RMD_ROOT = os.path.join(BASE, "data-screencasts-dgrtwo")
DATA_ROOT = os.path.join(BASE, "tidytuesday/data")

# ── THEMES ──────────────────────────────────────────────────────────────────
H1_THEME = "flatly"
H2_THEME = "cosmo"
H3_THEME = "litera"

# ── BRAND COLOURS ───────────────────────────────────────────────────────────
BRAND_SETUP = """
# TheDataShrink™ brand colours
TDS_BLUE  <- "#1b6ca8"
TDS_GOLD  <- "#c8a415"
TDS_DARK  <- "#1a1a2e"
TDS_LIGHT <- "#f8f9fa"
theme_set(theme_light(base_size = 13))
"""

# ─────────────────────────────────────────────────────────────────────────────
# RMD PARSING
# ─────────────────────────────────────────────────────────────────────────────

def parse_rmd_chunks(rmd_path):
    """Return list of dicts: {label, options, code, section_header}"""
    with open(rmd_path, encoding="utf-8", errors="replace") as f:
        content = f.read()

    chunks = []
    current_section = ""
    lines = content.split("\n")
    i = 0
    chunk_idx = 0
    while i < len(lines):
        line = lines[i]
        # Markdown section headers
        if line.startswith("#"):
            current_section = line.lstrip("#").strip()
            i += 1
            continue
        # Start of code chunk
        if line.startswith("```{r"):
            header = line.strip()
            # Parse label and options
            m = re.match(r"```\{r\s*([^,}]*)?(.*)\}", header)
            label = (m.group(1) or "").strip() if m else ""
            opts  = (m.group(2) or "").strip().lstrip(",").strip() if m else ""
            if not label:
                chunk_idx += 1
                label = f"chunk_{chunk_idx:02d}"
            # Collect body
            body_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                body_lines.append(lines[i])
                i += 1
            code = "\n".join(body_lines).strip()
            # Strip View() calls — only the View() line itself, not the pipe chain
            code = re.sub(r"\n?\s*View\([^)]*\)", "", code)
            # Modernise: replace magrittr %>% with native pipe |>
            code = code.replace("%>%", "|>")
            # Collapse multiple blank lines → single blank
            code = re.sub(r"\n{3,}", "\n\n", code).strip()
            # Skip empty / knitr setup / View() only chunks
            if code and not _is_trivial(code):
                chunks.append({
                    "label": label,
                    "options": opts,
                    "code": code,
                    "section": current_section,
                })
        i += 1
    return chunks


def _is_trivial(code):
    """True if chunk is just opts_chunk$set, View(), or blank."""
    stripped = re.sub(r"#.*", "", code).strip()
    if not stripped:
        return True
    if re.match(r"^knitr::opts_chunk\$set\(", stripped):
        return True
    if re.match(r"^[a-z_\$]+\s*%>%\s*View\(\)\s*$", stripped):
        return True
    if stripped == "View()":
        return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# DATA-PATH RESOLUTION  (replace tt_load with local read_csv)
# ─────────────────────────────────────────────────────────────────────────────

def resolve_local_load(manifest, chunks):
    """
    Replace tidytuesdayR::tt_load(...) chunks with direct read_csv calls
    using the local_data_files listed in the manifest.
    Returns modified chunk list.
    """
    local_files = manifest.get("local_data_files", [])
    if not local_files:
        return chunks

    # Build a name→path map  (e.g. "firsts" → "tidytuesday/data/.../firsts.csv")
    file_map = {}
    for rel in local_files:
        name = os.path.splitext(os.path.basename(rel))[0]
        abs_path = os.path.join(BASE, rel)
        file_map[name] = abs_path

    new_chunks = []
    for ch in chunks:
        code = ch["code"]
        # Replace tt_load block
        if "tt_load" in code or "tidytuesdayR" in code:
            read_lines = []
            for name, path in file_map.items():
                ext = os.path.splitext(path)[1].lower()
                if ext in (".tsv",):
                    read_lines.append(f'{name} <- read_tsv("{path}", show_col_types = FALSE)')
                elif ext in (".rds",):
                    read_lines.append(f'{name} <- readRDS("{path}")')
                else:
                    read_lines.append(f'{name} <- read_csv("{path}", show_col_types = FALSE)')
            new_code = "\n".join(read_lines)
            # Add glimpse for orientation
            for name in list(file_map.keys())[:2]:
                new_code += f"\nglimpse({name})"
            ch = dict(ch)
            ch["code"] = new_code
            ch["label"] = "load-data"

        # Remove tuesdata$ references in subsequent chunks
        code2 = re.sub(r"tuesdata\$(\w+)", r"\1", ch["code"])
        if code2 != ch["code"]:
            ch = dict(ch)
            ch["code"] = code2
        new_chunks.append(ch)
    return new_chunks


# ─────────────────────────────────────────────────────────────────────────────
# QMD BUILDERS
# ─────────────────────────────────────────────────────────────────────────────

def yaml_header(title, subtitle, theme, hour_n, ep_num):
    return f"""---
title: "{title}"
subtitle: "{subtitle} | TheDataShrink™"
author: "TheDataShrink™"
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
  error: true
editor: visual
---
"""


def callout_brand(ep_num, hour_n, ep_fn):
    links = []
    if hour_n > 1:
        links.append(f"[← Hour 1 EDA](h1_eda_{ep_fn}.qmd)")
    if hour_n > 2:
        links.append(f"[← Hour 2 Modeling](h2_modeling_{ep_fn}.qmd)")
    link_str = " · ".join(links)
    sep = " · " if links else ""
    return f"""
::: {{.callout-tip}}
## TheDataShrink™ — Data stories worth sharing.
Episode {ep_num:03d} · Hour {hour_n}{sep}{link_str}
:::
"""


def chunks_to_qmd(chunks, section_map=None):
    """Convert parsed chunks to QMD code block strings."""
    out = []
    last_section = None
    for ch in chunks:
        sec = ch.get("section", "")
        if sec and sec != last_section and section_map:
            mapped = section_map.get(sec, sec)
            out.append(f"\n## {mapped}\n")
            last_section = sec
        label = re.sub(r"[^a-zA-Z0-9_-]", "-", ch["label"])
        out.append(f'```{{r {label}}}\n{ch["code"]}\n```\n')
    return "\n".join(out)


# ── H1: EDA ──────────────────────────────────────────────────────────────────

def build_h1(manifest, chunks, ep_num, ep_fn, ep_dir):
    title   = manifest.get("transcript_title", f"Episode {ep_num:03d}")
    features = manifest.get("features", {})
    fails   = manifest.get("fails_when", [])
    works   = manifest.get("works_when", [])
    concepts = manifest.get("atomic_concepts", [])

    fails_md  = "\n".join(f"- {f}" for f in fails) if fails else "- (none documented)"
    works_md  = "\n".join(f"- {w}" for w in works) if works else "- (none documented)"
    concepts_md = " · ".join(f"`{c}`" for c in concepts[:12]) if concepts else ""

    # Detect library list from chunks
    libraries = _extract_libraries(chunks)
    # Always include tidyverse + here
    for lib in ["tidyverse", "scales", "here"]:
        if lib not in libraries:
            libraries.insert(0, lib)

    lib_block = "\n".join(f"library({l})" for l in libraries)

    # Build setup chunk: libraries + brand colours
    setup_code = f"{lib_block}\n{BRAND_SETUP}"

    # Remove existing setup/library chunks — we replace them
    data_chunks = [ch for ch in chunks if ch["label"] not in ("setup", "load-data") and
                   not _is_library_only(ch["code"])]
    load_chunk  = next((ch for ch in chunks if ch["label"] == "load-data"), None)

    body_parts = []

    # Setup
    body_parts.append(f'```{{r setup}}\n{setup_code}\n```\n')

    # Load
    if load_chunk:
        body_parts.append("## Load data\n")
        body_parts.append(f'```{{r load-data}}\n{load_chunk["code"]}\n```\n')

    # EDA chunks — group by section
    current_sec = None
    for ch in data_chunks:
        sec = ch.get("section", "")
        if sec and sec != current_sec:
            body_parts.append(f"\n## {sec}\n")
            current_sec = sec
        elif not sec and not current_sec:
            body_parts.append("\n## Explore\n")
            current_sec = "Explore"
        label = re.sub(r"[^a-zA-Z0-9_-]", "-", ch["label"])
        body_parts.append(f'```{{r {label}}}\n{ch["code"]}\n```\n')

    # Navigation footer
    body_parts.append(f'\n---\n\n**→ [Hour 2: Modeling](h2_modeling_{ep_fn}.qmd)**\n')

    content = f"""{yaml_header(f"Hour 1 — EDA: {title}", "David Robinson's analysis, extended", H1_THEME, 1, ep_num)}
{callout_brand(ep_num, 1, ep_fn)}

::: {{.callout-note collapse="true"}}
## Atomic Concepts in this episode
{concepts_md}
:::

::: {{.callout-warning collapse="true"}}
## FAILS WHEN
{fails_md}
:::

::: {{.callout-important collapse="true"}}
## WORKS WHEN
{works_md}
:::

{''.join(body_parts)}
*TheDataShrink™ — thedatashrink.com.au — Weekly data stories in R*
"""
    return content


# ── H2: MODELING ─────────────────────────────────────────────────────────────

def build_h2(manifest, chunks, ep_num, ep_fn):
    title    = manifest.get("transcript_title", f"Episode {ep_num:03d}")
    features = manifest.get("features", {})
    concepts = manifest.get("atomic_concepts", [])
    concepts_md = " · ".join(f"`{c}`" for c in concepts[:10]) if concepts else ""

    # Pick appropriate modeling section based on features
    modeling_section = _modeling_for_features(features, manifest)

    content = f"""{yaml_header(f"Hour 2 — Modeling: {title}", "Going deeper with statistical models", H2_THEME, 2, ep_num)}
{callout_brand(ep_num, 2, ep_fn)}

::: {{.callout-note collapse="true"}}
## Atomic Concepts — Hour 2
{concepts_md}
:::

## Setup

```{{r setup}}
library(tidyverse)
library(scales)
library(broom)
library(here)
theme_set(theme_light(base_size = 13))
```

## Reload data

```{{r load-data}}
# Re-load from Hour 1 — same local paths
source_qmd <- here::here("output/episodes/{ep_fn}/h1_eda_{ep_fn}.qmd")
# Data files are re-read directly below if needed
```

{modeling_section}

---

**→ [Hour 3: Communicate](h3_communicate_{ep_fn}.qmd)**
"""
    return content


def _modeling_for_features(features, manifest):
    """Return a QMD modeling section tailored to the episode's feature flags."""
    sections = []
    local_files = manifest.get("local_data_files", [])
    primary_csv = local_files[0] if local_files else None
    abs_path = os.path.join(BASE, primary_csv) if primary_csv else None
    read_stmt = f'df <- read_csv("{abs_path}", show_col_types = FALSE)' if abs_path else "# df <- read_csv(...)"

    if features.get("text_analysis"):
        sections.append(_text_modeling(read_stmt))
    if features.get("predictive") or features.get("modeling"):
        sections.append(_predictive_modeling(read_stmt))
    if features.get("time"):
        sections.append(_time_modeling(read_stmt))
    if not sections:
        sections.append(_generic_modeling(read_stmt))

    return "\n\n".join(sections)


def _text_modeling(read_stmt):
    return f"""## Model 1 — Sentiment analysis

```{{r text-setup}}
library(tidytext)
{read_stmt}
```

```{{r sentiment}}
afinn <- get_sentiments("afinn")

# Adjust column names to match your data
# df |> unnest_tokens(word, text_column) |> inner_join(afinn, by = "word") |>
#   group_by(group_col) |> summarise(mean_sentiment = mean(value), .groups = "drop") |>
#   mutate(group_col = fct_reorder(group_col, mean_sentiment)) |>
#   ggplot(aes(mean_sentiment, group_col)) + geom_col()
cat("Sentiment analysis: customise the column names above to your dataset\\n")
```

## Model 2 — TF-IDF: most distinctive terms by group

```{{r tfidf}}
# df |> unnest_tokens(word, text_column) |>
#   anti_join(stop_words, by = "word") |>
#   count(group_col, word) |>
#   bind_tf_idf(word, group_col, n) |>
#   group_by(group_col) |>
#   slice_max(tf_idf, n = 8, with_ties = FALSE) |>
#   mutate(word = reorder_within(word, tf_idf, group_col)) |>
#   ggplot(aes(tf_idf, word, fill = group_col)) +
#   geom_col(show.legend = FALSE) +
#   facet_wrap(~group_col, scales = "free_y") +
#   scale_y_reordered()
cat("TF-IDF: customise column names above\\n")
```
"""


def _predictive_modeling(read_stmt):
    return f"""## Model 1 — Linear regression baseline

```{{r lm-setup}}
{read_stmt}
glimpse(df)
```

```{{r lm-fit}}
# Identify your outcome and predictors first — adjust formula below
# fit <- lm(outcome ~ predictor1 + predictor2, data = df)
# tidy(fit) |> filter(term != "(Intercept)") |>
#   mutate(term = fct_reorder(term, estimate)) |>
#   ggplot(aes(estimate, term, xmin = estimate - 2*std.error,
#              xmax = estimate + 2*std.error)) +
#   geom_point() + geom_errorbarh(height = 0.2) +
#   geom_vline(xintercept = 0, lty = 2)
cat("Linear model: adjust formula to your outcome variable\\n")
```

## Model 2 — Variable importance

```{{r importance}}
# augment(fit) |>
#   ggplot(aes(.fitted, outcome)) +
#   geom_point(alpha = 0.4) +
#   geom_abline(color = "red", lty = 2) +
#   labs(title = "Predicted vs actual", x = "Fitted", y = "Observed")
cat("Residual diagnostics: wire up after lm fit above\\n")
```
"""


def _time_modeling(read_stmt):
    return f"""## Model 1 — Time trend

```{{r time-setup}}
library(lubridate)
{read_stmt}
```

```{{r trend}}
# df |>
#   mutate(date_col = ymd(date_col)) |>
#   group_by(floor_date(date_col, "month")) |>
#   summarise(n = n(), .groups = "drop") |>
#   ggplot(aes(`floor_date(date_col, "month")`, n)) +
#   geom_line() + geom_smooth(method = "loess")
cat("Time trend: adjust date_col to your date column\\n")
```

## Model 2 — Seasonality / year-over-year

```{{r seasonality}}
# df |>
#   mutate(year = year(date_col), month = month(date_col, label = TRUE)) |>
#   group_by(year, month) |>
#   summarise(n = n(), .groups = "drop") |>
#   ggplot(aes(month, n, group = year, color = factor(year))) +
#   geom_line()
cat("Seasonality: adjust date_col above\\n")
```
"""


def _generic_modeling(read_stmt):
    return f"""## Model 1 — Summary statistics

```{{r summary-setup}}
{read_stmt}
glimpse(df)
```

```{{r summary-stats}}
# Numeric columns summary
df |>
  select(where(is.numeric)) |>
  pivot_longer(everything(), names_to = "variable", values_to = "value") |>
  group_by(variable) |>
  summarise(
    n      = n(),
    mean   = mean(value, na.rm = TRUE),
    median = median(value, na.rm = TRUE),
    sd     = sd(value, na.rm = TRUE),
    .groups = "drop"
  )
```

## Model 2 — Correlation matrix

```{{r correlations}}
numeric_df <- df |> select(where(is.numeric)) |> drop_na()
if (ncol(numeric_df) >= 2) {{
  cor_mat <- cor(numeric_df)
  cor_mat |>
    as.data.frame() |>
    rownames_to_column("var1") |>
    pivot_longer(-var1, names_to = "var2", values_to = "correlation") |>
    filter(var1 < var2) |>
    slice_max(abs(correlation), n = 20) |>
    mutate(pair = paste(var1, "↔", var2),
           pair = fct_reorder(pair, correlation)) |>
    ggplot(aes(correlation, pair, fill = correlation > 0)) +
    geom_col(show.legend = FALSE) +
    geom_vline(xintercept = 0, lty = 2) +
    labs(title = "Top correlations", x = "Pearson r", y = NULL)
}} else {{
  cat("Not enough numeric columns for correlation matrix\\n")
}}
```

## Model 3 — Top categories by frequency

```{{r top-categories}}
char_cols <- df |> select(where(is.character)) |> names()
if (length(char_cols) > 0) {{
  col <- char_cols[1]
  df |>
    count(.data[[col]], sort = TRUE) |>
    slice_max(n, n = 20) |>
    mutate(!!col := fct_reorder(.data[[col]], n)) |>
    ggplot(aes(n, .data[[col]])) +
    geom_col(fill = "#1b6ca8") +
    labs(title = paste("Top", col, "by frequency"), x = "Count", y = NULL)
}} else {{
  cat("No character columns found\\n")
}}
```
"""


# ── H3: COMMUNICATE ──────────────────────────────────────────────────────────

def build_h3(manifest, chunks, ep_num, ep_fn):
    title    = manifest.get("transcript_title", f"Episode {ep_num:03d}")
    subtitle = manifest.get("analysis_intent", "Exploring the data with R")
    concepts = manifest.get("atomic_concepts", [])
    concepts_md = " · ".join(f"`{c}`" for c in concepts[:8]) if concepts else ""

    # Extract first library list for the setup chunk
    libraries = _extract_libraries(chunks)
    for lib in ["tidyverse", "scales", "here"]:
        if lib not in libraries:
            libraries.insert(0, lib)
    lib_block = "\n".join(f"library({l})" for l in libraries)

    # Local data load
    local_files = manifest.get("local_data_files", [])
    load_lines = []
    for rel in local_files[:3]:
        name = os.path.splitext(os.path.basename(rel))[0].replace("-", "_")
        abs_path = os.path.join(BASE, rel)
        ext = os.path.splitext(rel)[1].lower()
        if ext == ".tsv":
            load_lines.append(f'{name} <- read_tsv("{abs_path}", show_col_types = FALSE)')
        elif ext == ".rds":
            load_lines.append(f'{name} <- readRDS("{abs_path}")')
        else:
            load_lines.append(f'{name} <- read_csv("{abs_path}", show_col_types = FALSE)')
    load_code = "\n".join(load_lines) if load_lines else "# Load your data here"

    # Hero chart placeholder — references last meaningful plot from h1
    hero_comment = f"# Hero chart for: {title}\n# Reproduce the best chart from Hour 1 at 1200×628 px"

    content = f"""{yaml_header(f"Hour 3 — Communicate: {title}", "From analysis to TheDataShrink™ publication", H3_THEME, 3, ep_num)}
{callout_brand(ep_num, 3, ep_fn)}

## Setup

```{{r setup}}
{lib_block}
# Brand colours
TDS_BLUE  <- "#1b6ca8"
TDS_GOLD  <- "#c8a415"
TDS_DARK  <- "#1a1a2e"
TDS_LIGHT <- "#f8f9fa"
theme_set(theme_light(base_size = 14))
```

```{{r reload-data}}
{load_code}
```

---

## Hero chart (1200 × 628 — social media ratio)

::: {{.callout-note}}
The single best chart from the analysis. Sized for YouTube thumbnail, Facebook header,
and Twitter/X card. Saved as `hero_{ep_fn}.png`.
:::

```{{r hero-chart}}
#| fig-width: 12.5
#| fig-height: 6.54

{hero_comment}
# hero <- ggplot(...) + ...
# hero
#
# ggsave(
#   here::here("output/episodes/{ep_fn}/hero_{ep_fn}.png"),
#   hero, width = 12.5, height = 6.54, dpi = 150, bg = "white"
# )
cat("Hero chart: copy best ggplot from h1 here and uncomment ggsave\\n")
```

---

## Instagram carousel (5 slides)

```{{r carousel-slide1}}
#| fig-width: 5.4
#| fig-height: 5.4

# Slide 1 — Hook
ggplot() +
  annotate("rect", xmin = 0, xmax = 1, ymin = 0, ymax = 1, fill = TDS_DARK) +
  annotate("text", x = 0.5, y = 0.72,
           label = "{title}",
           size = 8, fontface = "bold", color = "white", hjust = 0.5) +
  annotate("text", x = 0.5, y = 0.50,
           label = "{subtitle}",
           size = 4.5, color = "#cccccc", hjust = 0.5) +
  annotate("text", x = 0.5, y = 0.28,
           label = "Swipe → to find out",
           size = 4, color = TDS_GOLD, hjust = 0.5) +
  annotate("text", x = 0.5, y = 0.10,
           label = "TheDataShrink™",
           size = 3.5, color = "#888888", hjust = 0.5) +
  theme_void() + coord_fixed()
```

```{{r carousel-slide2}}
#| fig-width: 5.4
#| fig-height: 5.4
# Slide 2 — Key finding chart (compact version of hero)
# Copy and resize the hero chart here
cat("Slide 2: copy hero chart, adjust size to 5.4×5.4\\n")
```

```{{r carousel-slide3}}
#| fig-width: 5.4
#| fig-height: 5.4
# Slide 3 — Second insight
cat("Slide 3: second key chart from h1\\n")
```

```{{r carousel-slide4}}
#| fig-width: 5.4
#| fig-height: 5.4
# Slide 4 — Third insight or model result from h2
cat("Slide 4: model result or third chart\\n")
```

```{{r carousel-slide5}}
#| fig-width: 5.4
#| fig-height: 5.4
# Slide 5 — CTA
ggplot() +
  annotate("rect", xmin = 0, xmax = 1, ymin = 0, ymax = 1, fill = TDS_DARK) +
  annotate("text", x = 0.5, y = 0.78, label = "Full analysis:",
           size = 5, color = "#aaaaaa", hjust = 0.5) +
  annotate("text", x = 0.5, y = 0.62,
           label = "thedatashrink.com.au\\n/tidytuesday/{ep_num:03d}",
           size = 6, fontface = "bold", color = "white", hjust = 0.5) +
  annotate("text", x = 0.5, y = 0.42,
           label = "Code · Data · 3-hour walkthrough",
           size = 4.5, color = "#cccccc", hjust = 0.5) +
  annotate("text", x = 0.5, y = 0.24,
           label = "Follow @thedatashrink",
           size = 5, color = TDS_GOLD, fontface = "bold", hjust = 0.5) +
  annotate("text", x = 0.5, y = 0.10,
           label = "#RStats #TidyTuesday #DataScience",
           size = 3.5, color = "#888888", hjust = 0.5) +
  theme_void() + coord_fixed()
```

---

## YouTube chapter timestamps

```
0:00   Intro — {title}
1:30   Load the data
4:00   First look — key distributions
8:00   Hour 1 — EDA: exploring the patterns
18:00  Extension: going beyond David's analysis
28:00  Hour 2 — Modeling: statistical models
38:00  Key findings and interpretation
47:00  Hour 3 — Hero chart + social media pack
52:00  What to try next on your own dataset
55:00  Next week on TheDataShrink™
```

---

## Social media copy

### Facebook / LinkedIn post

```
{title} — what does the data show?

We explored this week's #TidyTuesday dataset in R.

Here's what the data reveals:

→ [Key finding 1 — fill in after running h1]
→ [Key finding 2]
→ [Key finding 3]
→ [Surprising extension finding]

Full walkthrough (3 hours of R code, charts, and commentary):
👉 thedatashrink.com.au/tidytuesday/{ep_num:03d}

#DataScience #RStats #TidyTuesday #TheDataShrink
```

### Instagram caption

```
{subtitle}

Swipe to see how data science reveals the patterns 📊

Full analysis + R code → link in bio

#RStats #TidyTuesday #DataScience #DataViz #TheDataShrink
#DataStorytelling
```

### YouTube description

```
In this episode of TheDataShrink™, we explore:
{title}

What we cover:
✅ EDA: first look at the data structure and distributions
✅ Key visualisations using ggplot2 and the tidyverse
✅ Extensions beyond David Robinson's original screencast
✅ Statistical modeling and interpretation
✅ Social media pack: hero chart + Instagram carousel

Code and data: github.com/thedatashrink/tidytuesday
Website: thedatashrink.com.au

Chapters: [see timestamps in description]

#RStats #TidyTuesday #DataScience
```

---

## Render all three hours

```{{r render-info}}
#| echo: false
cat("This episode lives at:\\n")
cat("  output/episodes/{ep_fn}/\\n\\n")
cat("To render all three hours:\\n")
cat("  quarto render h1_eda_{ep_fn}.qmd\\n")
cat("  quarto render h2_modeling_{ep_fn}.qmd\\n")
cat("  quarto render h3_communicate_{ep_fn}.qmd\\n")
```

---

*TheDataShrink™ — thedatashrink.com.au — Weekly data stories in R*
"""
    return content


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _extract_libraries(chunks):
    libs = []
    for ch in chunks:
        for m in re.finditer(r"library\(([^)]+)\)", ch["code"]):
            lib = m.group(1).strip().strip('"\'')
            if lib not in libs:
                libs.append(lib)
    return libs


def _is_library_only(code):
    lines = [l.strip() for l in code.split("\n") if l.strip() and not l.strip().startswith("#")]
    return all(re.match(r"library\(", l) or re.match(r"theme_set\(", l) for l in lines)


def _is_built(ep_dir, ep_fn, force):
    """Return True if all 3 QMDs exist and are non-scaffold (eval:true lines present)."""
    if force:
        return False
    for hour in ("h1_eda", "h2_modeling", "h3_communicate"):
        path = os.path.join(EPS_ROOT, ep_dir, f"{hour}_{ep_fn}.qmd")
        if not os.path.exists(path):
            return False
        content = open(path).read()
        # Scaffold QMDs have eval: false throughout — skip those
        if "eval: false" in content or "PUT YOUR CODE HERE" in content:
            return False
    return True


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ep", help="Only build this episode prefix (e.g. 001)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing built QMDs")
    args = parser.parse_args()

    ep_dirs = sorted(os.listdir(EPS_ROOT))
    if args.ep:
        ep_dirs = [d for d in ep_dirs if d.startswith(args.ep)]

    built = skipped = failed = 0

    for ep_dir in ep_dirs:
        ep_num_str = ep_dir[:3]
        if not ep_num_str.isdigit():
            continue
        ep_num = int(ep_num_str)
        if ep_num == 8:  # 008 already hand-built
            print(f"  ⏭  {ep_dir} — already hand-built, skipping")
            skipped += 1
            continue

        mf_path = os.path.join(EPS_ROOT, ep_dir, "episode_manifest.json")
        if not os.path.exists(mf_path):
            print(f"  ✗  {ep_dir} — no manifest")
            failed += 1
            continue

        manifest = json.load(open(mf_path))
        ep_fn = "_".join(ep_dir.split("_")[1:])  # strip leading NNN_

        # Source Rmd
        rmd_rel = manifest.get("source_files", {}).get("code_file", "")
        rmd_path = os.path.join(BASE, rmd_rel) if rmd_rel else None
        if not rmd_path or not os.path.exists(rmd_path):
            print(f"  ✗  {ep_dir} — source Rmd not found: {rmd_rel}")
            failed += 1
            continue

        if _is_built(ep_dir, ep_fn, args.force):
            print(f"  ⏭  {ep_dir} — already built")
            skipped += 1
            continue

        print(f"  ⚙  Building {ep_dir} …", end=" ", flush=True)

        try:
            chunks  = parse_rmd_chunks(rmd_path)
            chunks  = resolve_local_load(manifest, chunks)

            h1 = build_h1(manifest, chunks, ep_num, ep_fn, ep_dir)
            h2 = build_h2(manifest, chunks, ep_num, ep_fn)
            h3 = build_h3(manifest, chunks, ep_num, ep_fn)

            for hour, content in [("h1_eda", h1), ("h2_modeling", h2), ("h3_communicate", h3)]:
                out = os.path.join(EPS_ROOT, ep_dir, f"{hour}_{ep_fn}.qmd")
                with open(out, "w", encoding="utf-8") as f:
                    f.write(content)

            print(f"✓")
            built += 1
        except Exception as e:
            print(f"✗ ERROR: {e}")
            failed += 1

    print(f"\n{'─'*50}")
    print(f"✓ Built:   {built}")
    print(f"⏭ Skipped: {skipped}")
    print(f"✗ Failed:  {failed}")
    print(f"{'─'*50}")


if __name__ == "__main__":
    main()
