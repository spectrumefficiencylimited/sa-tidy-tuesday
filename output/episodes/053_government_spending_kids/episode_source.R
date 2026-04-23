# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----
knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)
library(scales)
theme_set(theme_light())

# ---- Load ----
tt <- tt_load("2020-09-15")

kids <- tt$kids

# ---- chunk_03 ----
library(ggthemes)

kids %>%
  filter(variable == "PK12ed") %>%
  group_by(year) %>%
  summarize(total = 1000 * sum(inf_adj)) %>%
  ggplot(aes(year, total)) +
  geom_line() +
  expand_limits(y = 0) +
  scale_y_continuous(labels = dollar)

kids %>%
  filter(variable == "PK12ed") %>%
        # state %in% sample(unique(state), 20)) %>%
  mutate(state = fct_reorder(state, inf_adj_perchild, max, .desc = TRUE)) %>%
  ggplot(aes(year, 1000 * inf_adj_perchild)) +
  geom_line() +
  geom_vline(xintercept = 2009, color = "red", lty = 2) +
  scale_y_continuous(labels = dollar) +
  expand_limits(y = 0) +
  facet_wrap(~ state) +
  theme_tufte() +
  labs(x = "Year",
       y = "Inflation-adjusted spending per child")

plot_faceted <- function(tbl, y_axis) {
  tbl %>%
    mutate(state = fct_reorder(state, {{ y_axis }}, max, .desc = TRUE)) %>%
    ggplot(aes(year, {{ y_axis }})) +
    geom_hline(yintercept = 0, color = "gray") +
    geom_line() +
    facet_wrap(~ state)
}

plot_change_faceted <- function(tbl) {
  tbl %>%
    group_by(state, variable) %>%
    mutate(change = inf_adj_perchild / first(inf_adj_perchild) - 1) %>%
    ungroup() %>%
    plot_faceted(change) +
    scale_y_continuous(labels = percent)
}

# ---- chunk_04 ----
theme_set(theme_tufte())

kids %>%
  filter(variable == "PK12ed") %>%
  plot_faceted(inf_adj_perchild * 1000) +
  geom_vline(xintercept = 2009, color = "red", lty = 2) +
  scale_y_continuous(labels = dollar_format()) +
  labs(x = "",
       y = "Inflation-adjusted spending per child relative to 1997",
       title = "How has per-student K-12 spending changed per state?",
       subtitle = "Red line shows 2009 (global financial crisis)")

kids %>%
  filter(variable == "PK12ed") %>%
  plot_change_faceted() +
  geom_vline(xintercept = 2009, color = "red", lty = 2) +
  labs(x = "",
       y = "Increase in inflation-adjusted spending per child relative to 1997",
       title = "How has per-student K-12 spending changed per state?",
       subtitle = "Red line shows 2009 (global financial crisis)")

kids %>%
  filter(variable == "highered") %>%
  plot_faceted(inf_adj_perchild * 1000) +
  labs(y = "Spending per child")

kids %>%
  filter(variable == "highered") %>%
  plot_change_faceted() +
  labs(x = "",
       y = "Increase in inflation-adjusted spending per child relative to 1997",
       title = "How has higher education spending changed per state?",
       subtitle = "Red line shows 2009 (global financial crisis)")

# ---- chunk_05 ----
kids %>%
  filter(year == 2016,
         variable %in% c("PK12ed", "highered")) %>%
  arrange(desc(inf_adj_perchild)) %>%
  mutate(state = fct_reorder(state, inf_adj_perchild, max)) %>%
  ggplot(aes(inf_adj_perchild * 1000, state, fill = variable)) +
  geom_col(position = "dodge") +
  scale_x_continuous(labels = dollar) +
  labs(x = "Spending on K-12 per child in 2016") +
  scale_fill_discrete(guide = guide_legend(reverse = TRUE))

# ---- chunk_06 ----
library(widyr)

kids %>%
  filter(year == 2016,
         variable %in% c("PK12ed", "highered")) %>%
  pivot_wider(names_from = variable, values_from = raw:inf_adj_perchild) %>%
  ggplot(aes(inf_adj_perchild_PK12ed, inf_adj_perchild_highered)) +
  geom_point() +
  geom_text(aes(label = state), vjust = 1, hjust = 1) +
  scale_x_continuous(labels = dollar) +
  scale_y_continuous(labels = dollar) +
  labs(x = "K-12 spending per child (2016)",
       y = "Higher ed spending per child (2016)") +
  expand_limits(y = 0, x = 0)

kids %>%
  filter(year == 2016) %>%
  pairwise_cor(variable, state, inf_adj_perchild, sort = TRUE) %>%
  filter(item1 == "PK12ed") %>%
  mutate(item2 = fct_reorder(item2, correlation)) %>%
  ggplot(aes(correlation, item2)) +
  geom_col() +
  labs(y = "Spending metric",
       x = "Correlation with K-12 education spending")

# ---- chunk_07 ----
read_custom <- function(filename) {
  read_csv(filename) %>%
    mutate(across(starts_with("20"), as.numeric))
}

gdp_by_state_raw <- dir("~/Downloads/SQGDP/", pattern = "SQGDP2.*.csv", full.names = TRUE) %>%
  set_names(.) %>%
  map_df(read_custom, .id = "filename")

by_year_state_gdp <- read_csv("~/Downloads/SQGDP/SQGDP1__ALL_AREAS_2005_2020.csv") %>%
  pivot_longer(cols = starts_with("20"),
               names_to = "year_quarter",
               values_to = "gdp_millions") %>%
  separate(year_quarter, c("year", "quarter"), sep = ":", convert = TRUE) %>%
  group_by(state = GeoName, year, Description) %>%
  summarize(gdp_millions = sum(gdp_millions))

# ---- chunk_08 ----
library(tidycensus)

# ---- chunk_09 ----
# Extra credit! (Don't pay attention to this)
gdp_by_state_raw %>%
  filter(Description == "All industry total") %>%
  pivot_longer(cols = starts_with("20"),
               names_to = "year_quarter",
               values_to = "gdp_millions") %>%
  separate(year_quarter, c("year", "quarter"), sep = ":", convert = TRUE) %>%
  extract(filename, "state", "SQGDP2_(.*?)_20") %>%
  filter(str_length(state) == 2) %>%
  group_by(state, year) %>%
  summarize(gdp_millions = sum(gdp_millions))
