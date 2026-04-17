import argparse
import csv
import json
import re
from pathlib import Path

from build_ker_entries import (
    ROOT,
    build_adaptation_plan,
    build_data_flow,
    build_function_candidates,
    build_reusable_patterns,
    build_thought_process_map,
    detect_features,
    extract_data_source,
    infer_analysis_intent,
    infer_analysis_type,
    infer_pattern_signature,
    load_control_rows,
    read_text,
    topic_from_title,
)


OUTPUT_ROOT = ROOT / "output"
EPISODES_ROOT = OUTPUT_ROOT / "episodes"
INDEX_PATH = OUTPUT_ROOT / "reproduction_index.csv"
README_PATH = OUTPUT_ROOT / "README.md"

INDEX_COLUMNS = [
    "queue_position",
    "folder_name",
    "function_name",
    "transcript_title",
    "ker_status",
    "reproduction_status",
    "transcript_exists",
    "code_exists",
    "local_data_count",
    "external_dependency_count",
    "required_packages",
    "data_source",
    "analysis_type",
    "pattern_signature",
]

DATA_FILE_PATTERN = re.compile(r".+\.(csv|tsv|txt|xlsx|xls|json|geojson|rds|rda|rdata|feather|parquet)$", re.IGNORECASE)


def sanitize_slug(text):
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug or "episode"


def as_relative(path):
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def extract_code_chunks(rmd_text):
    chunks = []
    current_lines = []
    chunk_label = ""
    in_chunk = False

    for line in rmd_text.splitlines():
        if line.startswith("```{r"):
            in_chunk = True
            current_lines = []
            chunk_header = line.strip()
            match = re.match(r"```{r\s*([^,}]*)", chunk_header)
            chunk_label = match.group(1).strip() if match else ""
            if not chunk_label:
                chunk_label = f"chunk_{len(chunks) + 1:02d}"
            continue

        if in_chunk and line.strip() == "```":
            chunks.append({"label": chunk_label, "code": "\n".join(current_lines).rstrip()})
            in_chunk = False
            current_lines = []
            chunk_label = ""
            continue

        if in_chunk:
            current_lines.append(line)

    return chunks


def render_extracted_r_script(chunks):
    lines = [
        "# Auto-generated from the episode R Markdown file.",
        "# This script preserves code chunks in source order for reproducibility checks.",
        "",
    ]

    for chunk in chunks:
        lines.append(f"# ---- {chunk['label']} ----")
        if chunk["code"]:
            lines.append(chunk["code"])
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def extract_tt_dates(rmd_text):
    dates = set(re.findall(r'tt_load\(["\'](\d{4}-\d{2}-\d{2})["\']\)', rmd_text))
    dates.update(re.findall(r"rfordatascience/tidytuesday/master/data/\d{4}/(\d{4}-\d{2}-\d{2})/", rmd_text))
    return sorted(dates)


def extract_local_reads(rmd_text):
    reads = set(
        re.findall(
            r'(?:read_csv|read_tsv|read_delim|read_excel|read_xlsx|read_rds|readRDS|vroom|st_read)\(["\']([^"\']+)["\']',
            rmd_text,
        )
    )
    return sorted(reads)


def find_local_data_files(rmd_text):
    files = []
    seen = set()

    for date in extract_tt_dates(rmd_text):
        data_dir = ROOT / "tidytuesday" / "data" / date[:4] / date
        if data_dir.exists():
            for path in sorted(data_dir.iterdir()):
                if path.is_file() and DATA_FILE_PATTERN.match(path.name):
                    key = path.resolve()
                    if key not in seen:
                        files.append(path)
                        seen.add(key)

    for raw_path in extract_local_reads(rmd_text):
        candidate = ROOT / raw_path
        if candidate.exists() and candidate.is_file():
            key = candidate.resolve()
            if key not in seen:
                files.append(candidate)
                seen.add(key)

    return files


def find_reference_files(data_files):
    references = []
    seen = set()
    for data_file in data_files:
        parent = data_file.parent
        if not parent.exists():
            continue
        for candidate in sorted(parent.iterdir()):
            if not candidate.is_file():
                continue
            if candidate.resolve() == data_file.resolve():
                continue
            if DATA_FILE_PATTERN.match(candidate.name) or candidate.suffix.lower() in {".md", ".png", ".jpg", ".jpeg"}:
                key = candidate.resolve()
                if key not in seen:
                    references.append(candidate)
                    seen.add(key)
    return references


def detect_external_dependencies(rmd_text, features, local_data_files):
    dependencies = []
    remote_load_pattern = r'(?:read_csv|read_tsv|read_delim|read_excel|read_xlsx|vroom|read_html|GET|download\.file|fromJSON)\(["\']https?://'

    if extract_tt_dates(rmd_text) and not local_data_files:
        dependencies.append("tidytuesdayR::tt_load is used and no local TidyTuesday files were matched")
    if features["scraping"]:
        dependencies.append("web scraping or remote API logic detected")
    if re.search(remote_load_pattern, rmd_text) and not local_data_files:
        dependencies.append("remote file or API download detected in code")

    deduped = []
    for dependency in dependencies:
        if dependency not in deduped:
            deduped.append(dependency)
    return deduped


def detect_execution_notes(rmd_text, local_data_files):
    notes = []

    if re.search(r"\b(View)\(", rmd_text):
        notes.append("interactive `View()` calls are present and should be skipped or replaced in automated runs")
    if re.search(r"\b(ggplotly|plotlyOutput|DT::datatable)\(", rmd_text):
        notes.append("htmlwidget or interactive plotting calls are present")
    if re.search(r"\bclipr::|write_clip\(", rmd_text):
        notes.append("clipboard interaction is present")
    if extract_tt_dates(rmd_text) and local_data_files:
        notes.append("local TidyTuesday files were matched, so you can use `load_tidyweek_data()` and avoid a GitHub PAT")
    if extract_tt_dates(rmd_text) and not local_data_files:
        notes.append("this episode depends on `tidytuesdayR::tt_load()`, so set `GITHUB_PAT` if GitHub rate limits appear")

    deduped = []
    for note in notes:
        if note not in deduped:
            deduped.append(note)
    return deduped


def infer_reproduction_status(row, transcript_text, rmd_text, local_data_files, external_dependencies):
    if row["ker_status"] == "needs_mapping" or not row["code_file"]:
        return "blocked_needs_mapping"
    if not transcript_text:
        return "blocked_missing_transcript"
    if not rmd_text:
        return "blocked_missing_code"
    if local_data_files and not external_dependencies:
        return "ready_local"
    if local_data_files and external_dependencies:
        return "ready_with_external_steps"
    if external_dependencies:
        return "needs_external_sources"
    return "needs_data_review"


def build_reproduction_steps(row, rmd_text, local_data_files, external_dependencies):
    steps = [
        "1. Start from the control-table metadata and confirm the transcript, code file, and function identity match this episode.",
        "2. Read the transcript first to understand the story, then inspect the source `.Rmd` to locate the main transformation and plotting chunks.",
    ]

    if extract_tt_dates(rmd_text) and local_data_files:
        steps.append(
            "3. Prefer the local mirrored TidyTuesday files or `load_tidyweek_data()` from `R/screencast_helpers.R`; that keeps reproduction local and avoids the GitHub PAT requirement."
        )
    elif local_data_files:
        steps.append(
            "3. Load the local dataset assets captured for this episode before falling back to remote downloads or `tidytuesdayR::tt_load`."
        )
    elif extract_tt_dates(rmd_text):
        steps.append(
            "3. This episode uses `tidytuesdayR::tt_load()` without a matched local mirror, so expect a GitHub-backed load and set `GITHUB_PAT` if you hit API rate limits."
        )
    else:
        steps.append(
            "3. Rebuild the source data from the code path because no local dataset files were confidently matched by the builder."
        )

    if external_dependencies:
        steps.append(
            "4. Handle the external dependencies called out below before expecting a fully offline reproduction."
        )
    else:
        steps.append(
            "4. Run the extracted episode script in chunk order and compare the resulting tables and plots to the original screencast intent."
        )

    steps.extend(
        [
            "5. Use the KER thought process map and adaptation plan in this folder when rewriting the episode into a cleaner reusable analysis.",
            "6. Mark the episode as implemented or reviewed only after the reproduced workflow runs cleanly in the local environment.",
        ]
    )

    return steps


def build_qmd_text(row, features, transcript_text, local_data_files, reference_files, external_dependencies, execution_notes, chunks, reproduction_status):
    title = row["transcript_title"]
    function_name = row["function_name"] or sanitize_slug(title)
    topic = topic_from_title(title)
    data_source = row["data_source"] or extract_data_source(row, read_text(row["code_file"]))
    analysis_type = row["analysis_type"] or infer_analysis_type(row, features)
    analysis_intent = row["analysis_intent"] or infer_analysis_intent(row, features)
    pattern_signature = row["pattern_signature"] or infer_pattern_signature(row, features)
    transcript_preview = " ".join(transcript_text.split())[:450].strip()
    transcript_preview = transcript_preview + ("..." if len(" ".join(transcript_text.split())) > 450 else "")
    transcript_preview = transcript_preview or "Transcript text was not available when this guide was generated."

    thought_lines = "\n".join(f"- `{line}`" for line in build_thought_process_map(topic, features))
    data_flow_lines = "\n".join(f"- `{line}`" for line in build_data_flow(features))
    pattern_lines = "\n".join(f"- `{line}`" for line in build_reusable_patterns(features))
    function_lines = "\n".join(f"- `{line}`" for line in build_function_candidates(features))
    adaptation_lines = "\n".join(f"- `{line}`" for line in build_adaptation_plan(features))

    package_lines = "\n".join(f"- `{package}`" for package in features["libraries"]) or "- No explicit `library()` calls were detected."
    data_lines = "\n".join(f"- `{as_relative(path)}`" for path in local_data_files) or "- No local dataset files were resolved automatically."
    reference_lines = "\n".join(f"- `{as_relative(path)}`" for path in reference_files[:12]) or "- No nearby readme or asset files were captured."
    external_lines = "\n".join(f"- {dependency}" for dependency in external_dependencies) or "- No external dependencies were detected from the code scan."
    execution_lines = "\n".join(f"- {note}" for note in execution_notes) or "- No special interactive execution notes were detected."
    chunk_lines = "\n".join(f"- `{chunk['label']}`" for chunk in chunks[:20]) or "- No executable R chunks were extracted."
    step_lines = "\n".join(f"- {step}" for step in build_reproduction_steps(row, rmd_text=read_text(row["code_file"]), local_data_files=local_data_files, external_dependencies=external_dependencies))

    return f"""---
title: "Reproduction Guide: {title}"
subtitle: "Ordered episode output built from the control table and KER"
format:
  html:
    theme: flatly
    toc: true
    toc-depth: 2
    code-fold: show
execute:
  echo: false
  warning: false
  message: false
---

## Episode Snapshot

- `function_name`: `{function_name}`
- `ker_status`: `{row["ker_status"] or "untracked"}`
- `reproduction_status`: `{reproduction_status}`
- `transcript_file`: `{row["transcript_file"] or "(missing)"}`
- `code_file`: `{row["code_file"] or "(missing)"}`
- `data_source`: {data_source or "Not resolved"}
- `analysis_type`: `{analysis_type or "Not resolved"}`
- `pattern_signature`: `{pattern_signature or "Not resolved"}`

::: {{.callout-note}}
## Why this episode
This output was generated in control-table order so we can reproduce the repository one episode at a time from the top of the queue.

The KER classifies this episode as **{analysis_type or "unknown"}** and the main intent is:

{analysis_intent or "Intent was not resolved by the current metadata."}
:::

## Transcript Preview

{transcript_preview}

## Required Packages

{package_lines}

## Local Data Assets

{data_lines}

## Nearby Reference Files

{reference_lines}

## External Dependencies

{external_lines}

## Execution Notes

{execution_lines}

## Extracted Code Chunks

{chunk_lines}

## Thought Process Map

{thought_lines}

## Data Transformation Flow

{data_flow_lines}

## Reusable Patterns

{pattern_lines}

## Function Candidates

{function_lines}

## Reproduction Steps

{step_lines}

## Adaptation Plan

{adaptation_lines}

## Source Artifacts in This Folder

- `episode_guide.qmd`: this guided reproduction document
- `episode_source.R`: R code extracted from the original episode `.Rmd`
- `episode_manifest.json`: machine-readable metadata for automation and checks
"""


def build_manifest(row, features, transcript_text, rmd_text, local_data_files, reference_files, external_dependencies, execution_notes, reproduction_status, folder_name):
    return {
        "queue_position": None,
        "folder_name": folder_name,
        "transcript_title": row["transcript_title"],
        "function_name": row["function_name"] or sanitize_slug(row["transcript_title"]),
        "ker_status": row["ker_status"],
        "reproduction_status": reproduction_status,
        "source_files": {
            "transcript_file": row["transcript_file"],
            "code_file": row["code_file"],
        },
        "source_exists": {
            "transcript": bool(transcript_text),
            "code": bool(rmd_text),
        },
        "data_source": row["data_source"] or extract_data_source(row, rmd_text),
        "analysis_intent": row["analysis_intent"] or infer_analysis_intent(row, features),
        "analysis_type": row["analysis_type"] or infer_analysis_type(row, features),
        "pattern_signature": row["pattern_signature"] or infer_pattern_signature(row, features),
        "required_packages": features["libraries"],
        "features": {key: value for key, value in features.items() if key != "libraries"},
        "local_data_files": [as_relative(path) for path in local_data_files],
        "reference_files": [as_relative(path) for path in reference_files],
        "external_dependencies": external_dependencies,
        "execution_notes": execution_notes,
    }


def build_index_row(manifest):
    return {
        "queue_position": manifest["queue_position"],
        "folder_name": manifest["folder_name"],
        "function_name": manifest["function_name"],
        "transcript_title": manifest["transcript_title"],
        "ker_status": manifest["ker_status"],
        "reproduction_status": manifest["reproduction_status"],
        "transcript_exists": "yes" if manifest["source_exists"]["transcript"] else "no",
        "code_exists": "yes" if manifest["source_exists"]["code"] else "no",
        "local_data_count": str(len(manifest["local_data_files"])),
        "external_dependency_count": str(len(manifest["external_dependencies"])),
        "required_packages": ", ".join(manifest["required_packages"]),
        "data_source": manifest["data_source"],
        "analysis_type": manifest["analysis_type"],
        "pattern_signature": manifest["pattern_signature"],
    }


def write_index(rows):
    OUTPUT_ROOT.mkdir(exist_ok=True)
    with INDEX_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=INDEX_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def write_readme(index_rows):
    ready_local = sum(1 for row in index_rows if row["reproduction_status"] == "ready_local")
    ready_external = sum(1 for row in index_rows if row["reproduction_status"] == "ready_with_external_steps")
    needs_external = sum(1 for row in index_rows if row["reproduction_status"] == "needs_external_sources")
    blocked = sum(1 for row in index_rows if row["reproduction_status"].startswith("blocked"))
    needs_review = sum(1 for row in index_rows if row["reproduction_status"] == "needs_data_review")

    preview_lines = []
    for row in index_rows[:10]:
        preview_lines.append(
            f"- `{row['queue_position']}` `{row['function_name']}` -> `{row['reproduction_status']}`"
        )

    text = f"""# Episode Output Folder

This folder is generated from `control_table.csv` in queue order so the project can reproduce episodes one by one from the top of the list.

## What is here

- `episodes/`: one folder per control-table row with a guide, extracted R script, and manifest
- `reproduction_index.csv`: flat queue summary for automation and review

## Current status counts

- `ready_local`: {ready_local}
- `ready_with_external_steps`: {ready_external}
- `needs_external_sources`: {needs_external}
- `needs_data_review`: {needs_review}
- `blocked_*`: {blocked}

## First episodes in queue

{chr(10).join(preview_lines)}
"""

    README_PATH.write_text(text, encoding="utf-8")


def process_rows(limit=None, force=False):
    rows = load_control_rows()
    EPISODES_ROOT.mkdir(parents=True, exist_ok=True)
    index_rows = []

    selected_rows = rows if limit is None else rows[:limit]
    width = max(3, len(str(len(selected_rows))))

    for i, row in enumerate(selected_rows, start=1):
        folder_name = f"{i:0{width}d}_{sanitize_slug(row['function_name'] or row['transcript_title'])}"
        episode_dir = EPISODES_ROOT / folder_name
        if force:
            episode_dir.mkdir(parents=True, exist_ok=True)
        else:
            episode_dir.mkdir(parents=True, exist_ok=True)

        transcript_text = read_text(row["transcript_file"])
        rmd_text = read_text(row["code_file"])
        features = detect_features(row, rmd_text) if rmd_text else {
            "ggplot": False,
            "joins": False,
            "reshape": False,
            "text_analysis": False,
            "modeling": False,
            "predictive": False,
            "scraping": False,
            "maps": False,
            "time": False,
            "simulation": False,
            "multi_table": False,
            "libraries": [],
        }

        local_data_files = find_local_data_files(rmd_text)
        reference_files = find_reference_files(local_data_files)
        external_dependencies = detect_external_dependencies(rmd_text, features, local_data_files)
        execution_notes = detect_execution_notes(rmd_text, local_data_files)
        chunks = extract_code_chunks(rmd_text)
        reproduction_status = infer_reproduction_status(
            row=row,
            transcript_text=transcript_text,
            rmd_text=rmd_text,
            local_data_files=local_data_files,
            external_dependencies=external_dependencies,
        )

        qmd_text = build_qmd_text(
            row=row,
            features=features,
            transcript_text=transcript_text,
            local_data_files=local_data_files,
            reference_files=reference_files,
            external_dependencies=external_dependencies,
            execution_notes=execution_notes,
            chunks=chunks,
            reproduction_status=reproduction_status,
        )

        manifest = build_manifest(
            row=row,
            features=features,
            transcript_text=transcript_text,
            rmd_text=rmd_text,
            local_data_files=local_data_files,
            reference_files=reference_files,
            external_dependencies=external_dependencies,
            execution_notes=execution_notes,
            reproduction_status=reproduction_status,
            folder_name=folder_name,
        )
        manifest["queue_position"] = i

        (episode_dir / "episode_guide.qmd").write_text(qmd_text, encoding="utf-8")
        (episode_dir / "episode_source.R").write_text(render_extracted_r_script(chunks), encoding="utf-8")
        (episode_dir / "episode_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        index_rows.append(build_index_row(manifest))

    write_index(index_rows)
    write_readme(index_rows)
    return index_rows


def main():
    parser = argparse.ArgumentParser(description="Build ordered per-episode output folders from control_table.csv")
    parser.add_argument("--limit", type=int, default=None, help="Optional number of episodes to process from the top of the queue")
    parser.add_argument("--force", action="store_true", help="Reserved for future overwrite logic; current build always refreshes files")
    args = parser.parse_args()

    index_rows = process_rows(limit=args.limit, force=args.force)
    print(f"Generated output folders: {len(index_rows)}")
    print(f"Wrote {INDEX_PATH.relative_to(ROOT).as_posix()}")
    print(f"Wrote {README_PATH.relative_to(ROOT).as_posix()}")
    if index_rows:
        print(f"First episode: {index_rows[0]['folder_name']}")
        print(f"Last episode: {index_rows[-1]['folder_name']}")


if __name__ == "__main__":
    main()
