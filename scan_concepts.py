"""
scan_concepts.py — Deep concept extraction from all 102 Rmd files + 410 control table rows.

Scans the full corpus for atomic reusable concepts:
- Library usage patterns
- Function call signatures
- Geom / visualization types
- Statistical technique combinations
- Data manipulation idioms
- David Robinson signature patterns

Outputs:
  CONCEPT_INDEX.md  — updated with all discovered concepts
  concept_scan_raw.json  — raw scan data per Rmd file
  Updates all episode_manifest.json with enriched atomic_concepts[]
"""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DGRTWO = ROOT / "data-screencasts-dgrtwo"
EPISODES_ROOT = ROOT / "output" / "episodes"

# ─── Concept Definitions ─────────────────────────────────────────────────────
# Each entry: key → {label, detect, works_when, fails_when, category, tags}
# detect: list of regex patterns — ANY match in Rmd triggers this concept

CONCEPTS = {
    # ── DATA LOADING & SOURCES ────────────────────────────────────────────
    "tidytuesdayr_load": {
        "label": "TidyTuesdayR dataset loading",
        "category": "Data Loading",
        "detect": [r"tt_load\(", r"tidytuesdayR"],
        "works_when": ["weekly TidyTuesday dataset with a known date string"],
        "fails_when": ["dataset renamed or removed from TidyTuesdayR archive", "no internet / GitHub PAT needed"],
        "tags": ["loading", "tidytuesdayR"],
    },
    "web_scraping_rvest": {
        "label": "HTML scraping with rvest",
        "category": "Data Collection",
        "detect": [r"read_html\(", r"html_nodes?\(", r"html_elements?\(", r"library\(rvest\)"],
        "works_when": ["stable HTML table at a known URL", "supplemental reference not in flat file"],
        "fails_when": ["JS-rendered page (needs Playwright)", "rate-limited or auth-gated URL", "HTML structure changes"],
        "tags": ["scraping", "rvest", "web"],
    },
    "api_call_httr": {
        "label": "REST API call with httr / jsonlite",
        "category": "Data Collection",
        "detect": [r"GET\(", r"httr::", r"fromJSON\(", r"library\(jsonlite\)"],
        "works_when": ["public JSON API with stable schema"],
        "fails_when": ["API requires OAuth", "response schema changes without versioning"],
        "tags": ["api", "httr", "json"],
    },
    "world_bank_wdi": {
        "label": "World Bank WDI data enrichment",
        "category": "Data Collection",
        "detect": [r"library\(WDI\)", r"WDI\(", r"WDIsearch\("],
        "works_when": ["need country-level macro indicators (GDP, population, health)", "joining on ISO country code"],
        "fails_when": ["indicator has missing years for key countries", "needs real-time data"],
        "tags": ["world bank", "WDI", "country", "enrichment"],
    },
    "us_census_tidycensus": {
        "label": "US Census / ACS data with tidycensus",
        "category": "Data Collection",
        "detect": [r"library\(tidycensus\)", r"get_acs\(", r"get_decennial\(", r"library\(tigris\)"],
        "works_when": ["US geographic analysis needing demographic context", "joining to Census FIPS codes"],
        "fails_when": ["non-US geography", "variable codes change between Census years"],
        "tags": ["census", "tidycensus", "USA", "geographic"],
    },
    "statsboard_soccer": {
        "label": "StatsBomb event-level soccer data",
        "category": "Data Collection",
        "detect": [r"library\(StatsBombR\)", r"StatsBombR"],
        "works_when": ["event-level soccer analysis (passes, shots, xG)"],
        "fails_when": ["non-soccer sport", "match not in free StatsBomb dataset"],
        "tags": ["soccer", "StatsBomb", "sports"],
    },
    # ── DATA CLEANING & MANIPULATION ─────────────────────────────────────
    "janitor_clean": {
        "label": "Column name cleaning with janitor",
        "category": "Data Cleaning",
        "detect": [r"clean_names\(", r"library\(janitor\)", r"tabyl\("],
        "works_when": ["raw CSV with spaces, caps, or special chars in column names"],
        "fails_when": ["column names are already snake_case"],
        "tags": ["janitor", "cleaning", "names"],
    },
    "fuzzy_join": {
        "label": "Fuzzy / approximate string join",
        "category": "Data Manipulation",
        "detect": [r"library\(fuzzyjoin\)", r"stringdist_join\(", r"fuzzy_join\(", r"regex_join\("],
        "works_when": ["two tables share a text key but with spelling variation", "need to join on regex pattern"],
        "fails_when": ["key is numeric or exact", "string distance threshold is ambiguous across rows"],
        "tags": ["fuzzyjoin", "join", "strings", "matching"],
    },
    "pivot_reshape": {
        "label": "Reshape wide↔long with pivot_longer / pivot_wider",
        "category": "Data Manipulation",
        "detect": [r"pivot_longer\(", r"pivot_wider\(", r"gather\(", r"spread\("],
        "works_when": ["wide format with repeated column suffixes", "need one-row-per-observation for ggplot"],
        "fails_when": ["columns have inconsistent naming patterns without `names_pattern`", "values need type coercion first"],
        "tags": ["reshape", "pivot", "tidy"],
    },
    "unnest_list_cols": {
        "label": "Unnesting list columns (unnest / separate_rows)",
        "category": "Data Manipulation",
        "detect": [r"unnest\(", r"separate_rows\(", r"unnest_wider\(", r"unnest_longer\("],
        "works_when": ["column contains comma-separated tags, JSON arrays, or nested lists"],
        "fails_when": ["list elements have inconsistent length or names"],
        "tags": ["unnest", "list columns", "nested data"],
    },
    "countrycode_standardize": {
        "label": "Country name / code standardization with countrycode",
        "category": "Data Manipulation",
        "detect": [r"countrycode\(", r"library\(countrycode\)"],
        "works_when": ["dataset mixes country names, ISO2, ISO3, or continent labels"],
        "fails_when": ["country names are very non-standard (historical names, disputed territories)"],
        "tags": ["countrycode", "country", "standardize", "ISO"],
    },
    "lubridate_dates": {
        "label": "Date parsing and arithmetic with lubridate",
        "category": "Data Manipulation",
        "detect": [r"library\(lubridate\)", r"ymd\(", r"mdy\(", r"floor_date\(", r"year\(", r"month\("],
        "works_when": ["date column is a string in a known format", "need year/month/week extraction or rounding"],
        "fails_when": ["ambiguous date formats (e.g. 01/02/03)", "timezone-dependent analysis without tz specification"],
        "tags": ["lubridate", "dates", "time", "parsing"],
    },
    "glue_strings": {
        "label": "String interpolation with glue",
        "category": "Data Manipulation",
        "detect": [r"library\(glue\)", r"glue\(", r"glue_data\("],
        "works_when": ["need to construct labels, titles, or text from data values"],
        "fails_when": ["variables contain special characters that break glue syntax"],
        "tags": ["glue", "strings", "labels"],
    },
    "reorder_within_facets": {
        "label": "Reorder bars within each facet (David Robinson signature)",
        "category": "Visualization",
        "detect": [r"reorder_within\(", r"scale_x_reordered\(", r"scale_y_reordered\("],
        "works_when": ["faceted bar chart where each facet has its own ranking", "showing top-N per group"],
        "fails_when": ["single panel plot (just use fct_reorder)", "groups are not comparable in size"],
        "tags": ["reorder_within", "facet", "ranking", "bar chart", "drlib"],
    },
    # ── VISUALIZATION PATTERNS ─────────────────────────────────────────────
    "animated_transitions": {
        "label": "Animated chart with gganimate",
        "category": "Visualization",
        "detect": [r"library\(gganimate\)", r"transition_time\(", r"transition_states\(", r"transition_reveal\(", r"animate\("],
        "works_when": ["strong time dimension", "story benefits from showing change in motion", "YouTube / social media context"],
        "fails_when": ["static report", "too many categories causing visual clutter", "render time is prohibitive"],
        "tags": ["gganimate", "animation", "time", "motion"],
    },
    "ridge_joy_plot": {
        "label": "Ridge / joy plot for distribution comparison (ggridges)",
        "category": "Visualization",
        "detect": [r"library\(ggridges\)", r"geom_density_ridges\(", r"geom_ridgeline\("],
        "works_when": ["many ordered groups with overlapping distributions", "showing how distribution shifts over time or category"],
        "fails_when": ["fewer than 4-5 groups (use boxplot instead)", "distributions are discrete"],
        "tags": ["ggridges", "distribution", "density", "joy plot"],
    },
    "interactive_plotly": {
        "label": "Interactive chart with plotly / ggplotly",
        "category": "Visualization",
        "detect": [r"library\(plotly\)", r"ggplotly\(", r"plot_ly\("],
        "works_when": ["web publishing context", "user needs to hover/zoom/filter", "too many points for static labels"],
        "fails_when": ["print / PDF output", "very large datasets slow render in browser"],
        "tags": ["plotly", "interactive", "web", "hover"],
    },
    "label_repulsion_ggrepel": {
        "label": "Non-overlapping point labels with ggrepel",
        "category": "Visualization",
        "detect": [r"library\(ggrepel\)", r"geom_text_repel\(", r"geom_label_repel\("],
        "works_when": ["scatter plot with meaningful point labels", "up to ~30-50 labelled points"],
        "fails_when": ["hundreds of points (labels become unreadable)", "labels need exact positioning"],
        "tags": ["ggrepel", "labels", "scatter", "annotation"],
    },
    "heatmap_tile": {
        "label": "Heatmap with geom_tile",
        "category": "Visualization",
        "detect": [r"geom_tile\("],
        "works_when": ["two categorical axes with a numeric fill value", "showing a matrix of relationships"],
        "fails_when": ["too many categories on one axis (> 30, becomes unreadable)", "continuous axes (use geom_raster)"],
        "tags": ["heatmap", "geom_tile", "matrix", "categorical"],
    },
    "confidence_ribbon": {
        "label": "Confidence / prediction band with geom_ribbon",
        "category": "Visualization",
        "detect": [r"geom_ribbon\("],
        "works_when": ["time series or ordered x-axis with upper/lower bounds", "model prediction intervals"],
        "fails_when": ["ribbon bands overlap heavily without alpha transparency", "non-ordered x axis"],
        "tags": ["ribbon", "confidence interval", "band", "uncertainty"],
    },
    "log_scale": {
        "label": "Log scale transformation for skewed distributions",
        "category": "Visualization",
        "detect": [r"scale_x_log10\(", r"scale_y_log10\(", r"trans.*log", r"log10\("],
        "works_when": ["right-skewed numeric variable spanning multiple orders of magnitude", "multiplicative relationships"],
        "fails_when": ["zeros or negative values in data", "audience unfamiliar with log scale"],
        "tags": ["log scale", "transformation", "skew", "power law"],
    },
    "network_graph_ggraph": {
        "label": "Network / co-occurrence graph with ggraph + igraph",
        "category": "Visualization",
        "detect": [r"library\(ggraph\)", r"library\(igraph\)", r"library\(tidygraph\)", r"geom_edge_link\(", r"geom_node_point\(", r"as_tbl_graph\("],
        "works_when": ["pairwise relationships between entities", "co-occurrence of tokens or events", "graph data with nodes and edges"],
        "fails_when": ["too many nodes (> 200) without filtering", "graph is fully connected (no meaningful clusters)"],
        "tags": ["ggraph", "igraph", "network", "graph", "co-occurrence"],
    },
    "choropleth_sf": {
        "label": "Choropleth map with sf / geom_sf",
        "category": "Visualization",
        "detect": [r"library\(sf\)", r"geom_sf\(", r"geom_polygon\(.*map", r"st_read\(", r"library\(tigris\)"],
        "works_when": ["region column matchable to a shapefile", "spatial distribution is the main story"],
        "fails_when": ["region names differ from shapefile (needs fuzzy join)", "sub-region level without matching geometry", "CRS mismatch"],
        "tags": ["sf", "map", "spatial", "choropleth", "geom_sf"],
    },
    "error_bar_coef_plot": {
        "label": "Coefficient plot with error bars (broom + ggplot)",
        "category": "Visualization",
        "detect": [r"geom_errorbarh\(", r"geom_errorbar\("],
        "works_when": ["model output with confidence intervals", "comparing effect sizes across groups"],
        "fails_when": ["intervals are asymmetric without transformation", "too many coefficients without filtering"],
        "tags": ["error bars", "coefficient plot", "uncertainty", "broom"],
    },
    "shiny_app": {
        "label": "Shiny interactive application",
        "category": "Visualization",
        "detect": [r"library\(shiny\)", r"shinyApp\(", r"shinymetrics", r"library\(shinymetrics\)"],
        "works_when": ["user needs to filter, select, or explore data interactively", "web publishing with server"],
        "fails_when": ["static report context", "no server infrastructure available"],
        "tags": ["shiny", "interactive", "app", "web"],
    },
    # ── TEXT ANALYSIS ────────────────────────────────────────────────────
    "tokenization_pipeline": {
        "label": "Tidytext tokenization pipeline",
        "category": "Text Analysis",
        "detect": [r"unnest_tokens\(", r"library\(tidytext\)"],
        "works_when": ["raw text column", "want word-level frequency or sentiment analysis"],
        "fails_when": ["text is highly structured (JSON, code)", "non-English without custom stopwords"],
        "tags": ["tidytext", "tokenize", "NLP", "words"],
    },
    "tf_idf_comparison": {
        "label": "TF-IDF group comparison",
        "category": "Text Analysis",
        "detect": [r"bind_tf_idf\("],
        "works_when": ["multiple groups with text documents", "find distinctive vocabulary per group"],
        "fails_when": ["corpus is tiny (< 100 docs)", "groups very unequal in size without normalisation"],
        "tags": ["tf-idf", "text", "comparison", "distinctive words"],
    },
    "log_odds_ratio": {
        "label": "Log-odds ratio for group vocabulary contrast (tidylo)",
        "category": "Text Analysis",
        "detect": [r"bind_log_odds\(", r"library\(tidylo\)"],
        "works_when": ["two groups with token counts", "want statistically grounded vocabulary contrast"],
        "fails_when": ["groups not mutually exclusive", "token counts near zero (Jeffreys prior needed)"],
        "tags": ["log-odds", "tidylo", "text", "contrast"],
    },
    "pairwise_token_correlation": {
        "label": "Pairwise token correlation with widyr",
        "category": "Text Analysis",
        "detect": [r"pairwise_cor\(", r"pairwise_count\(", r"library\(widyr\)"],
        "works_when": ["want to find which words appear together across documents", "seed for network graph"],
        "fails_when": ["very large vocabulary without filtering (memory)", "documents are very short"],
        "tags": ["widyr", "pairwise", "correlation", "co-occurrence"],
    },
    "structural_topic_model": {
        "label": "Structural topic model (stm)",
        "category": "Text Analysis",
        "detect": [r"library\(stm\)", r"stm\(", r"cast_dtm\("],
        "works_when": ["large corpus (> 500 docs)", "want to discover latent themes with metadata covariates"],
        "fails_when": ["small corpus (< 200 docs)", "documents are very short (< 20 words)"],
        "tags": ["stm", "topic model", "LDA", "themes"],
    },
    "sparse_matrix_text": {
        "label": "Sparse document-term matrix for LASSO (cast_sparse)",
        "category": "Text Analysis",
        "detect": [r"cast_sparse\(", r"cast_dtm\("],
        "works_when": ["large text corpus as input to penalised regression", "want LASSO to select relevant tokens"],
        "fails_when": ["corpus is small (dense matrix is fine)", "tokens need preprocessing first"],
        "tags": ["sparse matrix", "cast_sparse", "LASSO", "text features"],
    },
    "text_recipes_tidymodels": {
        "label": "Text preprocessing in tidymodels recipe (textrecipes)",
        "category": "Text Analysis",
        "detect": [r"library\(textrecipes\)", r"step_tokenize\(", r"step_tfidf\(", r"step_word_embeddings\("],
        "works_when": ["text as feature in tidymodels pipeline", "want standardized preprocessing + CV"],
        "fails_when": ["corpus is tiny", "need custom tokenizer not in textrecipes"],
        "tags": ["textrecipes", "tidymodels", "text features", "recipe"],
    },
    "nlp_spacyr": {
        "label": "NLP entity recognition with spaCy (spacyr)",
        "category": "Text Analysis",
        "detect": [r"library\(spacyr\)", r"spacy_parse\(", r"spacy_extract_entity\("],
        "works_when": ["need named entity recognition (people, places, orgs)", "POS tagging for linguistic analysis"],
        "fails_when": ["no Python + spaCy installation", "domain-specific entities not in base model"],
        "tags": ["spacyr", "spaCy", "NLP", "entity recognition"],
    },
    # ── STATISTICAL MODELING ─────────────────────────────────────────────
    "linear_model_broom": {
        "label": "Linear model with broom output tidying",
        "category": "Modeling",
        "detect": [r"\blm\(", r"broom::tidy\(", r"library\(broom\)"],
        "works_when": ["continuous numeric outcome", "want interpretable coefficients", "checking linear assumptions"],
        "fails_when": ["outcome is binary or count (use glm)", "strong non-linearity without splines"],
        "tags": ["lm", "linear model", "broom", "regression"],
    },
    "logistic_regression": {
        "label": "Logistic regression (glm binomial)",
        "category": "Modeling",
        "detect": [r"glm\(.*binomial", r"family\s*=\s*binomial", r"glm\(.*logit"],
        "works_when": ["binary outcome", "interpretable log-odds needed", "small-to-medium dataset"],
        "fails_when": ["severe class imbalance without weighting", "many dummy features (use LASSO instead)"],
        "tags": ["glm", "logistic", "binary", "classification"],
    },
    "lasso_glmnet": {
        "label": "LASSO / Ridge regression with glmnet (cross-validated)",
        "category": "Modeling",
        "detect": [r"cv\.glmnet\(", r"library\(glmnet\)", r"library\(Matrix\)"],
        "works_when": ["many predictors (especially sparse text features)", "want automatic feature selection"],
        "fails_when": ["features are highly correlated in groups (use elastic net or group lasso)", "need non-linear relationships"],
        "tags": ["glmnet", "LASSO", "regularisation", "feature selection"],
    },
    "tidymodels_cv": {
        "label": "Tidymodels cross-validation pipeline (vfold + tune_grid)",
        "category": "Modeling",
        "detect": [r"library\(tidymodels\)", r"vfold_cv\(", r"tune_grid\(", r"initial_split\(", r"workflow\("],
        "works_when": ["tabular data with clear outcome", "comparing multiple model specs with hyperparameter tuning"],
        "fails_when": ["time series (needs sliding window CV)", "very small datasets (< 200 rows, too few folds)"],
        "tags": ["tidymodels", "cross-validation", "tune", "workflow"],
    },
    "survival_analysis": {
        "label": "Survival / time-to-event analysis (survival package)",
        "category": "Modeling",
        "detect": [r"library\(survival\)", r"Surv\(", r"survfit\(", r"coxph\("],
        "works_when": ["time-to-event outcome with censoring (did not observe event)"],
        "fails_when": ["no censoring indicator", "competing risks without cause-specific adjustment"],
        "tags": ["survival", "Surv", "Kaplan-Meier", "time-to-event"],
    },
    "spline_regression": {
        "label": "Spline regression for non-linear smoothing (splines::ns)",
        "category": "Modeling",
        "detect": [r"library\(splines\)", r"ns\(", r"bs\(", r"splines::"],
        "works_when": ["known non-linear relationship (e.g. age effects, seasonal curves)", "want smooth curve in lm/glm framework"],
        "fails_when": ["too few data points to fit the knots", "knot placement is not principled"],
        "tags": ["splines", "ns", "non-linear", "smoothing"],
    },
    "empirical_bayes": {
        "label": "Empirical Bayes estimation for proportions (ebbr)",
        "category": "Modeling",
        "detect": [r"library\(ebbr\)", r"add_ebb_estimate\(", r"augment_ebb\(", r"ebbr::"],
        "works_when": ["proportion outcome with wildly varying sample sizes per group", "want to shrink noisy small-sample estimates toward the global mean"],
        "fails_when": ["all groups have large sample sizes (shrinkage is negligible)", "prior is clearly wrong"],
        "tags": ["ebbr", "empirical Bayes", "shrinkage", "proportion"],
    },
    "nonlinear_nls": {
        "label": "Nonlinear least squares fitting (nls)",
        "category": "Modeling",
        "detect": [r"\bnls\("],
        "works_when": ["known parametric form for non-linear relationship (e.g. exponential, logistic growth)"],
        "fails_when": ["starting values poorly chosen (fails to converge)", "form is unknown (use loess/GAM instead)"],
        "tags": ["nls", "nonlinear", "curve fitting"],
    },
    "bootstrap_ci": {
        "label": "Bootstrap confidence intervals (rsample::bootstraps)",
        "category": "Modeling",
        "detect": [r"bootstraps\(", r"library\(rsample\)"],
        "works_when": ["want distribution-free uncertainty estimates for any statistic"],
        "fails_when": ["time-dependent data without block bootstrap", "n < 30"],
        "tags": ["bootstrap", "rsample", "confidence interval", "uncertainty"],
    },
    # ── TIME SERIES ─────────────────────────────────────────────────────
    "rolling_window_metrics": {
        "label": "Rolling window aggregation (tidymetrics / slider)",
        "category": "Time Series",
        "detect": [r"library\(tidymetrics\)", r"roll_summarise\(", r"library\(timetk\)", r"library\(slider\)"],
        "works_when": ["regular time series needing moving average or rolling sum"],
        "fails_when": ["irregular time intervals without imputation first"],
        "tags": ["rolling window", "tidymetrics", "timetk", "moving average"],
    },
    "time_series_forecast": {
        "label": "Time series decomposition and forecasting (sweep / fable)",
        "category": "Time Series",
        "detect": [r"library\(sweep\)", r"sw_tidy\(", r"library\(fable\)", r"library\(forecast\)", r"auto\.arima\(", r"ETS\("],
        "works_when": ["regular time series with enough history (> 2 seasonal cycles)"],
        "fails_when": ["very short series", "structural breaks in the series"],
        "tags": ["forecast", "sweep", "fable", "ARIMA", "ETS"],
    },
    # ── EDA PATTERNS ────────────────────────────────────────────────────
    "grouped_summary_ggplot": {
        "label": "Grouped summary → ggplot storytelling",
        "category": "EDA",
        "detect": [r"group_by\(.*\)\s*%>%\s*summaris[ez]", r"count\(.*sort", r"fct_lump\(", r"fct_reorder\("],
        "works_when": ["categorical grouping variable", "want to compare means, medians, or counts across groups"],
        "fails_when": ["too many groups (> 20) without fct_lump or top-N filter"],
        "tags": ["group_by", "summarise", "fct_reorder", "bar chart"],
    },
    "time_series_trend": {
        "label": "Time series trend line visualisation",
        "category": "EDA",
        "detect": [r"geom_line\(", r"scale_x_date\(", r"geom_smooth\("],
        "works_when": ["date column with regular intervals", "want to show change over time"],
        "fails_when": ["irregular time points inflate apparent trends", "missing periods without interpolation"],
        "tags": ["time series", "trend", "geom_line", "date"],
    },
    "multi_table_join": {
        "label": "Multi-table join and grain alignment",
        "category": "EDA",
        "detect": [r"left_join\(", r"inner_join\(", r"full_join\(", r"right_join\("],
        "works_when": ["multiple tables share a clean join key"],
        "fails_when": ["keys have case mismatch or trailing spaces without normalisation", "many-to-many join without deduplication"],
        "tags": ["join", "multi-table", "merge", "left_join"],
    },
    "faceted_comparison": {
        "label": "Faceted small multiples (facet_wrap / facet_grid)",
        "category": "EDA",
        "detect": [r"facet_wrap\(", r"facet_grid\("],
        "works_when": ["2-20 groups that share the same x/y scale", "comparing panel structure across a variable"],
        "fails_when": ["too many facets (> 30, unreadable)", "groups have very different scales (use free scales)"],
        "tags": ["facet_wrap", "facet_grid", "small multiples", "comparison"],
    },
    "geom_smooth_loess": {
        "label": "Trend smoothing with geom_smooth (loess / lm)",
        "category": "EDA",
        "detect": [r"geom_smooth\("],
        "works_when": ["scatter plot with noisy relationship", "want to show trend direction without parametric assumption"],
        "fails_when": ["very few points (loess overfits)", "trend has structural breaks that loess averages over"],
        "tags": ["geom_smooth", "loess", "trend", "smoothing"],
    },
    "skim_inspect": {
        "label": "Schema inspection and skimming (skimr / glimpse)",
        "category": "EDA",
        "detect": [r"skimr::", r"skim\(", r"glimpse\(", r"summary\("],
        "works_when": ["first look at any new dataset", "checking for NAs, types, and distribution shape"],
        "fails_when": ["output is too wide for console — pipe to `kable()` for reports"],
        "tags": ["skimr", "glimpse", "inspection", "EDA first step"],
    },
    "geom_histogram_density": {
        "label": "Distribution shape with histogram / density",
        "category": "EDA",
        "detect": [r"geom_histogram\(", r"geom_density\("],
        "works_when": ["continuous variable", "want to see shape (skew, bimodality, outliers)"],
        "fails_when": ["discrete variable with few levels (use bar chart)", "bandwidth / bins not tuned"],
        "tags": ["histogram", "density", "distribution", "continuous"],
    },
    "boxplot_jitter": {
        "label": "Boxplot / jitter for group distribution comparison",
        "category": "EDA",
        "detect": [r"geom_boxplot\(", r"geom_violin\(", r"geom_jitter\("],
        "works_when": ["comparing distribution spread across 3-15 groups"],
        "fails_when": ["very unequal group sizes (median is still valid but widths mislead)", "too many outliers obscuring the box"],
        "tags": ["boxplot", "violin", "jitter", "distribution comparison"],
    },
    "correlation_matrix": {
        "label": "Correlation matrix / heatmap",
        "category": "EDA",
        "detect": [r"\bcor\(", r"corrplot", r"cor_mat\(", r"correlate\("],
        "works_when": ["multiple numeric columns", "want to find candidate predictor pairs"],
        "fails_when": ["non-numeric columns without encoding", "correlation without checking for non-linearity"],
        "tags": ["correlation", "corrplot", "heatmap", "multivariate"],
    },
    # ── MODELING WORKFLOW ────────────────────────────────────────────────
    "broom_model_output": {
        "label": "Model output tidying with broom (tidy / glance / augment)",
        "category": "Modeling Workflow",
        "detect": [r"broom::tidy\(", r"broom::glance\(", r"broom::augment\(", r"tidy\(.*model", r"glance\("],
        "works_when": ["any base R model (lm, glm, survival, etc.)", "want ggplot-ready model output"],
        "fails_when": ["model class not supported by broom (check broom::tidy methods)"],
        "tags": ["broom", "tidy", "model output", "coefficients"],
    },
    "variable_importance_vip": {
        "label": "Variable importance plot (vip)",
        "category": "Modeling Workflow",
        "detect": [r"library\(vip\)", r"vi\(", r"vip\("],
        "works_when": ["tree models or regularised regression", "want to rank feature contributions"],
        "fails_when": ["correlated features — importance is split and misleading without grouped permutation"],
        "tags": ["vip", "variable importance", "feature selection", "interpretation"],
    },
    # ── DATA OUTPUT & PUBLISHING ─────────────────────────────────────────
    "quarto_parameterised": {
        "label": "Parameterised Quarto / RMarkdown report",
        "category": "Publishing",
        "detect": [r"params\$", r"params:", r"render\(.*params"],
        "works_when": ["same analysis needs to run for multiple years, regions, or cohorts"],
        "fails_when": ["parameters change the fundamental analysis logic (not just filters)"],
        "tags": ["quarto", "params", "parameterised", "reproducible"],
    },
    # ── DAVID ROBINSON SIGNATURE IDIOMS (SA Andrei — high frequency) ──────
    "fct_reorder_stat": {
        "label": "Factor reorder by statistic (fct_reorder) — 282 uses",
        "category": "David Robinson Idioms",
        "detect": [r"fct_reorder\("],
        "works_when": ["bar/lollipop chart where bars should be ranked by a numeric value", "any ggplot where alphabetical order tells no story"],
        "fails_when": ["factor has a natural order (dates, severity levels) — use fct_relevel instead", "ties in the statistic cause unstable ordering"],
        "tags": ["fct_reorder", "forcats", "ordering", "ranking", "bar chart"],
    },
    "fct_lump_infrequent": {
        "label": "Collapse infrequent factor levels to 'Other' (fct_lump) — 148 uses",
        "category": "David Robinson Idioms",
        "detect": [r"fct_lump\("],
        "works_when": ["categorical variable with long tail of rare levels", "want to keep top-N categories and aggregate the rest"],
        "fails_when": ["all levels are equally frequent (lumps nothing)", "the 'Other' category would dominate and mislead"],
        "tags": ["fct_lump", "forcats", "categories", "top-N", "long tail"],
    },
    "crossing_simulation_grid": {
        "label": "Cartesian grid expansion for simulation / parameter sweep (crossing) — 47 uses",
        "category": "David Robinson Idioms",
        "detect": [r"\bcrossing\(", r"expand_grid\("],
        "works_when": ["want all combinations of parameter values for simulation or comparison", "Riddler-style probability problems"],
        "fails_when": ["grid is too large (exponential blowup)", "combinations are logically constrained and need filtering after expand"],
        "tags": ["crossing", "expand_grid", "simulation", "combinatorics"],
    },
    "add_count_inline": {
        "label": "Add group count without collapsing (add_count) — 42 uses",
        "category": "David Robinson Idioms",
        "detect": [r"\badd_count\("],
        "works_when": ["want to keep all rows but annotate each with group size (e.g. for filtering rare groups)"],
        "fails_when": ["you want the count as a summary (use count() instead)", "group variables are not specified correctly"],
        "tags": ["add_count", "group size", "filter rare", "annotation"],
    },
    "fct_relevel_manual": {
        "label": "Manual factor level ordering (fct_relevel) — 25 uses",
        "category": "David Robinson Idioms",
        "detect": [r"fct_relevel\("],
        "works_when": ["factor has a meaningful non-alphabetical order (Low/Medium/High, before/after, etc.)"],
        "fails_when": ["level names you specify don't match the actual levels exactly (silent no-op)"],
        "tags": ["fct_relevel", "forcats", "ordering", "manual"],
    },
    "parse_number_dirty": {
        "label": "Extract numeric from dirty strings (parse_number) — 18 uses",
        "category": "Data Cleaning",
        "detect": [r"parse_number\("],
        "works_when": ["column contains numbers mixed with currency symbols, commas, units (e.g. '$1,200', '45%', '3.5k')"],
        "fails_when": ["string has multiple numbers and you need a specific one", "locale-specific decimal separators need explicit locale argument"],
        "tags": ["parse_number", "readr", "numeric extraction", "dirty data"],
    },
    "cumsum_running_total": {
        "label": "Running total / cumulative sum (cumsum) — 11 uses",
        "category": "EDA",
        "detect": [r"\bcumsum\("],
        "works_when": ["time-ordered data where cumulative growth is the story (launches, publications, cumulative cases)"],
        "fails_when": ["data is not time-ordered", "gaps in time series inflate apparent acceleration"],
        "tags": ["cumsum", "running total", "cumulative", "time series"],
    },
    "ntile_quantile_bucket": {
        "label": "Equal-frequency quantile bucketing (ntile) — 8 uses",
        "category": "EDA",
        "detect": [r"\bntile\("],
        "works_when": ["want to split a numeric variable into N equal-sized groups for comparison", "creating percentile deciles or quartiles"],
        "fails_when": ["variable has many ties (quantile boundaries are unstable)", "equal-frequency buckets are misleading when values cluster at extremes"],
        "tags": ["ntile", "quantile", "bucket", "decile", "percentile"],
    },
    "case_when_conditional_col": {
        "label": "Conditional column creation with case_when — 7 uses",
        "category": "Data Manipulation",
        "detect": [r"\bcase_when\("],
        "works_when": ["need to create a new column with 3+ conditional branches (replaces nested ifelse)"],
        "fails_when": ["conditions overlap without explicit priority order (first match wins — document the intent)", "default case is omitted (produces NA silently)"],
        "tags": ["case_when", "conditional", "mutate", "ifelse"],
    },
    "str_detect_filter": {
        "label": "Regex-based text filter / flag with str_detect — 43 uses",
        "category": "Data Manipulation",
        "detect": [r"\bstr_detect\(", r"\bstr_remove\(", r"\bstr_extract\("],
        "works_when": ["need to filter rows where a text column matches a pattern", "flagging rows with keyword presence"],
        "fails_when": ["pattern is language-specific without locale handling", "full parsing is needed (use tidytext instead of string ops)"],
        "tags": ["str_detect", "stringr", "regex", "filter", "text"],
    },
    "scales_axis_labels": {
        "label": "Human-readable axis labels with scales (label_percent, label_comma, label_dollar)",
        "category": "Visualization",
        "detect": [r"label_percent\(", r"label_comma\(", r"label_dollar\(", r"scales::comma\(", r"scales::percent\(", r"percent_format\(", r"comma_format\("],
        "works_when": ["axis shows proportions (→ percent), large numbers (→ comma), or currency (→ dollar)", "audience is non-technical and raw numbers are confusing"],
        "fails_when": ["precision matters and rounding in the label format obscures it"],
        "tags": ["scales", "label_percent", "label_comma", "axis", "formatting"],
    },
    "coord_flip_horizontal": {
        "label": "Horizontal bar chart with coord_flip (or native y aesthetic)",
        "category": "Visualization",
        "detect": [r"coord_flip\("],
        "works_when": ["long category labels that overlap on the x-axis", "ranking bars where the reader reads down rather than across"],
        "fails_when": ["already using y for position — just map directly to y aesthetic in newer ggplot2 versions"],
        "tags": ["coord_flip", "horizontal bar", "category labels", "ggplot"],
    },
    "theme_set_global": {
        "label": "Global ggplot theme with theme_set (David Robinson default: theme_light)",
        "category": "Visualization",
        "detect": [r"theme_set\(", r"theme_light\(", r"theme_minimal\("],
        "works_when": ["want consistent look across all plots in a script without repeating theme() on each"],
        "fails_when": ["individual plots need different themes — theme_set is a global side effect"],
        "tags": ["theme_set", "theme_light", "global theme", "ggplot", "consistency"],
    },
    "geom_area_stacked": {
        "label": "Area / stacked area chart (geom_area) for composition over time",
        "category": "Visualization",
        "detect": [r"geom_area\("],
        "works_when": ["showing how parts of a whole evolve over time", "categories are non-overlapping and sum to 100%"],
        "fails_when": ["many categories — lower bands are hard to read", "categories overlap (use geom_ribbon instead)"],
        "tags": ["geom_area", "stacked area", "composition", "time series"],
    },
    "geom_step_discrete_time": {
        "label": "Step chart for discrete time jumps (geom_step)",
        "category": "Visualization",
        "detect": [r"geom_step\("],
        "works_when": ["value changes discretely at specific time points (survival curves, cumulative counts, policy changes)"],
        "fails_when": ["interpolation between points is meaningful — use geom_line instead"],
        "tags": ["geom_step", "step chart", "discrete", "survival", "cumulative"],
    },
    "purrr_map_iterate": {
        "label": "Functional iteration over lists / data frames with purrr::map",
        "category": "Data Manipulation",
        "detect": [r"\bmap\(", r"\bmap_df\(", r"\bmap_dbl\(", r"\bmap_chr\(", r"\bmap2\(", r"\bimap\(", r"library\(purrr\)"],
        "works_when": ["applying the same function to a list of data frames, file paths, or parameter sets"],
        "fails_when": ["function has side effects that depend on order", "list is very large and a vectorised function exists"],
        "tags": ["purrr", "map", "functional", "iteration", "list"],
    },
}


# ─── Scanner ─────────────────────────────────────────────────────────────────

def scan_rmd(rmd_path: Path) -> list[str]:
    """Return list of concept keys found in this Rmd file."""
    text = rmd_path.read_text(encoding="utf-8", errors="ignore")
    found = []
    for key, meta in CONCEPTS.items():
        for pattern in meta["detect"]:
            if re.search(pattern, text):
                found.append(key)
                break
    return found


def slug_to_rmd(code_file: str) -> Path | None:
    """Resolve a code_file reference to an actual Rmd path."""
    if not code_file:
        return None
    # Try dgrtwo directly
    fname = Path(code_file).name
    p = DGRTWO / fname
    if p.exists():
        return p
    # Try any Rmd in dgrtwo matching the stem
    stem = Path(code_file).stem.lower().replace("-", "_").replace(" ", "_")
    for f in DGRTWO.glob("*.Rmd"):
        if f.stem.lower().replace("-", "_") == stem:
            return f
    return None


def main():
    print("=== Scanning all Rmd files ===")

    # 1. Scan every Rmd in dgrtwo
    rmd_concepts: dict[str, list[str]] = {}
    for rmd in sorted(DGRTWO.glob("*.Rmd")):
        found = scan_rmd(rmd)
        rmd_concepts[rmd.stem] = found
        print(f"  {rmd.name}: {len(found)} concepts → {found}")

    # 2. Load control_table_full.csv to get title → code_file mapping
    ct_path = ROOT / "control_table_full.csv"
    title_to_concepts: dict[str, list[str]] = {}
    with ct_path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            cf = row.get("code_file", "").strip()
            title = row.get("transcript_title", "").strip()
            if not cf or not title:
                continue
            fname_stem = Path(cf).stem
            # Try exact match
            concepts = rmd_concepts.get(fname_stem)
            if concepts is None:
                # Try normalised match
                norm = fname_stem.lower().replace("-", "_")
                for k, v in rmd_concepts.items():
                    if k.lower().replace("-", "_") == norm:
                        concepts = v
                        break
            if concepts is not None:
                title_to_concepts[title] = concepts

    print(f"\n  Mapped {len(title_to_concepts)} titles to concepts")

    # 3. Build concept → episodes mapping
    concept_to_episodes: dict[str, list[str]] = defaultdict(list)
    for title, concepts in title_to_concepts.items():
        for c in concepts:
            concept_to_episodes[c].append(title)

    # 4. Update episode_manifest.json files
    print("\n=== Updating episode manifests ===")
    updated = 0
    for manifest_path in sorted(EPISODES_ROOT.rglob("episode_manifest.json")):
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        title = data.get("transcript_title", "")
        cf = data.get("source_files", {}).get("code_file", "")
        fname_stem = Path(cf).stem if cf else ""

        new_concepts = rmd_concepts.get(fname_stem)
        if new_concepts is None:
            # Try via title
            new_concepts = title_to_concepts.get(title, data.get("atomic_concepts", []))

        old = set(data.get("atomic_concepts", []))
        new_set = set(new_concepts or [])
        if new_set != old:
            data["atomic_concepts"] = sorted(new_set)
            manifest_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            updated += 1

    print(f"  Updated {updated} manifests")

    # 5. Save raw scan
    raw_path = ROOT / "concept_scan_raw.json"
    raw_path.write_text(json.dumps(rmd_concepts, indent=2), encoding="utf-8")
    print(f"\n  Raw scan saved → {raw_path.name}")

    # 6. Build CONCEPT_INDEX.md
    print("\n=== Building CONCEPT_INDEX.md ===")
    lines = [
        "# Concept Index — TheDataShrink™ × TidyTuesday",
        "",
        "DataX Stage 2/3 output: atomic reusable concepts extracted from 102 Rmd files + 410 episodes.",
        "Each concept is independent of any single episode and reusable on any new dataset.",
        "",
        f"**Total concepts:** {len(concept_to_episodes)}  ",
        f"**Total Rmd files scanned:** {len(rmd_concepts)}  ",
        f"**Total episodes mapped:** {len(title_to_concepts)}",
        "",
        "---",
        "",
    ]

    # Group by category
    by_category: dict[str, list[tuple[str, dict, list[str]]]] = defaultdict(list)
    for key, episodes in sorted(concept_to_episodes.items(), key=lambda x: -len(x[1])):
        meta = CONCEPTS.get(key, {})
        cat = meta.get("category", "Other")
        by_category[cat].append((key, meta, episodes))

    category_order = [
        "Data Loading", "Data Collection", "Data Cleaning", "Data Manipulation",
        "EDA", "Visualization", "Text Analysis", "Modeling", "Modeling Workflow",
        "Time Series", "Publishing", "Other",
    ]

    for cat in category_order:
        entries = by_category.get(cat, [])
        if not entries:
            continue
        lines += [f"## {cat}", ""]
        for key, meta, episodes in entries:
            label = meta.get("label", key.replace("_", " ").title())
            works = meta.get("works_when", [])
            fails = meta.get("fails_when", [])
            tags = meta.get("tags", [])
            ep_count = len(episodes)
            ep_sample = sorted(episodes)[:5]
            ep_rest = f" + {ep_count - 5} more" if ep_count > 5 else ""

            lines += [
                f"### {label}",
                f"**key:** `{key}`  ",
                f"**category:** {cat}  ",
                f"**episodes ({ep_count}):** " + ", ".join(f"`{e}`" for e in ep_sample) + ep_rest,
            ]
            if tags:
                lines.append(f"**tags:** " + " · ".join(f"`{t}`" for t in tags))
            lines.append("")
            if works:
                lines.append("**WORKS WHEN:**")
                for w in works:
                    lines.append(f"- {w}")
                lines.append("")
            if fails:
                lines.append("**FAILS WHEN:**")
                for f_item in fails:
                    lines.append(f"- {f_item}")
                lines.append("")
            lines.append("---")
            lines.append("")

    out = ROOT / "CONCEPT_INDEX.md"
    out.write_text("\n".join(lines), encoding="utf-8")

    total_episodes_covered = len(title_to_concepts)
    print(f"\n✓ CONCEPT_INDEX.md written")
    print(f"  {len(concept_to_episodes)} concepts across {total_episodes_covered} episodes")
    print(f"  Top 5 most common concepts:")
    for key, eps in sorted(concept_to_episodes.items(), key=lambda x: -len(x[1]))[:5]:
        meta = CONCEPTS.get(key, {})
        print(f"    {meta.get('label', key)}: {len(eps)} episodes")


if __name__ == "__main__":
    main()
