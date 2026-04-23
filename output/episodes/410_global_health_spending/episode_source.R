# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)
library(scales)
theme_set(theme_light())

# ---- Load ----

tt <- tt_load("2026-04-21")

financing_schemes <- tt$financing_schemes
health_spending    <- tt$health_spending
spending_purpose   <- tt$spending_purpose

# ---- chunk_03 ----
health_spending %>%
  glimpse()

financing_schemes %>%
  glimpse()

spending_purpose %>%
  glimpse()

# ---- chunk_04 ----
