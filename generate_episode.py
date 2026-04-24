"""
generate_episode.py — Generate h1/h2/h3 QMDs from an approved episode_plan.md.

Reads the plan Andrei has reviewed, then calls Claude to write real, runnable
R code for each hour. The code uses actual column names from the plan.

Usage:
  python3 generate_episode.py --folder 109_fatal_car_crashes_on_4_20
  python3 generate_episode.py --ep 109
  python3 generate_episode.py --force   # overwrite existing QMDs
"""

import argparse
import json
import re
import sys
from pathlib import Path

import anthropic

ROOT         = Path(__file__).resolve().parent
EPISODES_DIR = ROOT / "output" / "episodes"

THEMES = {"h1": "flatly", "h2": "cosmo", "h3": "litera"}

SYSTEM = """\
You are SA Andrei — the Brain entity of TheDataShrink™.
You write clean, idiomatic R using the tidyverse.
Rules:
- Use |> not %>%
- Use real column names from the episode plan
- All code chunks have #| eval: true (except interactive/Shiny)
- No placeholder comments like # YOUR CODE HERE
- No library() calls for packages already in setup chunk
- Use fct_reorder() before plotting categorical variables
- theme_set(theme_light(base_size = 13)) in setup, then theme_light() in individual plots
- Brand colours: TDS_BLUE <- "#1b6ca8"  TDS_GOLD <- "#c8a415"
"""


# ── QMD builders ─────────────────────────────────────────────────────────────

def yaml_header(title: str, subtitle: str, hour: str) -> str:
    theme = THEMES.get(hour, "flatly")
    return f"""---
title: "{title}"
subtitle: "{subtitle}"
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
editor: visual
---
"""


def brand_callout(fn: str) -> str:
    return f"""
::: {{.callout-tip}}
## TheDataShrink™ — Data stories worth sharing.
Episode: `{fn}` | [All episodes](https://thedatashrink.com.au/tidytuesday) | [YouTube](#) | [Instagram](#)
:::
"""


def generate_h1(manifest: dict, plan: str, fn: str) -> str:
    client = anthropic.Anthropic()

    prompt = f"""Write the COMPLETE Quarto QMD body for Hour 1 (EDA) of this TidyTuesday episode.

## Episode Metadata
- Function name: `{fn}`
- Data source: {manifest.get("data_source", "")}
- Analysis type: {manifest.get("analysis_type", "EDA")}

## Approved Episode Plan
{plan}

---

Write ONLY the body content (no YAML header — that is added separately).
Start after the brand callout block.

Requirements:
- Real, runnable R code using actual column names from the plan
- Setup chunk: library(tidyverse), library(here), tidytuesdayR::tt_load() or read_csv(), TDS brand colours, theme_set()
- 4-6 code chunks following the H1 EDA Plan steps exactly
- Each chunk preceded by a ## section header and 1-2 sentences explaining WHAT we are looking at and WHY
- End with a ## Key Finding section (blockquote) — the one-sentence YouTube hook from the plan
- Cross-reference to h2 at the bottom

Format chunks as:
```{{r}}
#| label: descriptive-label
#| fig-width: 9
#| fig-height: 5
[actual R code]
```

The narrative text between chunks should sound like David Robinson narrating live —
direct, curious, building toward the finding.
"""

    resp = client.messages.create(
        model      = "claude-sonnet-4-6",
        max_tokens = 4096,
        system     = SYSTEM,
        messages   = [{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def generate_h2(manifest: dict, plan: str, h1_body: str, fn: str) -> str:
    client = anthropic.Anthropic()

    prompt = f"""Write the COMPLETE Quarto QMD body for Hour 2 (Modeling) of this TidyTuesday episode.

## Episode Metadata
- Function name: `{fn}`
- Data source: {manifest.get("data_source", "")}
- Analysis type: {manifest.get("analysis_type", "EDA")}

## Approved Episode Plan (H2 Modeling section is your primary guide)
{plan}

## What Hour 1 EDA Found (use this to inform what to model)
{h1_body[:2000]}

---

Write ONLY the body content (no YAML header).

Requirements:
- Setup chunk that loads the same data as H1 (one read, kept DRY)
- 3-5 modeling chunks following the H2 Modeling Plan exactly
- Use broom::tidy(), broom::glance() for model output
- If bootstrapping: use rsample::bootstraps()
- If text: use tidytext
- Each chunk preceded by ## section header + 1-2 sentences on what we are testing and why
- ## Model Story section at the end — what did the model reveal that EDA couldn't?
- Cross-reference to h1 and h3 at the bottom
"""

    resp = client.messages.create(
        model      = "claude-sonnet-4-6",
        max_tokens = 4096,
        system     = SYSTEM,
        messages   = [{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def generate_h3(manifest: dict, plan: str, h1_body: str, fn: str) -> str:
    client = anthropic.Anthropic()

    prompt = f"""Write the COMPLETE Quarto QMD body for Hour 3 (Communicate) of this TidyTuesday episode.

## Episode Metadata
- Function name: `{fn}`
- Data source: {manifest.get("data_source", "")}

## Approved Episode Plan (H3 Communication section is your primary guide)
{plan}

## Hour 1 EDA (for context on what was found)
{h1_body[:1500]}

---

Write ONLY the body content (no YAML header).

Requirements:
- Hero chart chunk: production-quality ggplot, fig-width: 12.5, fig-height: 6.54,
  saved with ggsave() at dpi=150. This IS the Instagram/YouTube thumbnail chart.
- ggsave() line: `ggsave("hero_{fn}.png", width=12.5, height=6.54, dpi=150)`
- ## Instagram Carousel Copy section (5 slides, copy-ready)
- ## YouTube Chapter Timestamps section
- ## Facebook Post Template section
- ## SEO Metadata section (YAML code block to paste into the published page)
- Optional: one Shiny/Observable interactive chunk (eval: false, clearly labelled)
- Cross-reference to h1 and h2 at the bottom

The hero chart must use real column names and the story from the plan.
It should be the single strongest visual from the episode — the one chart
that makes a viewer stop scrolling on Instagram.
"""

    resp = client.messages.create(
        model      = "claude-sonnet-4-6",
        max_tokens = 4096,
        system     = SYSTEM,
        messages   = [{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


# ── Episode discovery ─────────────────────────────────────────────────────────

def find_episode_folder(ep_arg: str | None, folder_arg: str | None) -> Path:
    if folder_arg:
        p = EPISODES_DIR / folder_arg
        if not p.exists():
            sys.exit(f"Folder not found: {p}")
        return p

    if ep_arg:
        matches = [d for d in EPISODES_DIR.iterdir()
                   if d.is_dir() and re.match(rf"0*{ep_arg}_", d.name)]
        if not matches:
            sys.exit(f"No episode folder matching --ep {ep_arg}")
        return sorted(matches)[0]

    sys.exit("Provide --ep or --folder")


# ── Assemble QMD ──────────────────────────────────────────────────────────────

def assemble_qmd(hour: str, title: str, subtitle: str, fn: str, body: str) -> str:
    return yaml_header(title, subtitle, hour) + brand_callout(fn) + "\n" + body


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate h1/h2/h3 QMDs from approved episode_plan.md")
    parser.add_argument("--ep",     help="Queue position prefix (e.g. 109)")
    parser.add_argument("--folder", help="Episode folder name")
    parser.add_argument("--force",  action="store_true", help="Overwrite existing QMDs")
    parser.add_argument("--hour",   choices=["h1", "h2", "h3"], help="Generate only this hour")
    args = parser.parse_args()

    ep_dir    = find_episode_folder(args.ep, args.folder)
    mf_path   = ep_dir / "episode_manifest.json"
    plan_path = ep_dir / "episode_plan.md"

    if not plan_path.exists():
        sys.exit(f"No episode_plan.md found in {ep_dir.name}\nRun plan_episode.py first.")

    manifest  = json.loads(mf_path.read_text())
    plan_text = plan_path.read_text(encoding="utf-8")
    fn        = manifest["function_name"]
    title_raw = manifest.get("transcript_title", fn)

    print(f"\n{'─'*60}")
    print(f"Generating QMDs: {ep_dir.name}")
    print(f"{'─'*60}")

    h1_body = h2_body = h3_body = ""

    # ── H1 ──
    h1_path = ep_dir / f"h1_eda_{fn}.qmd"
    if not args.hour or args.hour == "h1":
        if h1_path.exists() and not args.force:
            print(f"  SKIP h1 (exists) — use --force to overwrite")
            h1_body = h1_path.read_text(encoding="utf-8")
        else:
            print(f"  Generating h1 …", end=" ", flush=True)
            h1_body = generate_h1(manifest, plan_text, fn)
            qmd = assemble_qmd("h1", f"Hour 1 — EDA: {title_raw}",
                               "Reproduce + extend David Robinson's original analysis | TheDataShrink™",
                               fn, h1_body)
            h1_path.write_text(qmd, encoding="utf-8")
            print(f"✓  {h1_path.name}")
    else:
        if h1_path.exists():
            h1_body = h1_path.read_text(encoding="utf-8")

    # ── H2 ──
    h2_path = ep_dir / f"h2_modeling_{fn}.qmd"
    if not args.hour or args.hour == "h2":
        if h2_path.exists() and not args.force:
            print(f"  SKIP h2 (exists) — use --force to overwrite")
            h2_body = h2_path.read_text(encoding="utf-8")
        else:
            print(f"  Generating h2 …", end=" ", flush=True)
            h2_body = generate_h2(manifest, plan_text, h1_body, fn)
            qmd = assemble_qmd("h2", f"Hour 2 — Modeling: {title_raw}",
                               "Go deeper with statistics and models | TheDataShrink™",
                               fn, h2_body)
            h2_path.write_text(qmd, encoding="utf-8")
            print(f"✓  {h2_path.name}")

    # ── H3 ──
    h3_path = ep_dir / f"h3_communicate_{fn}.qmd"
    if not args.hour or args.hour == "h3":
        if h3_path.exists() and not args.force:
            print(f"  SKIP h3 (exists) — use --force to overwrite")
        else:
            print(f"  Generating h3 …", end=" ", flush=True)
            h3_body = generate_h3(manifest, plan_text, h1_body, fn)
            qmd = assemble_qmd("h3", f"Hour 3 — Communicate: {title_raw}",
                               "From analysis to publication | TheDataShrink™",
                               fn, h3_body)
            h3_path.write_text(qmd, encoding="utf-8")
            print(f"✓  {h3_path.name}")

    print(f"\n✓ Done — open in RStudio and render with quarto render")
    print(f"  Next episode: python3 plan_episode.py")


if __name__ == "__main__":
    main()
