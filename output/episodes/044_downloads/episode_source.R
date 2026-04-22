# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----
knitr::opts_chunk$set(echo = TRUE)

# ---- chunk_02 ----
library(tidyverse)
library(scales)
library(countrycode)
theme_set(theme_light())

r_downloads_year_raw <- read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-10-30/r_downloads_year.csv")

r_downloads_year <- r_downloads_year_raw %>%
  select(-X1) %>%
  mutate(country_name = countrycode(country, "iso2c", "country.name"))

# ---- chunk_03 ----
r_downloads_year %>%
  count(date) %>%
  ggplot(aes(date, n)) +
  geom_line() +
  expand_limits(y = 0) +
  labs(y = "# of R downloads per day")

library(lubridate)

r_downloads_year %>%
  count(date) %>%
  group_by(weekday = wday(date, label = TRUE)) %>%
  summarize(average = mean(n)) %>%
  ggplot(aes(weekday, average)) +
  geom_line(group = 1) +
  expand_limits(y = 0) +
  labs(y = "Average downloads per weekday")

# ---- chunk_04 ----
r_downloads_year %>%
  group_by(week = floor_date(date, "week")) %>%
  summarize(n = n_distinct(ip_id)) %>%
  filter(week > min(week)) %>%
  ggplot(aes(week, n)) +
  geom_line() +
  expand_limits(y = 0) +
  labs(y = "# of R downloads per week (distinct IPs)")

# ---- chunk_05 ----
r_downloads_year %>%
  mutate(country = countrycode(country, "iso2c", "country.name")) %>%
  filter(!is.na(country)) %>%
  count(hour = hour(time),
        country = fct_lump(country, 8)) %>%
  ggplot(aes(hour, n)) +
  geom_line() +
  expand_limits(y = 0) +
  facet_wrap(~ country, scales = "free_y")

# ---- chunk_06 ----
library(countrycode)

r_downloads_year %>%
  count(country = countrycode(country, "iso2c", "country.name"), sort = TRUE) %>%
  mutate(percent = n / sum(n)) %>%
  filter(!is.na(country)) %>%
  head(16) %>%
  mutate(country = fct_reorder(country, percent)) %>%
  ggplot(aes(country, percent)) +
  geom_col() +
  coord_flip() +
  scale_y_continuous(labels = percent_format()) +
  labs(title = "What countries install the most R?")

# ---- chunk_07 ----
r_downloads_year %>%
  mutate(version = fct_lump(version, 8)) %>%
  count(date, version) %>%
  ggplot(aes(date, n, color = version)) +
  geom_line()

# ---- chunk_08 ----
r_downloads_year %>%
  count(country = fct_lump(country, 8),
        week = floor_date(date, "week")) %>%
  filter(week > min(week)) %>%
  ggplot(aes(week, n, color = country)) +
  geom_line()

# ---- chunk_09 ----
package_downloads <- read_csv("http://cran-logs.rstudio.com/2018/2018-10-27.csv.gz")

# ---- chunk_10 ----
package_downloads %>%
  filter(country %in% c("US", "IN")) %>%
  group_by(country, package, sort = TRUE) %>%
  summarize(n = n_distinct(ip_id)) %>%
  spread(country, n, fill = 0) %>%
  ungroup() %>%
  mutate(total = US + IN,
         IN = (IN + 1) / sum(IN + 1),
         US = (US + 1) / sum(US + 1),
         ratio = US / IN) %>%
  filter(total >= 1000) %>%
  arrange((ratio)) %>%
  View()

# ---- chunk_11 ----
library(cranlogs)

cranlogs::cran_downloads(packages = c("tidyverse", "broom"), when = "last-week")

# ---- chunk_12 ----
r_download_gaps <- r_downloads_year %>%
  mutate(datetime = as.POSIXlt(date) + time) %>%
  arrange(datetime) %>%
  group_by(ip_id) %>%
  mutate(gap = as.numeric(datetime - lag(datetime))) %>%
  filter(!is.na(gap))

# ---- chunk_13 ----
ip_counts <- r_downloads_year %>%
  count(ip_id, sort = TRUE)

# ---- chunk_14 ----
r_download_gaps %>%
  ggplot(aes(gap)) +
  geom_histogram() +
  geom_vline(color = "red", lty = 2, xintercept = 86400) +
  scale_x_log10(breaks = 60 ^ (0:4),
                labels = c("Second", "Minute", "Hour", "2.5 Days", "120 Days"))

# ---- chunk_15 ----
r_download_gaps
