# Concept Index — TheDataShrink™ × TidyTuesday

DataX Stage 2/3 output: atomic reusable concepts extracted from 102 Rmd files + 410 episodes.
Each concept is independent of any single episode and reusable on any new dataset.

**Total concepts:** 64  
**Total Rmd files scanned:** 102  
**Total episodes mapped:** 79

---

## Data Loading

### TidyTuesdayR dataset loading
**key:** `tidytuesdayr_load`  
**category:** Data Loading  
**episodes (42):** `Analyzing African-American achievements in R`, `Analyzing African-American history in R`, `Analyzing Australian animal outcomes in R`, `Analyzing Beyonce and Taylor Swift lyrics in R`, `Analyzing Broadway shows in R` + 37 more
**tags:** `loading` · `tidytuesdayR`

**WORKS WHEN:**
- weekly TidyTuesday dataset with a known date string

**FAILS WHEN:**
- dataset renamed or removed from TidyTuesdayR archive
- no internet / GitHub PAT needed

---

## Data Collection

### HTML scraping with rvest
**key:** `web_scraping_rvest`  
**category:** Data Collection  
**episodes (6):** `Analyzing African-American achievements in R`, `Analyzing Australian animal outcomes in R`, `Analyzing Women's World Cup data in R`, `Analyzing extinct plants in R`, `Analyzing tidytuesday and rstats tweets in R` + 1 more
**tags:** `scraping` · `rvest` · `web`

**WORKS WHEN:**
- stable HTML table at a known URL
- supplemental reference not in flat file

**FAILS WHEN:**
- JS-rendered page (needs Playwright)
- rate-limited or auth-gated URL
- HTML structure changes

---

### World Bank WDI data enrichment
**key:** `world_bank_wdi`  
**category:** Data Collection  
**episodes (4):** `Analyzing Nobel Prize winners in R`, `Analyzing UN votes in R`, `Analyzing historical phones in R`, `Analyzing plastic waste across countries in R`
**tags:** `world bank` · `WDI` · `country` · `enrichment`

**WORKS WHEN:**
- need country-level macro indicators (GDP, population, health)
- joining on ISO country code

**FAILS WHEN:**
- indicator has missing years for key countries
- needs real-time data

---

### StatsBomb event-level soccer data
**key:** `statsboard_soccer`  
**category:** Data Collection  
**episodes (1):** `Analyzing Women's World Cup data in R`
**tags:** `soccer` · `StatsBomb` · `sports`

**WORKS WHEN:**
- event-level soccer analysis (passes, shots, xG)

**FAILS WHEN:**
- non-soccer sport
- match not in free StatsBomb dataset

---

### US Census / ACS data with tidycensus
**key:** `us_census_tidycensus`  
**category:** Data Collection  
**episodes (1):** `Analyzing government spending on kids in R`
**tags:** `census` · `tidycensus` · `USA` · `geographic`

**WORKS WHEN:**
- US geographic analysis needing demographic context
- joining to Census FIPS codes

**FAILS WHEN:**
- non-US geography
- variable codes change between Census years

---

## Data Cleaning

### Column name cleaning with janitor
**key:** `janitor_clean`  
**category:** Data Cleaning  
**episodes (12):** `Analyzing African-American achievements in R`, `Analyzing Beyonce and Taylor Swift lyrics in R`, `Analyzing Bob Ross paintings in R`, `Analyzing Chopped epiodes in R`, `Analyzing NYC restaurant inspections with R` + 7 more
**tags:** `janitor` · `cleaning` · `names`

**WORKS WHEN:**
- raw CSV with spaces, caps, or special chars in column names

**FAILS WHEN:**
- column names are already snake_case

---

### Extract numeric from dirty strings (parse_number) — 18 uses
**key:** `parse_number_dirty`  
**category:** Data Cleaning  
**episodes (8):** `Analyzing Australian animal outcomes in R`, `Analyzing Simpsons guest stars and dialogue in R`, `Analyzing Thanksgiving dinners in R`, `Analyzing Video Games in R`, `Analyzing and predicting horror movie ratings in R` + 3 more
**tags:** `parse_number` · `readr` · `numeric extraction` · `dirty data`

**WORKS WHEN:**
- column contains numbers mixed with currency symbols, commas, units (e.g. '$1,200', '45%', '3.5k')

**FAILS WHEN:**
- string has multiple numbers and you need a specific one
- locale-specific decimal separators need explicit locale argument

---

## Data Manipulation

### Reshape wide↔long with pivot_longer / pivot_wider
**key:** `pivot_reshape`  
**category:** Data Manipulation  
**episodes (44):** `Analyzing African-American achievements in R`, `Analyzing African-American history in R`, `Analyzing Animal Crossing in R`, `Analyzing Australian animal outcomes in R`, `Analyzing Beyonce and Taylor Swift lyrics in R` + 39 more
**tags:** `reshape` · `pivot` · `tidy`

**WORKS WHEN:**
- wide format with repeated column suffixes
- need one-row-per-observation for ggplot

**FAILS WHEN:**
- columns have inconsistent naming patterns without `names_pattern`
- values need type coercion first

---

### Regex-based text filter / flag with str_detect — 43 uses
**key:** `str_detect_filter`  
**category:** Data Manipulation  
**episodes (30):** `Analyzing African-American achievements in R`, `Analyzing Beyonce and Taylor Swift lyrics in R`, `Analyzing Broadway shows in R`, `Analyzing GDPR violations in R`, `Analyzing HBCU enrollment in R` + 25 more
**tags:** `str_detect` · `stringr` · `regex` · `filter` · `text`

**WORKS WHEN:**
- need to filter rows where a text column matches a pattern
- flagging rows with keyword presence

**FAILS WHEN:**
- pattern is language-specific without locale handling
- full parsing is needed (use tidytext instead of string ops)

---

### Functional iteration over lists / data frames with purrr::map
**key:** `purrr_map_iterate`  
**category:** Data Manipulation  
**episodes (25):** `Analyzing African-American achievements in R`, `Analyzing Australian animal outcomes in R`, `Analyzing Friends transcripts in R`, `Analyzing NYC restaurant inspections with R`, `Analyzing Ninja Warrior in R` + 20 more
**tags:** `purrr` · `map` · `functional` · `iteration` · `list`

**WORKS WHEN:**
- applying the same function to a list of data frames, file paths, or parameter sets

**FAILS WHEN:**
- function has side effects that depend on order
- list is very large and a vectorised function exists

---

### Unnesting list columns (unnest / separate_rows)
**key:** `unnest_list_cols`  
**category:** Data Manipulation  
**episodes (24):** `Analyzing African-American achievements in R`, `Analyzing Chopped epiodes in R`, `Analyzing GDPR violations in R`, `Analyzing NYC restaurant inspections with R`, `Analyzing Netflix titles in R` + 19 more
**tags:** `unnest` · `list columns` · `nested data`

**WORKS WHEN:**
- column contains comma-separated tags, JSON arrays, or nested lists

**FAILS WHEN:**
- list elements have inconsistent length or names

---

### Date parsing and arithmetic with lubridate
**key:** `lubridate_dates`  
**category:** Data Manipulation  
**episodes (24):** `Analyzing Animal Crossing in R`, `Analyzing Beyonce and Taylor Swift lyrics in R`, `Analyzing GDPR violations in R`, `Analyzing NYC restaurant inspections with R`, `Analyzing Netflix titles in R` + 19 more
**tags:** `lubridate` · `dates` · `time` · `parsing`

**WORKS WHEN:**
- date column is a string in a known format
- need year/month/week extraction or rounding

**FAILS WHEN:**
- ambiguous date formats (e.g. 01/02/03)
- timezone-dependent analysis without tz specification

---

### String interpolation with glue
**key:** `glue_strings`  
**category:** Data Manipulation  
**episodes (14):** `Analyzing African-American achievements in R`, `Analyzing Chopped epiodes in R`, `Analyzing Friends transcripts in R`, `Analyzing IKEA furniture in R`, `Analyzing NCAA Women's Basketball` + 9 more
**tags:** `glue` · `strings` · `labels`

**WORKS WHEN:**
- need to construct labels, titles, or text from data values

**FAILS WHEN:**
- variables contain special characters that break glue syntax

---

### Country name / code standardization with countrycode
**key:** `countrycode_standardize`  
**category:** Data Manipulation  
**episodes (8):** `Analyzing Nobel Prize winners in R`, `Analyzing UN votes in R`, `Analyzing data on R downloads`, `Analyzing global crop yields in R`, `Analyzing malaria incidence in R` + 3 more
**tags:** `countrycode` · `country` · `standardize` · `ISO`

**WORKS WHEN:**
- dataset mixes country names, ISO2, ISO3, or continent labels

**FAILS WHEN:**
- country names are very non-standard (historical names, disputed territories)

---

### Fuzzy / approximate string join
**key:** `fuzzy_join`  
**category:** Data Manipulation  
**episodes (6):** `Analyzing UN votes in R`, `Analyzing deforestation in R`, `Analyzing dolphin data in R`, `Analyzing historical phones in R`, `Analyzing malaria incidence in R` + 1 more
**tags:** `fuzzyjoin` · `join` · `strings` · `matching`

**WORKS WHEN:**
- two tables share a text key but with spelling variation
- need to join on regex pattern

**FAILS WHEN:**
- key is numeric or exact
- string distance threshold is ambiguous across rows

---

### Conditional column creation with case_when — 7 uses
**key:** `case_when_conditional_col`  
**category:** Data Manipulation  
**episodes (5):** `Analyzing Himalayan climbers in R`, `Analyzing art collections in R`, `Analyzing bike frequencies in Seattle in R`, `Analyzing employment and earnings in R`, `Analyzing tennis tournaments in R`
**tags:** `case_when` · `conditional` · `mutate` · `ifelse`

**WORKS WHEN:**
- need to create a new column with 3+ conditional branches (replaces nested ifelse)

**FAILS WHEN:**
- conditions overlap without explicit priority order (first match wins — document the intent)
- default case is omitted (produces NA silently)

---

## EDA

### Grouped summary → ggplot storytelling
**key:** `grouped_summary_ggplot`  
**category:** EDA  
**episodes (72):** `Analyzing African-American achievements in R`, `Analyzing African-American history in R`, `Analyzing Australian animal outcomes in R`, `Analyzing Beyonce and Taylor Swift lyrics in R`, `Analyzing Bob Ross paintings in R` + 67 more
**tags:** `group_by` · `summarise` · `fct_reorder` · `bar chart`

**WORKS WHEN:**
- categorical grouping variable
- want to compare means, medians, or counts across groups

**FAILS WHEN:**
- too many groups (> 20) without fct_lump or top-N filter

---

### Time series trend line visualisation
**key:** `time_series_trend`  
**category:** EDA  
**episodes (63):** `Analyzing African-American history in R`, `Analyzing Animal Crossing in R`, `Analyzing Australian animal outcomes in R`, `Analyzing Bob Ross paintings in R`, `Analyzing Broadway shows in R` + 58 more
**tags:** `time series` · `trend` · `geom_line` · `date`

**WORKS WHEN:**
- date column with regular intervals
- want to show change over time

**FAILS WHEN:**
- irregular time points inflate apparent trends
- missing periods without interpolation

---

### Faceted small multiples (facet_wrap / facet_grid)
**key:** `faceted_comparison`  
**category:** EDA  
**episodes (57):** `Analyzing African-American history in R`, `Analyzing Animal Crossing in R`, `Analyzing Australian animal outcomes in R`, `Analyzing Beyonce and Taylor Swift lyrics in R`, `Analyzing Bob Ross paintings in R` + 52 more
**tags:** `facet_wrap` · `facet_grid` · `small multiples` · `comparison`

**WORKS WHEN:**
- 2-20 groups that share the same x/y scale
- comparing panel structure across a variable

**FAILS WHEN:**
- too many facets (> 30, unreadable)
- groups have very different scales (use free scales)

---

### Multi-table join and grain alignment
**key:** `multi_table_join`  
**category:** EDA  
**episodes (39):** `Analyzing Animal Crossing in R`, `Analyzing Australian animal outcomes in R`, `Analyzing Beyonce and Taylor Swift lyrics in R`, `Analyzing Friends transcripts in R`, `Analyzing GDPR violations in R` + 34 more
**tags:** `join` · `multi-table` · `merge` · `left_join`

**WORKS WHEN:**
- multiple tables share a clean join key

**FAILS WHEN:**
- keys have case mismatch or trailing spaces without normalisation
- many-to-many join without deduplication

---

### Distribution shape with histogram / density
**key:** `geom_histogram_density`  
**category:** EDA  
**episodes (36):** `Analyzing African-American achievements in R`, `Analyzing African-American history in R`, `Analyzing Animal Crossing in R`, `Analyzing Chopped epiodes in R`, `Analyzing Himalayan climbers in R` + 31 more
**tags:** `histogram` · `density` · `distribution` · `continuous`

**WORKS WHEN:**
- continuous variable
- want to see shape (skew, bimodality, outliers)

**FAILS WHEN:**
- discrete variable with few levels (use bar chart)
- bandwidth / bins not tuned

---

### Boxplot / jitter for group distribution comparison
**key:** `boxplot_jitter`  
**category:** EDA  
**episodes (35):** `Analyzing African-American history in R`, `Analyzing Chopped epiodes in R`, `Analyzing Friends transcripts in R`, `Analyzing GDPR violations in R`, `Analyzing Himalayan climbers in R` + 30 more
**tags:** `boxplot` · `violin` · `jitter` · `distribution comparison`

**WORKS WHEN:**
- comparing distribution spread across 3-15 groups

**FAILS WHEN:**
- very unequal group sizes (median is still valid but widths mislead)
- too many outliers obscuring the box

---

### Trend smoothing with geom_smooth (loess / lm)
**key:** `geom_smooth_loess`  
**category:** EDA  
**episodes (17):** `Analyzing Friends transcripts in R`, `Analyzing IKEA furniture in R`, `Analyzing NCAA Women's Basketball`, `Analyzing Women's World Cup data in R`, `Analyzing and predicting horror movie ratings in R` + 12 more
**tags:** `geom_smooth` · `loess` · `trend` · `smoothing`

**WORKS WHEN:**
- scatter plot with noisy relationship
- want to show trend direction without parametric assumption

**FAILS WHEN:**
- very few points (loess overfits)
- trend has structural breaks that loess averages over

---

### Schema inspection and skimming (skimr / glimpse)
**key:** `skim_inspect`  
**category:** EDA  
**episodes (11):** `Analyzing Chopped epiodes in R`, `Analyzing Friends transcripts in R`, `Analyzing Super Bowl ads in R`, `Analyzing beach volleyball in R`, `Analyzing college major & income data in R` + 6 more
**tags:** `skimr` · `glimpse` · `inspection` · `EDA first step`

**WORKS WHEN:**
- first look at any new dataset
- checking for NAs, types, and distribution shape

**FAILS WHEN:**
- output is too wide for console — pipe to `kable()` for reports

---

### Correlation matrix / heatmap
**key:** `correlation_matrix`  
**category:** EDA  
**episodes (6):** `Analyzing Animal Crossing in R`, `Analyzing Friends transcripts in R`, `Analyzing NCAA Women's Basketball`, `Analyzing Super Bowl ads in R`, `Analyzing UN votes in R` + 1 more
**tags:** `correlation` · `corrplot` · `heatmap` · `multivariate`

**WORKS WHEN:**
- multiple numeric columns
- want to find candidate predictor pairs

**FAILS WHEN:**
- non-numeric columns without encoding
- correlation without checking for non-linearity

---

### Running total / cumulative sum (cumsum) — 11 uses
**key:** `cumsum_running_total`  
**category:** EDA  
**episodes (3):** `Analyzing HBCU enrollment in R`, `Analyzing Tour de France data in R`, `Analyzing tennis tournaments in R`
**tags:** `cumsum` · `running total` · `cumulative` · `time series`

**WORKS WHEN:**
- time-ordered data where cumulative growth is the story (launches, publications, cumulative cases)

**FAILS WHEN:**
- data is not time-ordered
- gaps in time series inflate apparent acceleration

---

## Visualization

### Global ggplot theme with theme_set (David Robinson default: theme_light)
**key:** `theme_set_global`  
**category:** Visualization  
**episodes (78):** `Analyzing African-American achievements in R`, `Analyzing African-American history in R`, `Analyzing Animal Crossing in R`, `Analyzing Australian animal outcomes in R`, `Analyzing Beyonce and Taylor Swift lyrics in R` + 73 more
**tags:** `theme_set` · `theme_light` · `global theme` · `ggplot` · `consistency`

**WORKS WHEN:**
- want consistent look across all plots in a script without repeating theme() on each

**FAILS WHEN:**
- individual plots need different themes — theme_set is a global side effect

---

### Log scale transformation for skewed distributions
**key:** `log_scale`  
**category:** Visualization  
**episodes (38):** `Analyzing Animal Crossing in R`, `Analyzing Beyonce and Taylor Swift lyrics in R`, `Analyzing Chopped epiodes in R`, `Analyzing European energy in R`, `Analyzing Friends transcripts in R` + 33 more
**tags:** `log scale` · `transformation` · `skew` · `power law`

**WORKS WHEN:**
- right-skewed numeric variable spanning multiple orders of magnitude
- multiplicative relationships

**FAILS WHEN:**
- zeros or negative values in data
- audience unfamiliar with log scale

---

### Horizontal bar chart with coord_flip (or native y aesthetic)
**key:** `coord_flip_horizontal`  
**category:** Visualization  
**episodes (29):** `Analyzing Bob Ross paintings in R`, `Analyzing Maryland bridges with R`, `Analyzing Medium articles with R`, `Analyzing NYC restaurant inspections with R`, `Analyzing Nobel Prize winners in R` + 24 more
**tags:** `coord_flip` · `horizontal bar` · `category labels` · `ggplot`

**WORKS WHEN:**
- long category labels that overlap on the x-axis
- ranking bars where the reader reads down rather than across

**FAILS WHEN:**
- already using y for position — just map directly to y aesthetic in newer ggplot2 versions

---

### Reorder bars within each facet (David Robinson signature)
**key:** `reorder_within_facets`  
**category:** Visualization  
**episodes (21):** `Analyzing African-American history in R`, `Analyzing Animal Crossing in R`, `Analyzing Beyonce and Taylor Swift lyrics in R`, `Analyzing Bob Ross paintings in R`, `Analyzing European energy in R` + 16 more
**tags:** `reorder_within` · `facet` · `ranking` · `bar chart` · `drlib`

**WORKS WHEN:**
- faceted bar chart where each facet has its own ranking
- showing top-N per group

**FAILS WHEN:**
- single panel plot (just use fct_reorder)
- groups are not comparable in size

---

### Human-readable axis labels with scales (label_percent, label_comma, label_dollar)
**key:** `scales_axis_labels`  
**category:** Visualization  
**episodes (18):** `Analyzing Bob Ross paintings in R`, `Analyzing Maryland bridges with R`, `Analyzing Medium articles with R`, `Analyzing Nobel Prize winners in R`, `Analyzing Thanksgiving dinners in R` + 13 more
**tags:** `scales` · `label_percent` · `label_comma` · `axis` · `formatting`

**WORKS WHEN:**
- axis shows proportions (→ percent), large numbers (→ comma), or currency (→ dollar)
- audience is non-technical and raw numbers are confusing

**FAILS WHEN:**
- precision matters and rounding in the label format obscures it

---

### Coefficient plot with error bars (broom + ggplot)
**key:** `error_bar_coef_plot`  
**category:** Visualization  
**episodes (16):** `Analyzing Himalayan climbers in R`, `Analyzing IKEA furniture in R`, `Analyzing Maryland bridges with R`, `Analyzing NYC restaurant inspections with R`, `Analyzing Netflix titles in R` + 11 more
**tags:** `error bars` · `coefficient plot` · `uncertainty` · `broom`

**WORKS WHEN:**
- model output with confidence intervals
- comparing effect sizes across groups

**FAILS WHEN:**
- intervals are asymmetric without transformation
- too many coefficients without filtering

---

### Animated chart with gganimate
**key:** `animated_transitions`  
**category:** Visualization  
**episodes (11):** `Analyzing Australian animal outcomes in R`, `Analyzing Tour de France data in R`, `Analyzing US wind data in R`, `Analyzing Women's World Cup data in R`, `Analyzing exploring US beer production in R` + 6 more
**tags:** `gganimate` · `animation` · `time` · `motion`

**WORKS WHEN:**
- strong time dimension
- story benefits from showing change in motion
- YouTube / social media context

**FAILS WHEN:**
- static report
- too many categories causing visual clutter
- render time is prohibitive

---

### Network / co-occurrence graph with ggraph + igraph
**key:** `network_graph_ggraph`  
**category:** Visualization  
**episodes (9):** `Analyzing African-American history in R`, `Analyzing Bob Ross paintings in R`, `Analyzing Chopped epiodes in R`, `Analyzing Medium articles with R`, `Analyzing Netflix titles in R` + 4 more
**tags:** `ggraph` · `igraph` · `network` · `graph` · `co-occurrence`

**WORKS WHEN:**
- pairwise relationships between entities
- co-occurrence of tokens or events
- graph data with nodes and edges

**FAILS WHEN:**
- too many nodes (> 200) without filtering
- graph is fully connected (no meaningful clusters)

---

### Non-overlapping point labels with ggrepel
**key:** `label_repulsion_ggrepel`  
**category:** Visualization  
**episodes (9):** `Analyzing X-Men comics in R`, `Analyzing cocktail recipes in R`, `Analyzing college major & income data in R`, `Analyzing employment and earnings in R`, `Analyzing global crop yields in R` + 4 more
**tags:** `ggrepel` · `labels` · `scatter` · `annotation`

**WORKS WHEN:**
- scatter plot with meaningful point labels
- up to ~30-50 labelled points

**FAILS WHEN:**
- hundreds of points (labels become unreadable)
- labels need exact positioning

---

### Heatmap with geom_tile
**key:** `heatmap_tile`  
**category:** Visualization  
**episodes (6):** `Analyzing NCAA Women's Basketball`, `Analyzing Ninja Warrior in R`, `Analyzing Super Bowl ads in R`, `Analyzing franchise revenue in R`, `Analyzing the Kenya census in R` + 1 more
**tags:** `heatmap` · `geom_tile` · `matrix` · `categorical`

**WORKS WHEN:**
- two categorical axes with a numeric fill value
- showing a matrix of relationships

**FAILS WHEN:**
- too many categories on one axis (> 30, becomes unreadable)
- continuous axes (use geom_raster)

---

### Area / stacked area chart (geom_area) for composition over time
**key:** `geom_area_stacked`  
**category:** Visualization  
**episodes (6):** `Analyzing Netflix titles in R`, `Analyzing art collections in R`, `Analyzing deforestation in R`, `Analyzing dolphin data in R`, `Analyzing post offices in R` + 1 more
**tags:** `geom_area` · `stacked area` · `composition` · `time series`

**WORKS WHEN:**
- showing how parts of a whole evolve over time
- categories are non-overlapping and sum to 100%

**FAILS WHEN:**
- many categories — lower bands are hard to read
- categories overlap (use geom_ribbon instead)

---

### Interactive chart with plotly / ggplotly
**key:** `interactive_plotly`  
**category:** Visualization  
**episodes (5):** `Analyzing African-American achievements in R`, `Analyzing Video Games in R`, `Analyzing college major & income data in R`, `Analyzing data on women in the workplace in R`, `Analyzing horror movie profits in R`
**tags:** `plotly` · `interactive` · `web` · `hover`

**WORKS WHEN:**
- web publishing context
- user needs to hover/zoom/filter
- too many points for static labels

**FAILS WHEN:**
- print / PDF output
- very large datasets slow render in browser

---

### Choropleth map with sf / geom_sf
**key:** `choropleth_sf`  
**category:** Visualization  
**episodes (5):** `Analyzing Australian animal outcomes in R`, `Analyzing caribou locations in R`, `Analyzing exploring US beer production in R`, `Analyzing squirrels in NYC in R`, `Analyzing the Kenya census in R`
**tags:** `sf` · `map` · `spatial` · `choropleth` · `geom_sf`

**WORKS WHEN:**
- region column matchable to a shapefile
- spatial distribution is the main story

**FAILS WHEN:**
- region names differ from shapefile (needs fuzzy join)
- sub-region level without matching geometry
- CRS mismatch

---

### Confidence / prediction band with geom_ribbon
**key:** `confidence_ribbon`  
**category:** Visualization  
**episodes (5):** `Analyzing Thanksgiving dinners in R`, `Analyzing US dairy consumption in R`, `Analyzing bird collisions with bootstrapping in R`, `Analyzing dolphin data in R`, `Analyzing historical phones in R`
**tags:** `ribbon` · `confidence interval` · `band` · `uncertainty`

**WORKS WHEN:**
- time series or ordered x-axis with upper/lower bounds
- model prediction intervals

**FAILS WHEN:**
- ribbon bands overlap heavily without alpha transparency
- non-ordered x axis

---

### Shiny interactive application
**key:** `shiny_app`  
**category:** Visualization  
**episodes (3):** `Analyzing Broadway shows in R`, `Analyzing GDPR violations in R`, `Analyzing exploring US beer production in R`
**tags:** `shiny` · `interactive` · `app` · `web`

**WORKS WHEN:**
- user needs to filter, select, or explore data interactively
- web publishing with server

**FAILS WHEN:**
- static report context
- no server infrastructure available

---

### Ridge / joy plot for distribution comparison (ggridges)
**key:** `ridge_joy_plot`  
**category:** Visualization  
**episodes (3):** `Analyzing IKEA furniture in R`, `Analyzing art collections in R`, `Analyzing coffee ratings in R`
**tags:** `ggridges` · `distribution` · `density` · `joy plot`

**WORKS WHEN:**
- many ordered groups with overlapping distributions
- showing how distribution shifts over time or category

**FAILS WHEN:**
- fewer than 4-5 groups (use boxplot instead)
- distributions are discrete

---

## Text Analysis

### Tidytext tokenization pipeline
**key:** `tokenization_pipeline`  
**category:** Text Analysis  
**episodes (26):** `Analyzing African-American history in R`, `Analyzing Animal Crossing in R`, `Analyzing Beyonce and Taylor Swift lyrics in R`, `Analyzing Bob Ross paintings in R`, `Analyzing European energy in R` + 21 more
**tags:** `tidytext` · `tokenize` · `NLP` · `words`

**WORKS WHEN:**
- raw text column
- want word-level frequency or sentiment analysis

**FAILS WHEN:**
- text is highly structured (JSON, code)
- non-English without custom stopwords

---

### Pairwise token correlation with widyr
**key:** `pairwise_token_correlation`  
**category:** Text Analysis  
**episodes (15):** `Analyzing Animal Crossing in R`, `Analyzing Bob Ross paintings in R`, `Analyzing Chopped epiodes in R`, `Analyzing Friends transcripts in R`, `Analyzing Medium articles with R` + 10 more
**tags:** `widyr` · `pairwise` · `correlation` · `co-occurrence`

**WORKS WHEN:**
- want to find which words appear together across documents
- seed for network graph

**FAILS WHEN:**
- very large vocabulary without filtering (memory)
- documents are very short

---

### Sparse document-term matrix for LASSO (cast_sparse)
**key:** `sparse_matrix_text`  
**category:** Text Analysis  
**episodes (8):** `Analyzing Animal Crossing in R`, `Analyzing Medium articles with R`, `Analyzing Netflix titles in R`, `Analyzing and predicting horror movie ratings in R`, `Analyzing board games and predicting ratings in R` + 3 more
**tags:** `sparse matrix` · `cast_sparse` · `LASSO` · `text features`

**WORKS WHEN:**
- large text corpus as input to penalised regression
- want LASSO to select relevant tokens

**FAILS WHEN:**
- corpus is small (dense matrix is fine)
- tokens need preprocessing first

---

### Log-odds ratio for group vocabulary contrast (tidylo)
**key:** `log_odds_ratio`  
**category:** Text Analysis  
**episodes (5):** `Analyzing Beyonce and Taylor Swift lyrics in R`, `Analyzing Friends transcripts in R`, `Analyzing Netflix titles in R`, `Analyzing Ninja Warrior in R`, `Analyzing the Great American Beer Festival`
**tags:** `log-odds` · `tidylo` · `text` · `contrast`

**WORKS WHEN:**
- two groups with token counts
- want statistically grounded vocabulary contrast

**FAILS WHEN:**
- groups not mutually exclusive
- token counts near zero (Jeffreys prior needed)

---

### TF-IDF group comparison
**key:** `tf_idf_comparison`  
**category:** Text Analysis  
**episodes (4):** `Analyzing Beyonce and Taylor Swift lyrics in R`, `Analyzing Simpsons guest stars and dialogue in R`, `Analyzing ratings and scripts from The Office in R`, `Analyzing tidytuesday and rstats tweets in R`
**tags:** `tf-idf` · `text` · `comparison` · `distinctive words`

**WORKS WHEN:**
- multiple groups with text documents
- find distinctive vocabulary per group

**FAILS WHEN:**
- corpus is tiny (< 100 docs)
- groups very unequal in size without normalisation

---

### Structural topic model (stm)
**key:** `structural_topic_model`  
**category:** Text Analysis  
**episodes (1):** `Analyzing Animal Crossing in R`
**tags:** `stm` · `topic model` · `LDA` · `themes`

**WORKS WHEN:**
- large corpus (> 500 docs)
- want to discover latent themes with metadata covariates

**FAILS WHEN:**
- small corpus (< 200 docs)
- documents are very short (< 20 words)

---

## Modeling

### Spline regression for non-linear smoothing (splines::ns)
**key:** `spline_regression`  
**category:** Modeling  
**episodes (79):** `Analyzing African-American achievements in R`, `Analyzing African-American history in R`, `Analyzing Animal Crossing in R`, `Analyzing Australian animal outcomes in R`, `Analyzing Beyonce and Taylor Swift lyrics in R` + 74 more
**tags:** `splines` · `ns` · `non-linear` · `smoothing`

**WORKS WHEN:**
- known non-linear relationship (e.g. age effects, seasonal curves)
- want smooth curve in lm/glm framework

**FAILS WHEN:**
- too few data points to fit the knots
- knot placement is not principled

---

### Linear model with broom output tidying
**key:** `linear_model_broom`  
**category:** Modeling  
**episodes (25):** `Analyzing Bob Ross paintings in R`, `Analyzing Chopped epiodes in R`, `Analyzing Friends transcripts in R`, `Analyzing Himalayan climbers in R`, `Analyzing IKEA furniture in R` + 20 more
**tags:** `lm` · `linear model` · `broom` · `regression`

**WORKS WHEN:**
- continuous numeric outcome
- want interpretable coefficients
- checking linear assumptions

**FAILS WHEN:**
- outcome is binary or count (use glm)
- strong non-linearity without splines

---

### LASSO / Ridge regression with glmnet (cross-validated)
**key:** `lasso_glmnet`  
**category:** Modeling  
**episodes (7):** `Analyzing Medium articles with R`, `Analyzing Netflix titles in R`, `Analyzing and predicting horror movie ratings in R`, `Analyzing board games and predicting ratings in R`, `Analyzing predicting wine ratings in R` + 2 more
**tags:** `glmnet` · `LASSO` · `regularisation` · `feature selection`

**WORKS WHEN:**
- many predictors (especially sparse text features)
- want automatic feature selection

**FAILS WHEN:**
- features are highly correlated in groups (use elastic net or group lasso)
- need non-linear relationships

---

### Logistic regression (glm binomial)
**key:** `logistic_regression`  
**category:** Modeling  
**episodes (6):** `Analyzing Himalayan climbers in R`, `Analyzing Maryland bridges with R`, `Analyzing Super Bowl ads in R`, `Analyzing squirrels in NYC in R`, `Analyzing the Great American Beer Festival` + 1 more
**tags:** `glm` · `logistic` · `binary` · `classification`

**WORKS WHEN:**
- binary outcome
- interpretable log-odds needed
- small-to-medium dataset

**FAILS WHEN:**
- severe class imbalance without weighting
- many dummy features (use LASSO instead)

---

### Tidymodels cross-validation pipeline (vfold + tune_grid)
**key:** `tidymodels_cv`  
**category:** Modeling  
**episodes (3):** `Analyzing Chopped epiodes in R`, `Analyzing penguins in R`, `Analyzing wealth and income in R`
**tags:** `tidymodels` · `cross-validation` · `tune` · `workflow`

**WORKS WHEN:**
- tabular data with clear outcome
- comparing multiple model specs with hyperparameter tuning

**FAILS WHEN:**
- time series (needs sliding window CV)
- very small datasets (< 200 rows, too few folds)

---

### Empirical Bayes estimation for proportions (ebbr)
**key:** `empirical_bayes`  
**category:** Modeling  
**episodes (2):** `Analyzing Himalayan climbers in R`, `Analyzing Thanksgiving dinners in R`
**tags:** `ebbr` · `empirical Bayes` · `shrinkage` · `proportion`

**WORKS WHEN:**
- proportion outcome with wildly varying sample sizes per group
- want to shrink noisy small-sample estimates toward the global mean

**FAILS WHEN:**
- all groups have large sample sizes (shrinkage is negligible)
- prior is clearly wrong

---

### Survival / time-to-event analysis (survival package)
**key:** `survival_analysis`  
**category:** Modeling  
**episodes (2):** `Analyzing Tour de France data in R`, `Analyzing dolphin data in R`
**tags:** `survival` · `Surv` · `Kaplan-Meier` · `time-to-event`

**WORKS WHEN:**
- time-to-event outcome with censoring (did not observe event)

**FAILS WHEN:**
- no censoring indicator
- competing risks without cause-specific adjustment

---

### Bootstrap confidence intervals (rsample::bootstraps)
**key:** `bootstrap_ci`  
**category:** Modeling  
**episodes (1):** `Analyzing bird collisions with bootstrapping in R`
**tags:** `bootstrap` · `rsample` · `confidence interval` · `uncertainty`

**WORKS WHEN:**
- want distribution-free uncertainty estimates for any statistic

**FAILS WHEN:**
- time-dependent data without block bootstrap
- n < 30

---

## Modeling Workflow

### Model output tidying with broom (tidy / glance / augment)
**key:** `broom_model_output`  
**category:** Modeling Workflow  
**episodes (7):** `Analyzing Animal Crossing in R`, `Analyzing Bob Ross paintings in R`, `Analyzing Medium articles with R`, `Analyzing Tour de France data in R`, `Analyzing and predicting horror movie ratings in R` + 2 more
**tags:** `broom` · `tidy` · `model output` · `coefficients`

**WORKS WHEN:**
- any base R model (lm, glm, survival, etc.)
- want ggplot-ready model output

**FAILS WHEN:**
- model class not supported by broom (check broom::tidy methods)

---

## Time Series

### Rolling window aggregation (tidymetrics / slider)
**key:** `rolling_window_metrics`  
**category:** Time Series  
**episodes (4):** `Analyzing Broadway shows in R`, `Analyzing GDPR violations in R`, `Analyzing US dairy consumption in R`, `Analyzing exploring US beer production in R`
**tags:** `rolling window` · `tidymetrics` · `timetk` · `moving average`

**WORKS WHEN:**
- regular time series needing moving average or rolling sum

**FAILS WHEN:**
- irregular time intervals without imputation first

---

### Time series decomposition and forecasting (sweep / fable)
**key:** `time_series_forecast`  
**category:** Time Series  
**episodes (1):** `Analyzing US dairy consumption in R`
**tags:** `forecast` · `sweep` · `fable` · `ARIMA` · `ETS`

**WORKS WHEN:**
- regular time series with enough history (> 2 seasonal cycles)

**FAILS WHEN:**
- very short series
- structural breaks in the series

---
