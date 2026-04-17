import argparse
import json
import re
from pathlib import Path

from build_episode_outputs import EPISODES_ROOT, extract_tt_dates, sanitize_slug
from build_ker_entries import (
    ROOT,
    build_adaptation_plan,
    build_code_mapping_table,
    build_data_flow,
    build_function_candidates,
    build_reusable_patterns,
    build_thought_process_map,
    detect_features,
    load_control_rows,
    read_text,
    topic_from_title,
)


SUPER_ROOT = ROOT / "output" / "super_qmd"


def value_or_placeholder(value, placeholder):
    value = (value or "").strip()
    return value if value else placeholder


def parse_thought_steps(lines):
    steps = []
    for line in lines:
        parts = [part.strip() for part in line.split("|")]
        if len(parts) < 4:
            continue
        steps.append(
            {
                "id": parts[0],
                "type": parts[1],
                "description": parts[2],
                "trigger": parts[3],
            }
        )
    return steps


def queue_folder_name(rows, queue_position, row):
    width = max(3, len(str(len(rows))))
    slug = sanitize_slug(row["function_name"] or row["transcript_title"])
    return f"{queue_position:0{width}d}_{slug}"


def load_episode_manifest(rows, queue_position, row):
    folder_name = queue_folder_name(rows, queue_position, row)
    manifest_path = EPISODES_ROOT / folder_name / "episode_manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding="utf-8")), folder_name
    return None, folder_name


def transcript_preview(transcript_text, limit=520):
    compact = " ".join(transcript_text.split())
    if not compact:
        return "Transcript text was not available for this episode."
    if len(compact) <= limit:
        return compact
    return compact[:limit].rstrip() + "..."


def cognition_rules(row, features):
    rules = [
        "Start by naming the question and the unit of analysis before choosing plots or metrics.",
        "Use schema inspection to decide which table carries the main story and which tables are support tables.",
    ]

    if features["scraping"]:
        rules.append("Treat data collection as its own stage; assemble or scrape context first, then interpret.")
    if features["reshape"] or features["joins"]:
        rules.append("Build one analysis-ready table before comparing groups so the narrative rests on a stable grain.")
    if features["text_analysis"]:
        rules.append("Lock the grouping variable first, then tokenize text and compare language only after the corpus structure is clear.")
    if features["modeling"]:
        rules.append("Do descriptive work before modeling; the model should organize what the exploratory work already suggested.")
    if features["maps"]:
        rules.append("Aggregate to the geographic unit before drawing maps so the visual carries a clean analytical message.")
    if features["time"]:
        rules.append("Start broad with time or trend structure when it helps explain which later comparisons are fair.")

    rules.append("End with one communication-ready chart or table that carries the episode's main claim.")
    return rules


def stage_coaching(step_type, features):
    coaching = {
        "Context": "Define the analytical question, likely unit of analysis, and what would count as an interesting result.",
        "Inspect": "Inspect shape, columns, missingness, and table roles before committing to transformations.",
        "Hypothesis": "Write the likely comparison or tension you expect to see, but keep it provisional.",
        "Transform": "Reshape, join, or normalize only enough to make the next comparison possible.",
        "Compare": "Summarize groups or entities in a way that reveals differences, rankings, or trends without overfitting the story.",
        "Visualize": "Choose the plot after the summary table exists, then optimize for clarity rather than novelty.",
        "Reflect": "Translate the episode-specific move into a reusable function, helper, or workflow note.",
    }.get(step_type, "Use this step to turn cognition into a concrete analysis move.")

    extras = []
    if step_type == "Transform" and features["scraping"]:
        extras.append("Keep scraped or externally collected context separate from the main analysis table until keys are stable.")
    if step_type == "Compare" and features["text_analysis"]:
        extras.append("For text work, compare grouped term patterns only after you know what counts as a document and a group.")
    if step_type == "Compare" and features["modeling"]:
        extras.append("If you plan to model, use this step to identify which predictors deserve to enter the first baseline model.")
    if step_type == "Visualize" and features["time"]:
        extras.append("When time is present, lead with the broad trend before showing narrower subgroup comparisons.")

    return coaching, extras


def step_scaffold(step_type, row, manifest):
    topic = topic_from_title(row["transcript_title"])
    main_data_lines = manifest.get("local_data_files", []) if manifest else []
    data_preview = ", ".join(main_data_lines[:3]) if main_data_lines else "local episode data"

    scaffolds = {
        "Context": [
            "# Write the one-sentence analytical question for this episode.",
            f"# Topic: {topic}",
            "# Unit of analysis:",
            "# Main comparison axis:",
            "# What would make the result interesting?",
        ],
        "Inspect": [
            "# Start here once data is loaded.",
            "# names(tuesdata)",
            "# purrr::imap_dfr(tuesdata, ~ tibble(table = .y, rows = nrow(.x), cols = ncol(.x)))",
            "# glimpse(analysis_tbl)",
        ],
        "Hypothesis": [
            "# Sketch the first hypothesis before building complicated code.",
            "# Example:",
            "# - I expect ...",
            "# - Because ...",
            "# - I will check this with ...",
        ],
        "Transform": [
            "# Build the canonical analysis table for this episode.",
            f"# Source assets: {data_preview}",
            "# Suggested verbs: mutate(), separate_rows(), pivot_longer(), left_join(), unnest()",
            "# analysis_tbl <- raw_tbl %>%",
            "#   ..."
        ],
        "Compare": [
            "# Summarize the comparison that best answers the question.",
            "# comparison_tbl <- analysis_tbl %>%",
            "#   group_by(...) %>%",
            "#   summarise(...) %>%",
            "#   arrange(desc(...))",
        ],
        "Visualize": [
            "# Turn the comparison table into one clear communication plot.",
            "# ggplot(comparison_tbl, aes(...)) +",
            "#   geom_col() +",
            "#   labs(title = ..., subtitle = ...)",
        ],
        "Reflect": [
            "# Capture the reusable move after the analysis is clear.",
            "# Candidate helper:",
            "# - input:",
            "# - output:",
            "# - why it is reusable:",
        ],
    }

    return "\n".join(scaffolds.get(step_type, ["# TODO: turn this cognitive step into concrete analysis code."]))


def setup_chunk(row, manifest, rmd_text):
    packages = manifest.get("required_packages", []) if manifest else []
    tt_dates = extract_tt_dates(rmd_text)
    reproduction_status = manifest.get("reproduction_status", "") if manifest else ""
    lines = [
        "library(tidyverse)",
        'source("R/screencast_helpers.R")',
    ]

    optional_packages = [pkg for pkg in packages if pkg != "tidyverse"]
    if optional_packages:
        lines.append("")
        lines.append("# Optional episode packages:")
        for pkg in optional_packages:
            lines.append(f"# library({pkg})")

    if tt_dates:
        lines.extend(
            [
                "",
                f'tuesdata <- load_tidyweek_data("{tt_dates[0]}")',
                "names(tuesdata)",
            ]
        )
        assignments = re.findall(r"(\w+)\s*<-\s*tuesdata\$(\w+)", rmd_text)
        seen = set()
        for lhs, rhs in assignments[:6]:
            if lhs not in seen:
                lines.append(f"{lhs} <- tuesdata${rhs}")
                seen.add(lhs)
    else:
        local_files = manifest.get("local_data_files", []) if manifest else []
        if local_files:
            for rel_path in local_files[:3]:
                var_name = sanitize_slug(Path(rel_path).stem)
                lines.append(f'{var_name} <- readr::read_csv("{rel_path}", show_col_types = FALSE)')
        elif reproduction_status == "blocked_needs_mapping":
            lines.extend(
                [
                    "",
                    "# Episode mapping is incomplete, so the data scaffold cannot be generated yet.",
                    "# TODO: identify the correct source data and code file, then rebuild this super QMD.",
                ]
            )
        else:
            lines.extend(
                [
                    "",
                    "# TODO: load the episode data here.",
                    "# data <- readr::read_csv(...)",
                ]
            )

    return "\n".join(lines)


def render_super_qmd(row, queue_position, manifest, folder_name):
    transcript_text = read_text(row["transcript_file"])
    rmd_text = read_text(row["code_file"])
    features = detect_features(row, rmd_text)
    analysis_type = value_or_placeholder(row["analysis_type"], "Not resolved yet")
    pattern_signature = value_or_placeholder(row["pattern_signature"], "Not resolved yet")
    data_source = value_or_placeholder(row["data_source"], "Data source not resolved yet")
    analysis_intent = value_or_placeholder(
        row["analysis_intent"],
        "Analysis intent is not resolved yet. Use the transcript and code mapping step before filling in the narrative.",
    )
    thought_lines = build_thought_process_map(topic_from_title(row["transcript_title"]), features)
    thought_steps = parse_thought_steps(thought_lines)
    code_map = build_code_mapping_table(rmd_text, features)
    data_flow = build_data_flow(features)
    reusable_patterns = build_reusable_patterns(features)
    function_candidates = build_function_candidates(features)
    adaptation_plan = build_adaptation_plan(features)

    cognition_lines = "\n".join(f"- {line}" for line in cognition_rules(row, features))
    thought_block = "\n".join(f"- `{line}`" for line in thought_lines)
    code_block = "\n".join(f"- `{line}`" for line in code_map)
    flow_block = "\n".join(f"- `{line}`" for line in data_flow)
    pattern_block = "\n".join(f"- `{line}`" for line in reusable_patterns)
    function_block = "\n".join(f"- `{line}`" for line in function_candidates)
    adaptation_block = "\n".join(f"- `{line}`" for line in adaptation_plan)

    local_assets = manifest.get("local_data_files", []) if manifest else []
    local_asset_block = "\n".join(f"- `{asset}`" for asset in local_assets) or "- No local assets were captured yet."
    execution_notes = manifest.get("execution_notes", []) if manifest else []
    execution_block = "\n".join(f"- {note}" for note in execution_notes) or "- No execution notes were captured."
    external_dependencies = manifest.get("external_dependencies", []) if manifest else []
    external_block = "\n".join(f"- {note}" for note in external_dependencies) or "- No external dependencies were captured."

    reproduction_status = manifest.get("reproduction_status", "not generated") if manifest else "not generated"
    status_note = ""
    if reproduction_status == "blocked_needs_mapping":
        status_note = """::: {.callout-warning}
## Status Note
This episode is still blocked at the mapping stage. The super QMD is useful as a shell for cognition and planning, but it needs a confirmed transcript-to-code-to-data mapping before the setup scaffold can become runnable.
:::
"""
    elif reproduction_status == "needs_data_review":
        status_note = """::: {.callout-warning}
## Status Note
This episode has a tentative mapping but still needs a manual data review. Treat the current scaffold as a draft until the source data path is confirmed.
:::
"""
    elif reproduction_status == "needs_external_sources":
        status_note = """::: {.callout-important}
## Status Note
This episode currently depends on external data retrieval. The cognitive structure is ready, but the execution path still needs remote source handling before it becomes locally reproducible.
:::
"""

    stages = []
    for index, step in enumerate(thought_steps, start=1):
        coaching, extras = stage_coaching(step["type"], features)
        extra_text = ""
        if extras:
            extra_text = "Additional guidance:\n\n" + "\n".join(f"- {item}" for item in extras)

        stage_section = f"""## Stage {index}: {step["type"]}

{step["description"]}

::: {{.callout-note}}
## Cognitive Move
{coaching}

Trigger:

- {step["trigger"]}

{extra_text}
:::

```{{r}}
#| label: stage_{index:02d}_{step["type"].lower()}
#| eval: false

{step_scaffold(step["type"], row, manifest)}
```
"""
        stages.append(stage_section.rstrip())

    title = row["transcript_title"]
    function_name = row["function_name"] or sanitize_slug(title)
    transcript_text_preview = transcript_preview(transcript_text)
    guide_path = f"output/episodes/{folder_name}/episode_guide.qmd"

    return f"""---
title: "Super QMD: {title}"
subtitle: "Cognition-first blueprint built from the episode guide and KER"
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

- the reproduction artifact in `{guide_path}`
- the KER entry for `{function_name}`
- a final guided analysis document like `bechdel_ker_guided_analysis.qmd`

The point is to preserve not only the code path, but the author's cognition:

- what question gets asked first
- how the dataset is inspected
- when transformation happens
- why one comparison is chosen before another
- which pieces should become reusable helpers

## Episode Snapshot

- `queue_position`: `{queue_position}`
- `function_name`: `{function_name}`
- `analysis_type`: `{analysis_type}`
- `pattern_signature`: `{pattern_signature}`
- `data_source`: {data_source}
- `reproduction_status`: `{reproduction_status}`

::: {{.callout-note}}
## Analysis Intent
{analysis_intent}
:::

{status_note}

## Transcript Preview

{transcript_text_preview}

## Cognitive Signature

{cognition_lines}

## Data and Execution Context

### Local Assets

{local_asset_block}

### Execution Notes

{execution_block}

### External Dependencies

{external_block}

## Setup Scaffold

```{{r}}
#| label: setup
#| eval: false

{setup_chunk(row, manifest or {{}}, rmd_text)}
```

## Thought -> Code -> Data Bridge

### Thought Process Map

{thought_block}

### Code Mapping Table

{code_block}

### Data Transformation Flow

{flow_block}

## Guided Build Sequence

{chr(10).join(stages)}

## Reusable Layer

### Reusable Patterns

{pattern_block}

### Function Candidates

{function_block}

## How To Finish This Super QMD

1. Replace each scaffold chunk with the real episode-specific analysis code.
2. After each major result, add a short callout explaining what changed in your thinking.
3. Keep one broad chart early, one comparison chart in the middle, and one final communication chart at the end.
4. Move any repeated transformation or comparison logic into `R/screencast_helpers.R`.
5. Once the document reads like a guided walkthrough instead of a reproduction note, promote it into a finished KER-guided analysis.

## Adaptation Layer

{adaptation_block}
"""


def resolve_row(rows, queue_position=None, function_name=None):
    if queue_position is not None:
        if queue_position < 1 or queue_position > len(rows):
            raise ValueError(f"queue_position must be between 1 and {len(rows)}")
        return queue_position, rows[queue_position - 1]

    if function_name:
        for index, row in enumerate(rows, start=1):
            if row["function_name"] == function_name:
                return index, row
        raise ValueError(f"Could not find function_name: {function_name}")

    return 1, rows[0]


def write_super_qmd(rows, queue_position, row):
    manifest, folder_name = load_episode_manifest(rows, queue_position, row)
    output_path = SUPER_ROOT / f"{folder_name}_super.qmd"
    output_path.write_text(render_super_qmd(row, queue_position, manifest, folder_name), encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Build a cognition-first super QMD from KER and episode metadata.")
    parser.add_argument("--queue-position", type=int, default=None, help="Control-table row number to build")
    parser.add_argument("--function-name", type=str, default=None, help="Function name to build")
    parser.add_argument("--all", action="store_true", help="Build super QMD files for every control-table row")
    args = parser.parse_args()

    rows = load_control_rows()
    SUPER_ROOT.mkdir(parents=True, exist_ok=True)

    if args.all:
        output_paths = []
        for queue_position, row in enumerate(rows, start=1):
            output_paths.append(write_super_qmd(rows, queue_position, row))

        print(f"Wrote {len(output_paths)} super QMD files")
        print(f"First file: {output_paths[0].relative_to(ROOT).as_posix()}")
        print(f"Last file: {output_paths[-1].relative_to(ROOT).as_posix()}")
        return

    queue_position, row = resolve_row(rows, queue_position=args.queue_position, function_name=args.function_name)
    output_path = write_super_qmd(rows, queue_position, row)

    print(f"Wrote {output_path.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
