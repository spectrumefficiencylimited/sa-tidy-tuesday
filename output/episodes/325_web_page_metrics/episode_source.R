# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)
library(scales)
library(lubridate)
theme_set(theme_light())

# ---- Load ----
clean_data <- . %>%
  select(-timestamp) %>%
  mutate(date = ymd(date))

image_alt <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2022/2022-11-15/image_alt.csv') %>%
  clean_data()
color_contrast <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2022/2022-11-15/color_contrast.csv') %>%
  clean_data()
ally_scores <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2022/2022-11-15/ally_scores.csv') %>%
  clean_data()
bytes_total <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2022/2022-11-15/bytes_total.csv') %>%
  clean_data()
speed_index <- readr::read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2022/2022-11-15/speed_index.csv') %>%
  clean_data()

# ---- chunk_03 ----
image_alt %>%
  ggplot(aes(date, percent, color = client)) +
  geom_line() +
  labs(y = "% of images with alt text")

# ---- chunk_04 ----
combined_percentages <- bind_rows(image_alt,
                                  color_contrast)

combined_percentages %>%
  ggplot(aes(date, percent / 100, color = client)) +
  geom_line() +
  scale_y_continuous(labels = percent_format()) +
  labs(y = "Percentage") +
  facet_wrap(~ measure)

combined_percentiles <- bind_rows(speed_index,
                                  bytes_total,
                                  ally_scores)

combined_percentiles %>%
  ggplot(aes(date, p50, color = client)) +
  geom_line() +
  geom_ribbon(aes(ymin = p25, ymax = p75), alpha = .25) +
  facet_wrap(~ measure, scales = "free") +
  labs(y = "Median (with 25th-75th percentile)",
       color = "Client")

# ---- chunk_05 ----
library(bigrquery)

bq_project_query("bigquery-drob-screencast",
                 "SELECT * FROM `bigquery-public-data.baseball.games_wide` LIMIT 10")

# devtools::install_github("chriscardillo/dbcooper")

# Connection object
con <- DBI::dbConnect(bigrquery::bigquery(),
                      project = "bigquery-public-data",
                      dataset = "stackoverflow",
                      billing = "bigquery-drob-screencast")

library(dbcooper)
dbc_init(con, "stack")

stack_badges()

stack_query("select * from badges limit 10")
