# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----
knitr::opts_chunk$set(echo = TRUE)

# ---- chunk_02 ----
library(tidyverse)
library(scales)
theme_set(theme_light())

maryland_bridges <- read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-11-27/baltimore_bridges.csv") %>%
  select(-vehicles) %>%
  mutate(inspection_yr = inspection_yr + 2000,
         decade = 10 * (yr_built %/% 10),
         responsibility = fct_lump(responsibility, 4),
         county = str_to_title(county))

# ---- chunk_03 ----
maryland_bridges %>%
  filter(yr_built >= 1900) %>%
  count(decade = 10 * (yr_built %/% 10), sort = TRUE) %>%
  ggplot(aes(decade, n)) +
  geom_line() +
  expand_limits(y = 0) +
  labs(y = "# of bridges in Baltimore built this decade")

# ---- chunk_04 ----
maryland_bridges %>%
  filter(yr_built >= 1900) %>%
  group_by(decade) %>%
  summarize(pct_good = mean(bridge_condition == "Good"),
            total = n()) %>%
  ggplot(aes(decade, pct_good)) +
  geom_line() +
  scale_y_continuous(labels = percent_format()) +
  expand_limits(y = 0)

# ---- chunk_05 ----
maryland_bridges %>%
  replace_na(list(responsibility = "Other")) %>%
  count(responsibility = fct_lump(responsibility, 4), sort = TRUE) %>%
  mutate(responsibility = fct_reorder(responsibility, n)) %>%
  ggplot(aes(responsibility, n)) +
  geom_col() +
  coord_flip()

# ---- chunk_06 ----
maryland_bridges %>%
  filter(yr_built >= 1900) %>%
  group_by(responsibility = fct_lump(responsibility, 4),
           decade) %>%
  summarize(pct_good = mean(bridge_condition == "Good"),
            total = n()) %>%
  filter(responsibility != "Other") %>%
  ggplot(aes(decade, pct_good, color = responsibility)) +
  geom_line() +
  scale_y_continuous(labels = percent_format()) +
  expand_limits(y = 0) +
  labs(y = "% of bridges rated 'Good'")

# ---- chunk_07 ----
maryland_bridges %>%
  ggplot(aes(avg_daily_traffic)) +
  geom_histogram() +
  scale_x_log10(labels = comma_format())

# ---- chunk_08 ----
maryland_bridges %>%
  filter(yr_built >= 1990) %>%
  group_by(traffic_category = cut(avg_daily_traffic, c(0, 1000, 10000, Inf),
                                  labels = c("<1000", "1000-10,000", "10,000+"))) %>%
  summarize(pct_good = mean(bridge_condition == "Good"),
            total = n())

# ---- chunk_09 ----
maryland_bridges %>%
  ggplot(aes(long, lat, color = avg_daily_traffic)) +
  borders("state", regions = "Maryland") +
  geom_point() +
  scale_color_gradient2(low = "blue",
                        high = "red",
                        midpoint = log10(median(maryland_bridges$avg_daily_traffic)),
                        trans = "log10",
                        labels = comma_format()) +
  coord_map() +
  theme_void()

# ---- chunk_10 ----
maryland_bridges %>%
  ggplot(aes(long, lat, color = bridge_condition)) +
  borders("state", regions = "Maryland") +
  geom_point(size = 1) +
  coord_map() +
  theme_void()

# ---- chunk_11 ----
maryland_bridges %>%
  filter(yr_built >= 1900) %>%
  ggplot(aes(long, lat, color = county)) +
  borders("state", regions = "Maryland") +
  geom_point(size = 1) +
  coord_map() +
  theme_void()

# ---- chunk_12 ----
maryland_bridges %>%
  filter(yr_built >= 1900) %>%
  group_by(county, decade) %>%
  summarize(pct_good = mean(bridge_condition == "Good"),
            total = n()) %>%
  arrange(county, decade) %>%
  ggplot(aes(decade, pct_good, color = county)) +
  geom_line() +
  scale_y_continuous(labels = percent_format()) +
  expand_limits(y = 0) +
  labs(y = "% of bridges rated 'Good'")

# ---- chunk_13 ----
# fit a logistic model
bridges <- maryland_bridges %>%
  filter(yr_built >= 1900)

library(broom)
library(splines)

simple_model <- bridges %>%
  mutate(good = bridge_condition == "Good") %>%
  glm(good ~ ns(yr_built, 4), data = ., family = "binomial")

model <- bridges %>%
  mutate(good = bridge_condition == "Good") %>%
  glm(good ~ ns(yr_built, 4) + responsibility + county, data = ., family = "binomial")

augment(simple_model, bridges, type.predict = "response") %>%
  ggplot(aes(yr_built, .fitted)) +
  geom_line() +
  expand_limits(y = 0) +
  scale_y_continuous(labels = percent_format()) +
  labs(y = "Predicted probability a bridge is rated 'Good'")

augment(model, bridges, type.predict = "response") %>%
  ggplot(aes(yr_built, .fitted, color = responsibility)) +
  geom_line() +
  expand_limits(y = 0) +
  facet_wrap(~ county) +
  scale_y_continuous(labels = percent_format()) +
  labs(y = "Predicted probability a bridge is rated 'Good'")

# ---- chunk_14 ----
model %>%
  tidy(conf.int = TRUE) %>%
  filter(str_detect(term, "responsibility|county")) %>%
  mutate(term = reorder(term, estimate)) %>%
  ggplot(aes(estimate, term)) +
  geom_point() +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high)) +
  geom_vline(xintercept = 0, color = "red", lty = 2)
