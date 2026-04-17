import csv
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTROL_TABLE_PATH = ROOT / "control_table.csv"
KER_PATH = ROOT / "knowledge register.md"

CONTROL_COLUMNS = [
    "transcript_title",
    "transcript_file",
    "code_file",
    "function_name",
    "data_source",
    "analysis_intent",
    "analysis_type",
    "pattern_signature",
    "adaptation_hint",
    "ker_status",
    "notes",
]


def read_text(relative_path):
    if not relative_path:
        return ""

    path = ROOT / relative_path
    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8", errors="ignore")


def load_control_rows():
    with CONTROL_TABLE_PATH.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            normalized = {column: row.get(column, "").strip() for column in CONTROL_COLUMNS}
            rows.append(normalized)
        return rows


def write_control_rows(rows):
    with CONTROL_TABLE_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CONTROL_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def topic_from_title(title):
    topic = title.strip()
    topic = re.sub(r"^Analyz(?:ing|ng)\s+", "", topic, flags=re.IGNORECASE)
    topic = re.sub(r"^(and\s+)?predict(?:ing|ive)\s+", "", topic, flags=re.IGNORECASE)
    topic = re.sub(r"\s+(in|with)\s+R$", "", topic, flags=re.IGNORECASE)
    topic = re.sub(r"\s+data$", "", topic, flags=re.IGNORECASE)
    return topic.strip()


def find_library_names(rmd_text):
    return sorted(set(re.findall(r"library\(([^)]+)\)", rmd_text)))


def has_pattern(text, pattern):
    return re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) is not None


def detect_features(row, rmd_text):
    title_lower = row["transcript_title"].lower()

    features = {
        "ggplot": has_pattern(rmd_text, r"\bggplot\("),
        "joins": has_pattern(rmd_text, r"\b(left_join|inner_join|right_join|full_join|semi_join|anti_join)\("),
        "reshape": has_pattern(rmd_text, r"\b(pivot_longer|pivot_wider|gather|spread|separate_rows|unnest)\("),
        "text_analysis": has_pattern(rmd_text, r"\b(unnest_tokens|bind_tf_idf|bind_log_odds|stop_words|tidytext)\b"),
        "modeling": has_pattern(
            rmd_text,
            r"\b(glm\(|lm\(|tidymodels|parsnip|recipe\(|fit\(|predict\(|cv_glmnet|cv\.glmnet|boost_tree|rand_forest|survfit|Surv\()",
        ),
        "predictive": "predict" in title_lower
        or has_pattern(rmd_text, r"\b(vfold_cv|tune_grid|boost_tree|rand_forest|predict\(|cv_glmnet|cv\.glmnet)\b"),
        "scraping": has_pattern(rmd_text, r"\b(read_html|rvest|html_nodes|html_elements|jsonlite|fromJSON|GET\()\b"),
        "maps": has_pattern(rmd_text, r"\b(geom_sf|coord_sf|map_data\(|library\(sf\)|leaflet\(|maps::)\b"),
        "time": has_pattern(rmd_text, r"\b(year|month|date|lubridate|ymd\(|mdy\(|geom_line\(|scale_x_date|floor_date)\b"),
        "simulation": has_pattern(rmd_text, r"\b(simulate|crossing\(|sample_|reroll|trial)\b")
        or "riddler" in row["code_file"].lower(),
        "multi_table": has_pattern(rmd_text, r"\btt\$\w+") and len(set(re.findall(r"tt\$(\w+)", rmd_text))) > 1,
    }

    features["libraries"] = find_library_names(rmd_text)
    return features


def extract_data_source(row, rmd_text):
    tt_loads = sorted(set(re.findall(r'tt_load\(["\']([^"\']+)["\']\)', rmd_text)))
    if tt_loads:
        if len(tt_loads) == 1:
            return f"TidyTuesday {tt_loads[0]} dataset"
        return "TidyTuesday datasets: " + ", ".join(tt_loads)

    github_dates = sorted(
        set(re.findall(r"rfordatascience/tidytuesday/master/data/\d{4}/(\d{4}-\d{2}-\d{2})/", rmd_text))
    )
    if github_dates:
        if len(github_dates) == 1:
            return f"TidyTuesday {github_dates[0]} source files"
        return "TidyTuesday source files: " + ", ".join(github_dates)

    local_reads = sorted(
        set(
            re.findall(
                r'(?:read_csv|read_tsv|read_delim|read_excel|read_rds|vroom|st_read)\(["\']([^"\']+)["\']',
                rmd_text,
            )
        )
    )
    if local_reads:
        preview = ", ".join(local_reads[:4])
        if len(local_reads) > 4:
            preview += ", ..."
        return f"Local source files read in episode: {preview}"

    urls = sorted(set(re.findall(r'https?://[^\'")\s]+', rmd_text)))
    if urls:
        preview = ", ".join(urls[:2])
        if len(urls) > 2:
            preview += ", ..."
        return f"External sources used in episode: {preview}"

    return f"Dataset inferred from {Path(row['code_file']).name}" if row["code_file"] else ""


def infer_analysis_type(row, features):
    title_lower = row["transcript_title"].lower()
    data_source_lower = row["data_source"].lower()

    if features["predictive"]:
        return "Predictive"
    if features["modeling"]:
        return "Modeling"
    if "scrap" in title_lower:
        return "Scraping"
    if features["scraping"] and "tidytuesday" not in data_source_lower:
        return "Scraping"
    if features["scraping"] and not features["ggplot"] and not features["modeling"]:
        return "Scraping"
    if features["reshape"] and not features["ggplot"] and not features["text_analysis"]:
        return "Data Cleaning"
    return "EDA"


def infer_analysis_intent(row, features):
    topic = topic_from_title(row["transcript_title"])
    analysis_type = infer_analysis_type(row, features)

    if features["predictive"]:
        return (
            f"Predict or estimate outcomes in {topic} using cleaned features, exploratory analysis, "
            "and model evaluation"
        )
    if features["text_analysis"]:
        return (
            f"Explore and compare language patterns in {topic} using tokenization, grouped counts, "
            "and discriminative text analysis"
        )
    if analysis_type == "Scraping":
        return f"Collect, clean, and explore {topic} data from external web sources"
    if features["maps"] and features["time"]:
        return f"Explore geographic and temporal variation in {topic} through joins, summarization, and mapping"
    if features["maps"]:
        return f"Explore geographic variation in {topic} through joins, summarization, and visualization"
    if features["modeling"]:
        return f"Explore, explain, and model patterns in {topic} using engineered features and comparative summaries"
    return f"Explore distributions, group differences, and notable patterns in {topic} through cleaning, summarization, and visualization"


def unique_in_order(values):
    seen = set()
    ordered = []
    for value in values:
        if value and value not in seen:
            ordered.append(value)
            seen.add(value)
    return ordered


def infer_pattern_signature(row, features):
    parts = ["load", "inspect"]
    if features["scraping"]:
        parts.append("scrape")
    if features["reshape"]:
        parts.append("reshape")
    if features["joins"]:
        parts.append("join")
    if features["text_analysis"]:
        parts.append("tokenize")
    if features["maps"]:
        parts.append("map")
    if features["time"]:
        parts.append("trend")
    if features["simulation"]:
        parts.append("simulate")
    if features["modeling"]:
        parts.extend(["model", "evaluate"])
    else:
        parts.append("compare")
    if features["ggplot"]:
        parts.append("visualize")

    return "_".join(unique_in_order(parts))


def infer_adaptation_hint(row, features):
    if features["predictive"]:
        return "Reuse for tabular datasets with a clear outcome column, engineered features, and model evaluation needs"
    if features["text_analysis"]:
        return "Reuse for grouped text corpora that need tokenization, term comparison, and context-aware vocabulary analysis"
    if features["modeling"]:
        return "Reuse for structured datasets where descriptive analysis leads into explanatory or predictive models"
    if features["scraping"] and features["maps"]:
        return "Reuse for web-sourced reference tables that need cleaning, joining, and geographic display"
    if features["scraping"]:
        return "Reuse for datasets that must be assembled from HTML or JSON sources before analysis"
    if features["maps"] and features["time"]:
        return "Reuse for geographic datasets with region codes, time fields, and map-ready joins"
    if features["maps"]:
        return "Reuse for datasets with spatial identifiers that benefit from region-level aggregation and mapping"
    if features["reshape"] and features["joins"]:
        return "Reuse for messy multi-table datasets that need reshaping, enrichment, and grouped summaries before plotting"
    return "Reuse for exploratory datasets that need schema inspection, grouped summaries, and visualization-first storytelling"


def infer_complexity(features):
    score = 1
    for key in ("reshape", "joins", "text_analysis", "maps", "modeling", "scraping", "multi_table", "simulation"):
        if features.get(key):
            score += 1

    if score >= 6:
        return "high", 5
    if score >= 4:
        return "medium-high", 4
    if score >= 3:
        return "medium", 3
    return "low-medium", 2


def present_functions(rmd_text, candidates):
    found = [candidate for candidate in candidates if has_pattern(rmd_text, re.escape(candidate))]
    return ", ".join(found[:5]) if found else "episode-specific dplyr and ggplot verbs"


def build_thought_process_map(topic, features):
    steps = [
        "T1 | Context | Frame the episode as exploratory analysis of "
        + topic
        + " with limited advance knowledge of the data. | Transcript title and opening context",
        "T2 | Inspect | Load the data, inspect table shape, and identify the main entities, measures, and comparison axes. | Initial data load and early counts or prints",
    ]

    if features["scraping"]:
        steps.append(
            "T3 | Transform | Acquire or supplement source data from external web pages or APIs before analysis. | Presence of scraping or external-source code"
        )

    if features["reshape"] or features["joins"]:
        steps.append(
            "T4 | Transform | Reshape fields, standardize column meanings, and join supporting tables to create analysis-ready records. | Join and reshaping operations in the Rmd"
        )

    if features["text_analysis"]:
        steps.append(
            "T5 | Compare | Tokenize text, remove noise terms, and compare vocabulary across groups or documents. | tidytext workflow in the episode"
        )

    if features["modeling"]:
        steps.append(
            "T6 | Compare | Move from descriptive patterns into statistical or predictive modeling once the feature space is ready. | Modeling functions and evaluation code"
        )
    else:
        steps.append(
            "T6 | Compare | Summarize group differences, rates, rankings, or trajectories to surface the main story in the data. | Grouped summaries and comparative plots"
        )

    if features["maps"]:
        steps.append(
            "T7 | Visualize | Translate the analytical result into geographic views to reveal regional variation and outliers. | Spatial joins or mapping code"
        )
    else:
        steps.append(
            "T7 | Visualize | Turn the cleaned summaries into interpretable visual comparisons and iterate toward the clearest view. | ggplot workflow"
        )

    steps.append(
        "T8 | Reflect | Identify reusable workflow pieces that can transfer to future datasets with a similar shape or question. | End-state of the analysis pattern"
    )

    return steps


def build_code_mapping_table(rmd_text, features):
    lines = [
        "T1 | Data load and inspection | "
        + present_functions(rmd_text, ["tt_load", "read_csv", "read_excel", "read_html", "count", "glimpse"])
        + " | Establish source shape, units, and comparison candidates"
    ]

    if features["scraping"]:
        lines.append(
            "T3 | External acquisition | "
            + present_functions(rmd_text, ["read_html", "html_nodes", "html_elements", "fromJSON", "GET"])
            + " | Build or enrich the dataset before analysis"
        )

    if features["reshape"] or features["joins"]:
        lines.append(
            "T4 | Structuring and enrichment | "
            + present_functions(
                rmd_text,
                [
                    "pivot_longer",
                    "pivot_wider",
                    "gather",
                    "spread",
                    "separate_rows",
                    "unnest",
                    "left_join",
                    "inner_join",
                ],
            )
            + " | Convert messy inputs into analysis-ready tables"
        )

    if features["text_analysis"]:
        lines.append(
            "T5 | Text comparison | "
            + present_functions(rmd_text, ["unnest_tokens", "anti_join", "bind_tf_idf", "bind_log_odds"])
            + " | Identify terms that distinguish groups or documents"
        )

    if features["modeling"]:
        lines.append(
            "T6 | Modeling and evaluation | "
            + present_functions(rmd_text, ["lm", "glm", "recipe", "fit", "predict", "vfold_cv", "tune_grid", "survfit"])
            + " | Test explanatory or predictive relationships after EDA"
        )
    else:
        lines.append(
            "T6 | Group comparison | "
            + present_functions(rmd_text, ["group_by", "summarize", "count", "mutate"])
            + " | Compare categories, time periods, or entities"
        )

    lines.append(
        "T7 | Visualization | "
        + present_functions(rmd_text, ["ggplot", "geom_col", "geom_point", "geom_line", "geom_sf", "facet_wrap"])
        + " | Communicate the core result visually"
    )

    return lines


def build_data_flow(features):
    flow = [
        "Raw | Imported source tables or files | Load source data into tibbles or lists | Raw episode objects | Establish the starting analysis surface"
    ]

    if features["scraping"]:
        flow.append(
            "Raw -> Collected | External web or JSON sources | Scrape or request supplemental records | Collected reference tables | Fill gaps not available in the initial source"
        )

    if features["reshape"] or features["joins"]:
        flow.append(
            "Raw -> Clean | Raw source tables | Rename, reshape, unnest, and join supporting data | Analysis-ready rows with consistent keys | Standardize the schema before comparison"
        )
    else:
        flow.append(
            "Raw -> Clean | Raw source tables | Filter, rename, and derive analysis columns | Cleaned table | Make the data comparable and plot-ready"
        )

    if features["text_analysis"]:
        flow.append(
            "Clean -> Analytical | Clean text corpus | Tokenize text, remove stop words, and count terms by group | Term-frequency comparison tables | Surface language differences and signatures"
        )
    elif features["modeling"]:
        flow.append(
            "Clean -> Analytical | Feature table | Engineer predictors and fit models | Model outputs, predictions, or coefficients | Quantify relationships beyond descriptive summaries"
        )
    else:
        flow.append(
            "Clean -> Analytical | Cleaned table | Group, summarize, rank, or compare entities | Summary tables or rate calculations | Surface the core analytical story"
        )

    if features["maps"]:
        flow.append(
            "Analytical -> Visual | Analytical summaries with geographic identifiers | Join map geometry or region lookup data | Map-ready plotting table | Display geographic variation"
        )
    else:
        flow.append(
            "Analytical -> Visual | Summary or model outputs | Reorder factors and prepare plotting fields | Plot-ready table | Turn the analytical result into an interpretable chart"
        )

    return flow


def build_reusable_patterns(features):
    patterns = ["inspect_source_schema | Inspect source tables, field meanings, and likely comparison axes | Raw dataset or dataset list | Initial analysis plan | Y"]

    if features["scraping"]:
        patterns.append(
            "scrape_supporting_reference_data | Pull structured records from HTML or JSON before analysis | External source url and parsing rules | Supplemental reference table | Y"
        )
    if features["reshape"]:
        patterns.append(
            "reshape_analysis_inputs | Convert wide or nested source fields into normalized long-form records | Raw tabular fields | Tidy analysis table | Y"
        )
    if features["joins"]:
        patterns.append(
            "join_context_tables | Enrich the main table with lookup or metadata tables | Primary data plus keys | Context-enriched analysis table | Y"
        )
    if features["text_analysis"]:
        patterns.append(
            "compare_group_vocabulary | Tokenize text and compute grouped term distinctiveness | Text, grouping variable, document or entity ids | Ranked term comparison tables | Y"
        )
    if features["modeling"]:
        patterns.append(
            "build_predictive_or_explanatory_model | Move from cleaned features to fitted models and evaluation outputs | Feature table and outcome field | Model object and diagnostics | Y"
        )
    if features["maps"]:
        patterns.append(
            "prepare_geographic_summary | Aggregate metrics by region and join map geometry or lookup tables | Regional metrics and identifiers | Map-ready data | Y"
        )

    patterns.append(
        "plot_comparative_story | Reorder entities and visualize the main comparison cleanly | Summary table or model output | Communication-ready plot | Y"
    )
    return patterns


def build_function_candidates(features):
    candidates = []

    if features["scraping"]:
        candidates.extend(
            [
                "scrape_reference_table(url, css_selector)",
                "collect_episode_source_records(urls, parser)",
            ]
        )
    if features["reshape"] or features["joins"]:
        candidates.extend(
            [
                "reshape_episode_inputs(data, ...)",
                "join_episode_context(primary_data, lookup_data, by)",
            ]
        )
    if features["text_analysis"]:
        candidates.extend(
            [
                "prepare_text_tokens(data, text_column)",
                "compare_group_vocabulary(data, group_col, term_col, count_col = 'n')",
            ]
        )
    if features["modeling"]:
        candidates.extend(
            [
                "build_predictive_pipeline(data, formula, ...)",
                "evaluate_episode_model(model, test_data, outcome_col)",
            ]
        )
    if features["maps"]:
        candidates.extend(
            [
                "prepare_map_summary(data, region_col, value_col)",
                "plot_geographic_metric(map_data, value_col)",
            ]
        )

    candidates.append("plot_comparative_story(data, x_col, y_col, group_col = NULL)")
    return unique_in_order(candidates)


def primary_techniques(features):
    techniques = ["schema inspection", "grouped summaries"]
    if features["scraping"]:
        techniques.append("web or API data collection")
    if features["reshape"]:
        techniques.append("reshaping")
    if features["joins"]:
        techniques.append("table joins")
    if features["text_analysis"]:
        techniques.extend(["tokenization", "term comparison"])
    if features["maps"]:
        techniques.append("mapping")
    if features["modeling"]:
        techniques.append("modeling")
    if features["time"]:
        techniques.append("time-aware comparison")
    techniques.append("visualization")
    return unique_in_order(techniques)


def build_adaptation_plan(features):
    plan = [
        "1 | inspect_source_schema | Start by mapping entities, measures, and likely comparison axes before transforming anything"
    ]

    if features["scraping"]:
        plan.append(
            "2 | scrape_supporting_reference_data | Rebuild any missing lookup or metadata tables from the relevant external source"
        )
    if features["reshape"]:
        plan.append(
            "3 | reshape_analysis_inputs | Normalize wide, nested, or repeated fields into one analysis-ready row structure"
        )
    if features["joins"]:
        plan.append(
            "4 | join_context_tables | Enrich the main analysis table with keys, metadata, or auxiliary measurements"
        )
    if features["text_analysis"]:
        plan.append(
            "5 | compare_group_vocabulary | Tokenize the new corpus and compare terms across groups or documents"
        )
    if features["modeling"]:
        plan.append(
            "6 | build_predictive_or_explanatory_model | Fit and evaluate a baseline model after the core feature engineering is stable"
        )
    if features["maps"]:
        plan.append(
            "7 | prepare_geographic_summary | Aggregate to the geographic unit available in the new dataset and rebuild the map join"
        )

    plan.append(
        "8 | plot_comparative_story | Choose the clearest visual comparison once the analytical table is ready"
    )
    return plan


def build_ker_entry(row, features):
    topic = topic_from_title(row["transcript_title"])
    complexity_label, difficulty_score = infer_complexity(features)
    techniques = ", ".join(primary_techniques(features))

    metadata_lines = [
        f"### `{row['function_name']}`",
        "",
        f"- `transcript_title`: {row['transcript_title']}",
        f"- `transcript_file`: `{row['transcript_file']}`",
        f"- `code_file`: `{row['code_file']}`",
        f"- `data_source`: {row['data_source']}",
        f"- `analysis_intent`: {row['analysis_intent']}",
        f"- `analysis_type`: {row['analysis_type']}",
        f"- `pattern_signature`: `{row['pattern_signature']}`",
        f"- `adaptation_hint`: {row['adaptation_hint']}",
        f"- `ker_status`: {row['ker_status']}",
        "",
        "Thought Process Map:",
        "",
    ]

    thought_lines = [f"- `{line}`" for line in build_thought_process_map(topic, features)]
    code_lines = ["", "Code Mapping Table:", ""] + [f"- `{line}`" for line in build_code_mapping_table(read_text(row["code_file"]), features)]
    flow_lines = ["", "Data Transformation Flow:", ""] + [f"- `{line}`" for line in build_data_flow(features)]
    pattern_lines = ["", "Reusable Patterns:", ""] + [f"- `{line}`" for line in build_reusable_patterns(features)]
    function_lines = ["", "Function Candidates:", ""] + [f"- `{candidate}`" for candidate in build_function_candidates(features)]
    signature_lines = [
        "",
        "Episode Signature:",
        "",
        f"- `analysis_intent`: {row['analysis_intent']}",
        f"- `analysis_type`: {row['analysis_type']}",
        f"- `primary_techniques`: {techniques}",
        f"- `data_complexity_level`: {complexity_label}",
        f"- `reusable_difficulty_score`: {difficulty_score}",
    ]
    adaptation_lines = ["", "Adaptation Plan:", ""] + [f"- `{line}`" for line in build_adaptation_plan(features)]

    return "\n".join(
        metadata_lines
        + thought_lines
        + code_lines
        + flow_lines
        + pattern_lines
        + function_lines
        + signature_lines
        + adaptation_lines
        + [""]
    )


def render_extracted_section(rows):
    extracted_rows = [row for row in rows if row["ker_status"] == "extracted"]
    if not extracted_rows:
        return "## Extracted episodes\n\nNo extracted episodes have been generated yet.\n\n"

    parts = ["## Extracted episodes", ""]
    for row in extracted_rows:
        rmd_text = read_text(row["code_file"])
        features = detect_features(row, rmd_text)
        parts.append(build_ker_entry(row, features))
    return "\n".join(parts).rstrip() + "\n\n"


def update_ker_document(extracted_section):
    text = KER_PATH.read_text(encoding="utf-8")
    reviewed_header = "## Reviewed episodes"
    extracted_header = "## Extracted episodes"

    reviewed_index = text.find(reviewed_header)
    if reviewed_index == -1:
        raise RuntimeError("Could not find '## Reviewed episodes' in knowledge register.md")

    extracted_index = text.find(extracted_header)
    if extracted_index == -1:
        new_text = text[:reviewed_index] + extracted_section + text[reviewed_index:]
    else:
        new_text = text[:extracted_index] + extracted_section + text[reviewed_index:]

    KER_PATH.write_text(new_text, encoding="utf-8")


def enrich_rows(rows):
    extracted_count = 0
    for row in rows:
        if row["ker_status"] in {"reviewed", "needs_mapping"}:
            continue
        if not row["code_file"]:
            continue

        rmd_text = read_text(row["code_file"])
        features = detect_features(row, rmd_text)

        row["data_source"] = extract_data_source(row, rmd_text)
        row["analysis_type"] = infer_analysis_type(row, features)
        row["analysis_intent"] = infer_analysis_intent(row, features)
        row["pattern_signature"] = infer_pattern_signature(row, features)
        row["adaptation_hint"] = infer_adaptation_hint(row, features)
        row["ker_status"] = "extracted"
        extracted_count += 1

    return extracted_count


def main():
    rows = load_control_rows()
    extracted_count = enrich_rows(rows)
    write_control_rows(rows)
    extracted_section = render_extracted_section(rows)
    update_ker_document(extracted_section)

    reviewed_count = sum(1 for row in rows if row["ker_status"] == "reviewed")
    extracted_total = sum(1 for row in rows if row["ker_status"] == "extracted")
    needs_mapping_count = sum(1 for row in rows if row["ker_status"] == "needs_mapping")

    print(f"Updated control table rows to extracted: {extracted_count}")
    print(f"Reviewed rows preserved: {reviewed_count}")
    print(f"Extracted rows now in queue: {extracted_total}")
    print(f"Needs mapping rows: {needs_mapping_count}")
    print(f"Updated {KER_PATH.name}")


if __name__ == "__main__":
    main()
