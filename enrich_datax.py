"""
enrich_datax.py — Add TheDataShrink™ concept fields to every episode manifest.

Fields added:
  - fails_when      : conditions where this pattern BREAKS
  - works_when      : conditions where this pattern EXCELS
  - atomic_concepts : list of atomic reusable concepts this episode demonstrates

Also adds the 3-hour architecture stub to every manifest:
  - h1_eda_status
  - h2_modeling_status
  - h3_communicate_status

These fields are inferred from existing manifest data (features, pattern_signature,
analysis_type) so the marathon can start with pre-filled stubs that get refined.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EPISODES_ROOT = ROOT / "output" / "episodes"

# --- Atomic concept catalogue ---
# TheDataShrink™ concept library — derived from pattern_signatures across all episodes.
# Each concept is a reusable node that transcends any single episode.
CONCEPT_CATALOGUE = {
    # Text analysis concepts
    "tf_idf_comparison": {
        "label": "TF-IDF group comparison",
        "works_when": ["multiple groups with text documents", "want to find distinctive vocabulary per group"],
        "fails_when": ["corpus is tiny (<100 docs)", "groups are very unequal in size without normalisation"],
    },
    "log_odds_ratio": {
        "label": "Log-odds ratio for group text",
        "works_when": ["two groups with token counts", "want statistically grounded vocabulary contrast"],
        "fails_when": ["groups are not mutually exclusive", "token counts are near-zero (Jeffreys prior needed)"],
    },
    "tokenization_pipeline": {
        "label": "Tidytext tokenization pipeline",
        "works_when": ["raw text column", "want word-level analysis"],
        "fails_when": ["text is highly structured (JSON, code)", "language is non-English without custom stopwords"],
    },
    # Modeling concepts
    "lasso_sparse_features": {
        "label": "LASSO for sparse feature selection",
        "works_when": ["many engineered/dummy features", "want automatic feature selection"],
        "fails_when": ["features are highly correlated without grouping", "outcome is non-linear"],
    },
    "cross_validation_tidymodels": {
        "label": "Cross-validation with tidymodels v-fold",
        "works_when": ["tabular data, clear outcome column", "comparing multiple model specs"],
        "fails_when": ["time series data without blocking", "very small datasets (<200 rows)"],
    },
    "survival_kaplan_meier": {
        "label": "Kaplan-Meier survival analysis",
        "works_when": ["time-to-event outcome with censoring"],
        "fails_when": ["no censoring indicator", "competing risks without adjustment"],
    },
    # EDA concepts
    "grouped_summary_ggplot": {
        "label": "Grouped summary → ggplot storytelling",
        "works_when": ["categorical grouping variable", "want to compare distributions or means across groups"],
        "fails_when": ["too many groups (>15) without faceting", "data is wide format without pivoting"],
    },
    "time_series_trend": {
        "label": "Time series trend visualisation",
        "works_when": ["date/year column", "want to show change over time"],
        "fails_when": ["irregular time intervals without aggregation", "missing time points without imputation"],
    },
    "geospatial_choropleth": {
        "label": "Choropleth map with sf/ggplot",
        "works_when": ["region or country column matchable to a shapefile"],
        "fails_when": ["data is at sub-region level without matching geometry", "CRS mismatch"],
    },
    "web_scraping_rvest": {
        "label": "HTML scraping with rvest to build reference table",
        "works_when": ["stable HTML table at a known URL", "need supplemental context not in TidyTuesday file"],
        "fails_when": ["JS-rendered content (needs Selenium/Playwright)", "rate-limited or auth-gated URLs"],
    },
    "multi_table_join": {
        "label": "Multi-table join and grain alignment",
        "works_when": ["multiple TidyTuesday files with a shared key"],
        "fails_when": ["keys are dirty (case mismatch, trailing spaces) without normalisation"],
    },
    "pivot_reshape": {
        "label": "pivot_longer / pivot_wider reshape",
        "works_when": ["wide format with repeated column suffixes"],
        "fails_when": ["columns have inconsistent naming patterns", "values need type coercion first"],
    },
    "animated_transition": {
        "label": "gganimate / transition_time animation",
        "works_when": ["strong time dimension", "story benefits from showing change in motion"],
        "fails_when": ["static report context", "too many categories causing visual clutter"],
    },
    "topic_modelling_lda": {
        "label": "LDA / STM topic modelling",
        "works_when": ["large corpus of documents", "want to discover latent themes"],
        "fails_when": ["corpus is small (<500 docs)", "documents are very short (<50 words)"],
    },
    "bootstrap_confidence": {
        "label": "Bootstrap confidence intervals (rsample)",
        "works_when": ["want distribution-free uncertainty estimates"],
        "fails_when": ["data is time-dependent (need block bootstrap)", "n < 30"],
    },
}

# Pattern signature → concept mapping
PATTERN_TO_CONCEPTS = {
    "tokenize": ["tokenization_pipeline"],
    "tf_idf": ["tf_idf_comparison", "tokenization_pipeline"],
    "log_odds": ["log_odds_ratio", "tokenization_pipeline"],
    "model": ["cross_validation_tidymodels"],
    "lasso": ["lasso_sparse_features", "cross_validation_tidymodels"],
    "glmnet": ["lasso_sparse_features"],
    "survival": ["survival_kaplan_meier"],
    "map": ["geospatial_choropleth"],
    "scrape": ["web_scraping_rvest"],
    "join": ["multi_table_join"],
    "reshape": ["pivot_reshape"],
    "trend": ["time_series_trend"],
    "compare": ["grouped_summary_ggplot"],
    "visualize": ["grouped_summary_ggplot"],
    "animate": ["animated_transition"],
    "topic": ["topic_modelling_lda"],
    "simulate": ["bootstrap_confidence"],
    "stm": ["topic_modelling_lda"],
}


def infer_atomic_concepts(manifest: dict) -> list[str]:
    sig = manifest.get("pattern_signature", "").lower()
    features = manifest.get("features", {})
    concepts = set()

    for keyword, concept_keys in PATTERN_TO_CONCEPTS.items():
        if keyword in sig:
            concepts.update(concept_keys)

    # Feature-based overrides
    if features.get("text_analysis"):
        concepts.add("tokenization_pipeline")
    if features.get("maps"):
        concepts.add("geospatial_choropleth")
    if features.get("scraping"):
        concepts.add("web_scraping_rvest")
    if features.get("joins"):
        concepts.add("multi_table_join")
    if features.get("reshape"):
        concepts.add("pivot_reshape")
    if features.get("time"):
        concepts.add("time_series_trend")
    if features.get("modeling"):
        concepts.add("cross_validation_tidymodels")
    if features.get("simulation"):
        concepts.add("bootstrap_confidence")

    return sorted(concepts)


def infer_fails_when(manifest: dict) -> list[str]:
    atype = manifest.get("analysis_type", "")
    sig = manifest.get("pattern_signature", "").lower()
    fails = []

    if atype == "EDA":
        fails.append("dataset has no natural grouping variable — comparisons become meaningless")
        fails.append("column names are unstable across TidyTuesday editions (re-check schema each year)")
    if atype in ("Predictive", "Modeling"):
        fails.append("outcome column is missing or near-zero variance")
        fails.append("training set is too small for the number of predictors")
    if "scrape" in sig:
        fails.append("source HTML structure changes — selector-based scraping breaks silently")
    if "map" in sig:
        fails.append("region name spelling differs between data and shapefile — silent dropped rows")
    if "tokenize" in sig or "text" in sig:
        fails.append("text is multilingual without language detection")
    if "join" in sig:
        fails.append("join key has trailing whitespace or case inconsistency — produces unexpected NAs")
    if "time" in sig or "trend" in sig:
        fails.append("irregular time intervals inflate or deflate apparent trends")

    return fails if fails else ["pattern is broadly applicable — inspect data grain before applying"]


def infer_works_when(manifest: dict) -> list[str]:
    atype = manifest.get("analysis_type", "")
    sig = manifest.get("pattern_signature", "").lower()
    works = []

    if atype == "EDA":
        works.append("dataset has clear categorical + numeric columns for grouped comparisons")
        works.append("question is exploratory — no strong prior hypothesis")
    if atype in ("Predictive", "Modeling"):
        works.append("outcome column is clearly defined and has sufficient variance")
        works.append("features can be engineered from existing columns without external joins")
    if "scrape" in sig:
        works.append("supplemental context is unavailable in the flat file and worth the scraping overhead")
    if "map" in sig:
        works.append("geographic column can be matched to a standard ISO/FIPS shapefile without fuzzy joins")
    if "text" in sig or "tokenize" in sig:
        works.append("text is long-form English and benefits from word-level decomposition")
    if "trend" in sig:
        works.append("time dimension is regular and spans multiple periods with meaningful change")

    return works if works else ["dataset is clean, rectangular, and at a single grain"]


def build_hour_architecture(manifest: dict) -> dict:
    sig = manifest.get("pattern_signature", "").lower()
    atype = manifest.get("analysis_type", "")
    fn = manifest.get("function_name", "")
    concepts = manifest.get("atomic_concepts", [])

    h1_steps = ["Load data with load_tidyweek_data()", "Inspect schema and types", "Identify main grouping + metric columns"]
    if "scrape" in sig:
        h1_steps.append("Scrape supplemental reference table")
    if "reshape" in sig:
        h1_steps.append("Reshape from wide to long")
    if "join" in sig:
        h1_steps.append("Join tables on shared key")
    if "tokenize" in sig or "text" in sig:
        h1_steps.append("Tokenize text, remove stopwords, compute frequencies")
    if "map" in sig:
        h1_steps.append("Join to shapefile, plot choropleth")
    h1_steps.append("Build 3-4 core ggplot charts telling the main story")
    h1_steps.append("Write 150-word narrative summary")

    h2_steps = []
    if atype in ("Predictive", "Modeling") or "model" in sig:
        h2_steps = [
            "Engineer features from EDA findings",
            "Split with initial_split(), create v-fold CV",
            "Fit baseline model (linear/logistic)",
            "Tune LASSO / random forest / xgboost",
            "Compare models with collect_metrics()",
            "Interpret with vip / SHAP values",
            "Residual analysis + calibration plot",
        ]
    elif "text" in sig or "tokenize" in sig:
        h2_steps = [
            "TF-IDF or log-odds group comparison",
            "LDA / STM topic model (if corpus large enough)",
            "Bigram network graph with ggraph",
            "Sentiment arc if temporal dimension present",
        ]
    else:
        h2_steps = [
            "Fit linear model on main numeric outcome",
            "Compute bootstrap confidence intervals for key estimates",
            "Test for interaction effects between top 2 grouping vars",
            "Summarise effect sizes with broom::tidy()",
        ]

    h3_steps = [
        f"Quarto doc: {fn}_report.qmd with params for data year",
        "Hero chart: single best visualisation at 1200×628 (social media ratio)",
        "Instagram carousel: 5 slides (hook → data → insight → method → CTA)",
        "YouTube thumbnail text + chapter timestamps",
        "Shiny widget or Observable/D3 for one interactive element",
        f"TheDataShrink™ post template: title, 3 bullets, hashtags, link to episode page",
    ]

    return {
        "h1_eda": {
            "status": "pending",
            "qmd": f"h1_eda_{fn}.qmd",
            "steps": h1_steps,
        },
        "h2_modeling": {
            "status": "pending",
            "qmd": f"h2_modeling_{fn}.qmd",
            "steps": h2_steps,
        },
        "h3_communicate": {
            "status": "pending",
            "qmd": f"h3_communicate_{fn}.qmd",
            "steps": h3_steps,
            "channels": ["youtube", "instagram", "facebook", "website"],
            "brand": "TheDataShrink™",
        },
    }


def enrich_manifest(manifest_path: Path) -> bool:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))

    # Skip if already enriched
    if "atomic_concepts" in data and "hour_architecture" in data:
        return False

    # Infer and inject TheDataShrink™ concept fields
    data["atomic_concepts"] = infer_atomic_concepts(data)
    data["fails_when"] = infer_fails_when(data)
    data["works_when"] = infer_works_when(data)
    data["hour_architecture"] = build_hour_architecture(data)
    data["brand"] = "TheDataShrink™"

    manifest_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return True


def build_concept_index():
    """Write CONCEPT_INDEX.md — TheDataShrink™ concept library across all episodes."""
    episodes_root = EPISODES_ROOT
    concept_to_episodes: dict[str, list[str]] = {}

    for manifest_path in sorted(episodes_root.rglob("episode_manifest.json")):
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        for concept_key in data.get("atomic_concepts", []):
            concept_to_episodes.setdefault(concept_key, []).append(
                data.get("transcript_title", manifest_path.parent.name)
            )

    lines = [
        "# Concept Index — TheDataShrink™ × TidyTuesday",
        "",
        "TheDataShrink™ concept library: atomic reusable concepts extracted across all episodes.",
        "Each concept is independent of any single episode and reusable on any new dataset.",
        "",
        f"**Total concepts:** {len(concept_to_episodes)}",
        "",
        "---",
        "",
    ]

    for key in sorted(concept_to_episodes.keys()):
        meta = CONCEPT_CATALOGUE.get(key, {})
        label = meta.get("label", key.replace("_", " ").title())
        episodes = concept_to_episodes[key]
        works = meta.get("works_when", [])
        fails = meta.get("fails_when", [])

        lines += [
            f"## {label}",
            f"**key:** `{key}`  ",
            f"**episodes ({len(episodes)}):** " + ", ".join(f"`{e}`" for e in sorted(episodes[:5]))
            + (" + more" if len(episodes) > 5 else ""),
            "",
        ]
        if works:
            lines.append("**WORKS WHEN:**")
            for w in works:
                lines.append(f"- {w}")
            lines.append("")
        if fails:
            lines.append("**FAILS WHEN:**")
            for f in fails:
                lines.append(f"- {f}")
            lines.append("")
        lines.append("---")
        lines.append("")

    out = ROOT / "CONCEPT_INDEX.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Written {out} ({len(concept_to_episodes)} concepts)")


def main():
    print("=== Enriching episode manifests with TheDataShrink™ concept fields ===")
    enriched = 0
    skipped = 0
    for manifest_path in sorted(EPISODES_ROOT.rglob("episode_manifest.json")):
        if enrich_manifest(manifest_path):
            enriched += 1
        else:
            skipped += 1
    print(f"  Enriched: {enriched}, Already done: {skipped}")

    print("\n=== Building CONCEPT_INDEX.md ===")
    build_concept_index()

    print("\nDone. Run build_3hour_qmd.py to generate the 3-hour episode QMDs.")


if __name__ == "__main__":
    main()
