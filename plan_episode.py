"""
plan_episode.py — Generate an analysis plan for a TidyTuesday episode.

Steps:
  1. Find next unplanned episode (or use --ep / --folder)
  2. Download TidyTuesday data + README from GitHub
  3. Inspect real column names and types
  4. Load CONCEPT_INDEX.md
  5. Call Claude API → generates episode_plan.md
  6. Print plan for your review

Usage:
  python3 plan_episode.py                              # next unplanned
  python3 plan_episode.py --ep 109                    # by queue position
  python3 plan_episode.py --folder 109_fatal_car_crashes_on_4_20
  python3 plan_episode.py --force                     # overwrite existing plan
"""

import argparse
import csv
import io
import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

import anthropic

ROOT         = Path(__file__).resolve().parent
EPISODES_DIR = ROOT / "output" / "episodes"
REPRO_INDEX  = ROOT / "output" / "reproduction_index.csv"
CONCEPT_FILE = ROOT / "CONCEPT_INDEX.md"

GH_API  = "https://api.github.com/repos/rfordatascience/tidytuesday/contents/data/{year}/{date}"
GH_RAW  = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/{year}/{date}/{name}"

MAX_CSV_ROWS   = 8
MAX_README_LEN = 4000
MAX_CONCEPT_LEN = 8000


# ── GitHub helpers ────────────────────────────────────────────────────────────

def _get(url: str) -> bytes | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "sa-tidy-tuesday/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read()
    except Exception as e:
        print(f"  fetch failed: {url} — {e}")
        return None


def fetch_tt_files(date_str: str) -> tuple[dict, str]:
    """Return (csv_contents_by_name, readme_text) for a TidyTuesday date."""
    year = date_str[:4]
    listing = _get(GH_API.format(year=year, date=date_str))
    if not listing:
        return {}, ""

    files = json.loads(listing)
    csvs, readme = {}, ""

    for f in files:
        name = f["name"]
        url  = f.get("download_url", "")
        if not url:
            continue
        if name.lower().endswith((".md", ".qmd")) and "readme" in name.lower():
            raw = _get(url)
            if raw:
                readme = raw.decode("utf-8", errors="ignore")
        elif name.lower().endswith(".csv"):
            raw = _get(url)
            if raw:
                csvs[name] = raw.decode("utf-8", errors="ignore")

    return csvs, readme


# ── Data inspection ───────────────────────────────────────────────────────────

def inspect_csv(content: str, filename: str) -> dict:
    reader = csv.DictReader(io.StringIO(content))
    rows = []
    for i, row in enumerate(reader):
        if i >= MAX_CSV_ROWS:
            break
        rows.append(dict(row))

    if not rows:
        return {"filename": filename, "columns": [], "types": {}, "sample": []}

    cols = list(rows[0].keys())
    types = {}
    for col in cols:
        vals = [r[col] for r in rows if r.get(col, "").strip()]
        if not vals:
            types[col] = "unknown"
            continue
        try:
            [float(v.replace(",", "").replace("%", "")) for v in vals]
            types[col] = "numeric"
        except ValueError:
            # Detect date-like
            if any(re.search(r"\d{4}", v) for v in vals):
                types[col] = "date/year"
            else:
                types[col] = "character"

    return {
        "filename": filename,
        "n_rows_sampled": len(rows),
        "n_cols": len(cols),
        "columns": cols,
        "types": types,
        "sample": rows[:3],
    }


def format_data_summary(summaries: list[dict]) -> str:
    if not summaries:
        return "(no data files downloaded)"
    lines = []
    for s in summaries:
        lines.append(f"### {s['filename']}  ({s['n_cols']} columns)")
        for col in s["columns"]:
            lines.append(f"  - `{col}` — {s['types'].get(col,'?')}")
        lines.append("")
        lines.append("**Sample rows:**")
        lines.append("```")
        for row in s["sample"]:
            lines.append(json.dumps(row))
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


# ── Episode discovery ─────────────────────────────────────────────────────────

def find_episode_folder(ep_arg: str | None, folder_arg: str | None, force: bool) -> Path:
    if folder_arg:
        p = EPISODES_DIR / folder_arg
        if not p.exists():
            sys.exit(f"Folder not found: {p}")
        return p

    if ep_arg:
        matches = [d for d in EPISODES_DIR.iterdir() if d.is_dir() and d.name.startswith(ep_arg + "_")]
        if not matches:
            # Try numeric prefix only
            matches = [d for d in EPISODES_DIR.iterdir() if d.is_dir() and re.match(rf"0*{ep_arg}_", d.name)]
        if not matches:
            sys.exit(f"No episode folder matching --ep {ep_arg}")
        return sorted(matches)[0]

    # Auto: first episode without episode_plan.md
    if REPRO_INDEX.exists():
        with open(REPRO_INDEX) as f:
            for row in csv.DictReader(f):
                folder = row.get("folder_name", "")
                d = EPISODES_DIR / folder
                if d.is_dir():
                    plan = d / "episode_plan.md"
                    if force or not plan.exists():
                        return d

    # Fallback: scan alphabetically
    for d in sorted(EPISODES_DIR.iterdir()):
        if d.is_dir() and (d / "episode_manifest.json").exists():
            if force or not (d / "episode_plan.md").exists():
                return d

    sys.exit("All episodes already have episode_plan.md. Use --force to regenerate.")


# ── Plan generation ───────────────────────────────────────────────────────────

SYSTEM = """\
You are SA Andrei — the Brain entity of TheDataShrink™.
You think like a senior data scientist who has watched 410 TidyTuesday screencasts.
You are precise, use real column names, and form concrete analytical opinions.
You do NOT hedge. You pick the best angle and argue for it.
"""

PLAN_PROMPT = """\
## Episode to Plan

**Title:** {title}
**TidyTuesday date:** {date}
**Analysis type:** {atype}
**Pattern signature:** {pattern}
**Analysis intent:** {intent}

---

## TidyTuesday README

{readme}

---

## Dataset Structure (real column names + types)

{data_summary}

---

## CONCEPT INDEX (what we know works and fails)

{concept_index}

---

## Your Task

Generate `episode_plan.md` — a concrete, opinionated analysis plan for this episode.
Use real column names throughout. Think like David Robinson would approach this live.

Structure your output EXACTLY as follows (use these headings):

# Episode Plan: {title}

## Dataset Summary
[2-3 sentences: what is this data, what is the grain (one row = one what?), what time span]

## The Story
[1 paragraph: the most interesting angle. What question will the episode answer?
 What will surprise the viewer? Be opinionated — pick one story and commit to it.]

## Applicable Concepts
[For each CONCEPT_INDEX concept that WORKS for this data:]
- `concept_key` — **why it works**: [cite actual column names from this dataset]

## Concepts That Don't Apply
[For each concept where FAILS_WHEN matches this data:]
- `concept_key` — **why it fails**: [specific reason for this dataset]

## H1 — EDA Plan (Hour 1)
[Ordered steps with real R code snippets using actual column names:]

### Step 1: Load & Inspect
```r
# exact data loading code
```

### Step 2: [Specific question 1]
```r
# actual ggplot or dplyr code using real column names
```

### Step 3: [Specific question 2]
```r
# actual code
```

[Continue for 4-5 steps total. End with:]

### Key H1 Finding
[The one sentence that will be the YouTube hook]

## H2 — Modeling Plan (Hour 2)
[What model, what outcome, what predictors — using real column names.
 Why this model fits. What interaction effects to test.]

```r
# skeleton modeling code with real variable names
```

## H3 — Communication Plan (Hour 3)
**Hero chart concept:** [describe the single best chart at 1200×628]
**Instagram hook:** [the first slide text — what stops the scroll]
**YouTube thumbnail text:** [3-5 words that will get clicked]
**Shiny/Observable idea:** [one interactive element that adds value]

---
[End of plan]
"""


def generate_plan(manifest: dict, summaries: list[dict], readme: str) -> str:
    concept_index = CONCEPT_FILE.read_text(encoding="utf-8")[:MAX_CONCEPT_LEN]
    data_summary  = format_data_summary(summaries)
    readme_trunc  = readme[:MAX_README_LEN] if readme else "(no README found)"

    prompt = PLAN_PROMPT.format(
        title        = manifest.get("transcript_title", ""),
        date         = manifest.get("data_source", ""),
        atype        = manifest.get("analysis_type", "EDA"),
        pattern      = manifest.get("pattern_signature", ""),
        intent       = manifest.get("analysis_intent", ""),
        readme       = readme_trunc,
        data_summary = data_summary,
        concept_index = concept_index,
    )

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model      = "claude-sonnet-4-6",
        max_tokens = 4096,
        system     = SYSTEM,
        messages   = [{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate episode_plan.md for a TidyTuesday episode")
    parser.add_argument("--ep",     help="Queue position prefix (e.g. 109)")
    parser.add_argument("--folder", help="Episode folder name")
    parser.add_argument("--force",  action="store_true", help="Overwrite existing plan")
    args = parser.parse_args()

    ep_dir   = find_episode_folder(args.ep, args.folder, args.force)
    mf_path  = ep_dir / "episode_manifest.json"
    plan_path = ep_dir / "episode_plan.md"

    if plan_path.exists() and not args.force:
        print(f"Plan already exists: {plan_path}")
        print("Use --force to regenerate.")
        sys.exit(0)

    manifest = json.loads(mf_path.read_text())
    print(f"\n{'─'*60}")
    print(f"Planning: {ep_dir.name}")
    print(f"{'─'*60}")

    # Extract TidyTuesday date
    date_str = re.search(r"\d{4}-\d{2}-\d{2}", manifest.get("data_source", ""))
    date_str = date_str.group(0) if date_str else None

    csvs, readme = {}, ""
    summaries = []

    if date_str:
        print(f"Fetching TidyTuesday data for {date_str} …")
        csvs, readme = fetch_tt_files(date_str)
        if csvs:
            print(f"  Downloaded: {', '.join(csvs.keys())}")
            summaries = [inspect_csv(content, name) for name, content in csvs.items()]
        else:
            print("  No CSV files found — plan will be based on manifest + README only")
        if readme:
            print(f"  README: {len(readme)} chars")
    else:
        print("  No TidyTuesday date found in manifest — fetching skipped")

    print("\nCalling Claude to generate plan …")
    plan_text = generate_plan(manifest, summaries, readme)

    plan_path.write_text(plan_text, encoding="utf-8")
    print(f"\n✓ Written: {plan_path}")
    print(f"\n{'═'*60}")
    print(plan_text)
    print(f"{'═'*60}")
    print(f"\nReview and edit: {plan_path}")
    print(f"Then run: python3 generate_episode.py --folder {ep_dir.name}")


if __name__ == "__main__":
    main()
