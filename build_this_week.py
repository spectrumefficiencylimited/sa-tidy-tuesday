"""
build_this_week.py
------------------
Full weekly pipeline for sa-tidy-tuesday.

Steps:
  1. git pull in tidytuesday/
  2. Detect the latest week from tidytuesday/data/
  3. Create Rmd template if missing
  4. build_control_table.py   — sync transcripts + Rmd files
  5. build_ker_entries.py     — enrich mapped rows, update KER
  6. build_episode_outputs.py — regenerate episode folders + reproduction_index
  7. build_intent_stubs.ps1   — regenerate R stubs
  8. build_new_super_qmds.py  — generate H1/H2/H3 super QMDs
  9. Report what changed

Usage:
  py -3 build_this_week.py
  py -3 build_this_week.py --no-pull     # skip git pull (offline)
  py -3 build_this_week.py --force-qmd   # regenerate all super QMDs
"""

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TT_DIR = ROOT / "tidytuesday"
TT_DATA = TT_DIR / "data"
SCREENCASTS_DIR = ROOT / "data-screencasts"
INDEX_PATH = ROOT / "output" / "reproduction_index.csv"


# ---------------------------------------------------------------------------
# Step 1: git pull
# ---------------------------------------------------------------------------

def git_pull():
    print("── Step 1: git pull tidytuesday ──────────────────────────────")
    result = subprocess.run(
        ["git", "pull"],
        cwd=TT_DIR,
        capture_output=True,
        text=True,
    )
    print(result.stdout.strip() or "(no output)")
    if result.returncode != 0:
        print(f"  WARNING: git pull failed: {result.stderr.strip()}")
    print()


# ---------------------------------------------------------------------------
# Step 2: detect latest week
# ---------------------------------------------------------------------------

def detect_latest_week():
    """Return (date_str, data_name) for the most recent week with local data."""
    years = sorted(
        (p for p in TT_DATA.iterdir() if p.is_dir() and p.name.isdigit()),
        reverse=True,
    )
    for year_dir in years:
        weeks = sorted(
            (p for p in year_dir.iterdir() if p.is_dir() and re.match(r"\d{4}-\d{2}-\d{2}", p.name)),
            reverse=True,
        )
        for week_dir in weeks:
            has_data = any(week_dir.glob("*.csv")) or any(week_dir.glob("*.tsv"))
            if has_data:
                date_str = week_dir.name
                data_name = _name_from_readme(week_dir) or _name_from_date(date_str)
                return date_str, data_name
    return None, None


def _name_from_readme(week_dir: Path) -> str:
    readme = week_dir / "readme.md"
    if not readme.exists():
        return ""
    text = readme.read_text(encoding="utf-8", errors="ignore")
    # Look for "# <Title>" at top of file
    m = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ""


def _name_from_date(date_str: str) -> str:
    # Fall back to parsing the year readme
    year = date_str[:4]
    year_readme = TT_DATA / year / "readme.md"
    if not year_readme.exists():
        return ""
    text = year_readme.read_text(encoding="utf-8", errors="ignore")
    # Table row format: | 16|2026-04-21 |[Global Health Spending](...) |...
    pattern = rf"\|\s*\d+\s*\|\s*{re.escape(date_str)}\s*\|\s*\[([^\]]+)\]"
    m = re.search(pattern, text)
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------------------
# Step 3: create Rmd template
# ---------------------------------------------------------------------------

def sanitize_slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug


def find_week_data_files(date_str: str) -> list[str]:
    year = date_str[:4]
    week_dir = TT_DATA / year / date_str
    if not week_dir.exists():
        return []
    files = sorted(week_dir.glob("*.csv")) + sorted(week_dir.glob("*.tsv"))
    return [f.stem for f in files if not f.stem.startswith(".")]


def create_rmd_template(date_str: str, data_name: str) -> Path:
    slug = sanitize_slug(data_name)
    date_slug = date_str.replace("-", "_")
    rmd_path = SCREENCASTS_DIR / f"{date_slug}_{slug}.Rmd"

    if rmd_path.exists():
        print(f"  Rmd already exists: {rmd_path.name}")
        return rmd_path

    tables = find_week_data_files(date_str)
    load_lines = "\n".join(
        f"{t} <- tuesdata${t}" for t in tables
    ) if tables else "# names(tuesdata)"

    rmd = f"""\
---
title: "TidyTemplate"
author: "Andrei Stoian"
date: {date_str}
output: html_document
---

```{{r setup, include=FALSE}}

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(scales)
source("R/screencast_helpers.R")
theme_set(theme_light())
```

# Load the weekly Data

```{{r Load}}

tuesdata <- load_tidyweek_data("{date_str}")

{load_lines}
```

# Explore

```{{r}}
{tables[0] if tables else "tuesdata[[1]]"} |>
  glimpse()
```

```{{r}}

```
"""
    rmd_path.write_text(rmd, encoding="utf-8")
    print(f"  Created Rmd: {rmd_path.name}")
    return rmd_path


# ---------------------------------------------------------------------------
# Step 4–8: run build scripts
# ---------------------------------------------------------------------------

def run_script(label: str, *args):
    print(f"── {label} ──────────────────────────────")
    result = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    for line in (result.stdout + result.stderr).strip().splitlines():
        print(f"  {line}")
    if result.returncode != 0:
        print(f"  ERROR: exit code {result.returncode}")
    print()


def run_ps1(label: str, script: str):
    print(f"── {label} ──────────────────────────────")
    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", script],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    for line in (result.stdout + result.stderr).strip().splitlines():
        print(f"  {line}")
    print()


# ---------------------------------------------------------------------------
# Step 9: report
# ---------------------------------------------------------------------------

def load_index() -> list[dict]:
    if not INDEX_PATH.exists():
        return []
    with INDEX_PATH.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def report(date_str: str, data_name: str, rmd_path: Path):
    print("── Summary ───────────────────────────────────────────────────")
    print(f"  Week    : {date_str}  —  {data_name}")
    print(f"  Rmd     : {rmd_path.relative_to(ROOT).as_posix()}")

    rows = load_index()
    slug = sanitize_slug(data_name)
    date_slug = date_str.replace("-", "_")
    match = next(
        (r for r in rows if date_slug in r.get("folder_name", "") or slug in r.get("folder_name", "")),
        None,
    )
    if match:
        print(f"  Queue   : #{match['queue_position']}  status={match['ker_status']}  repro={match['reproduction_status']}")

    super_qmds = sorted(ROOT.glob(f"output/super_qmd/*{slug}*"))
    for q in super_qmds:
        print(f"  SuperQMD: {q.relative_to(ROOT).as_posix()}")

    print()
    print("  What to do next:")
    print(f"    1. Open {rmd_path.name} and fill in the analysis")
    print(f"    2. Open the SuperQMD above — it maps Hour 1 / Hour 2 / Hour 3")
    print( "    3. When done, run: py -3 build_ker_entries.py")
    print( "    4. Publish:        py -3 build_site.py --episode " +
           sanitize_slug(data_name))
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-pull", action="store_true", help="Skip git pull")
    parser.add_argument("--force-qmd", action="store_true", help="Regenerate all super QMDs")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    print()
    print("=" * 62)
    print("  sa-tidy-tuesday -- weekly build")
    print("=" * 62)
    print()

    if not args.no_pull:
        git_pull()

    print("── Step 2: detect latest week ────────────────────────────────")
    date_str, data_name = detect_latest_week()
    if not date_str:
        print("  ERROR: could not detect latest week from tidytuesday/data/")
        sys.exit(1)
    print(f"  Latest week: {date_str}  —  {data_name}")
    print()

    print("── Step 3: Rmd template ──────────────────────────────────────")
    rmd_path = create_rmd_template(date_str, data_name)
    print()

    run_script("Step 4: build_control_table", "build_control_table.py")
    run_script("Step 5: build_ker_entries", "build_ker_entries.py")
    run_script("Step 6: build_episode_outputs", "build_episode_outputs.py")
    run_ps1("Step 7: build_intent_stubs", "build_intent_stubs.ps1")

    qmd_args = ["build_new_super_qmds.py"]
    if args.force_qmd:
        qmd_args.append("--force")
    run_script("Step 8: build_new_super_qmds", *qmd_args)

    report(date_str, data_name, rmd_path)


if __name__ == "__main__":
    main()
