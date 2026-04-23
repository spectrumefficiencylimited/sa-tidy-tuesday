# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----
knitr::opts_chunk$set(echo = TRUE)

# ---- chunk_02 ----
library(tidyverse)
library(lubridate)
library(scales)
theme_set(theme_light())

# ---- chunk_03 ----
movie_profit_raw <- read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-10-23/movie_profit.csv")

# ---- chunk_04 ----
# Data cleaning
movie_profit <- movie_profit_raw %>%
  select(-X1) %>%
  mutate(release_date = as.Date(parse_date_time(release_date, "%m!/%d/%Y"))) %>%
  filter(release_date < "2018-01-01") %>%
  arrange(desc(row_number())) %>%
  distinct(movie, release_date, .keep_all = TRUE) %>%
  mutate(distributor = fct_lump(distributor, 5)) %>%
  filter(worldwide_gross > 0) %>%
  mutate(profit_ratio = worldwide_gross / production_budget,
         decade = 10 * floor(year(release_date) / 10))

# ---- chunk_05 ----
movie_profit %>%
  count(distributor, sort = TRUE)

movie_profit %>%
  ggplot(aes(production_budget)) +
  geom_histogram() +
  scale_x_log10(labels = dollar_format())

movie_profit %>%
  ggplot(aes(distributor, production_budget)) +
  geom_boxplot() +
  scale_y_log10(labels = dollar_format()) +
  coord_flip()

# ---- chunk_06 ----
movie_profit %>%
  ggplot(aes(distributor, worldwide_gross)) +
  geom_boxplot() +
  scale_y_log10(labels = dollar_format()) +
  coord_flip()

# ---- chunk_07 ----
movie_profit %>%
  mutate(genre = fct_reorder(genre, production_budget)) %>%
  filter(!is.na(distributor)) %>%
  ggplot(aes(genre, production_budget)) +
  geom_boxplot() +
  scale_y_log10(labels = dollar_format()) +
  coord_flip() +
  facet_wrap(~ distributor)

# ---- chunk_08 ----
movie_profit %>%
  mutate(genre = fct_reorder(genre, worldwide_gross)) %>%
  filter(!is.na(distributor)) %>%
  ggplot(aes(genre, worldwide_gross)) +
  geom_boxplot() +
  scale_y_log10(labels = dollar_format()) +
  coord_flip() +
  facet_wrap(~ distributor)

# ---- chunk_09 ----
movie_profit %>%
  arrange(desc(profit_ratio)) %>%
  head(20) %>%
  mutate(movie = fct_reorder(movie, profit_ratio)) %>%
  ggplot(aes(movie, profit_ratio, fill = genre)) +
  geom_col() +
  coord_flip() +
  scale_y_continuous(labels = function(x) paste0(x, "X")) +
  labs(x = "",
       y = "Ratio of worldwide gross to production budget",
       title = "What movies have most outgrossed their budget?",
       fill = "Genre")

# ---- chunk_10 ----
movie_profit %>%
  count(decade, genre) %>%
  group_by(decade) %>%
  mutate(percent = n / sum(n)) %>%
  ggplot(aes(decade, percent, color = genre)) +
  geom_line() +
  scale_y_continuous(labels = percent_format())

# ---- chunk_11 ----
movie_profit %>%
  filter(!is.na(distributor)) %>%
  count(distributor, genre) %>%
  ggplot(aes(genre, n, fill = genre)) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ distributor, scales = "free_x") +
  coord_flip()

# ---- chunk_12 ----
movie_profit %>%
  group_by(genre) %>%
  summarize(median_profit_ratio = median(profit_ratio)) %>%
  arrange(desc(median_profit_ratio)) %>%
  mutate(genre = fct_reorder(genre, median_profit_ratio)) %>%
  ggplot(aes(genre, median_profit_ratio)) +
  geom_col() +
  scale_y_continuous(labels = function(x) paste0(x, "X")) +
  coord_flip()

# ---- chunk_13 ----
movie_profit %>%
  group_by(genre, year = year(release_date)) %>%
  summarize(median_profit_ratio = median(profit_ratio),
            movies = n()) %>%
  ungroup() %>%
  filter(year >= 2000) %>%
  arrange(desc(median_profit_ratio)) %>%
  mutate(genre = fct_reorder(genre, median_profit_ratio)) %>%
  ggplot(aes(year, median_profit_ratio, color = genre)) +
  geom_line() +
  scale_y_continuous(labels = function(x) paste0(x, "X"))

# ---- horror_movies ----
horror_movies <- movie_profit %>%
  filter(genre == "Horror") %>%
  arrange(desc(profit_ratio))

# ---- chunk_15 ----
horror_movies %>%
  head(20) %>%
  mutate(movie = paste0(movie, " (", year(release_date), ")"),
         movie = fct_reorder(movie, profit_ratio)) %>%
  ggplot(aes(movie, profit_ratio, fill = distributor)) +
  geom_col() +
  coord_flip() +
  scale_y_continuous(labels = function(x) paste0(x, "X")) +
  labs(x = "",
       y = "Ratio of worldwide gross to production budget",
       title = "What horror movies have most outgrossed their budget?")

# ---- chunk_16 ----
horror_movies %>%
  filter(release_date >= "1990-01-01",
         profit_ratio >= .01) %>%
  ggplot(aes(release_date, profit_ratio)) +
  geom_point() +
  geom_smooth(method = "lm") +
  geom_text(aes(label = movie), vjust = 1, hjust = 1, check_overlap = TRUE) +
  scale_y_log10(labels = function(x) paste0(x, "X"), breaks = c(.1, 1, 10, 100))

# ---- chunk_17 ----
g <- movie_profit %>%
  filter(release_date >= "1990-01-01",
         profit_ratio >= .01) %>%
  ggplot(aes(release_date, profit_ratio, label = movie)) +
  geom_point() +
  geom_smooth(method = "lm") +
  scale_y_log10(labels = function(x) paste0(x, "X"), breaks = c(.1, 1, 10, 100)) +
  facet_wrap(~ genre)

library(plotly)

ggplotly(g)

# ---- chunk_18 ----
movie_profit %>%
  group_by(genre, distributor, decade) %>%
  summarize(median_profit_ratio = median(profit_ratio),
            movies = n()) %>%
  ungroup() %>%
  filter(decade >= 1990,
         !is.na(distributor)) %>%
  arrange(movies)
  mutate(genre = fct_reorder(genre, median_profit_ratio)) %>%
  ggplot(aes(decade, median_profit_ratio, color = genre)) +
  geom_line() +
  facet_wrap(~ distributor) +
  scale_y_continuous(labels = function(x) paste0(x, "X"))

# ---- chunk_19 ----
movie_profit %>%
  group_by(decade) %>%
  summarize_at(vars(production_budget:worldwide_gross), median, na.rm = TRUE) %>%
  gather(metric, value, -decade) %>%
  ggplot(aes(decade, value, color = metric)) +
  geom_line() +
  scale_y_continuous(labels = dollar_format())
