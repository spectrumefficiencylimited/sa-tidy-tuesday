# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)
theme_set(theme_light())
library(scales)

# ---- Load ----

tt <- tt_load("2021-02-02")

hbcu_all_long <- tt$hbcu_all %>%
  gather(metric, enrollment, -Year) %>%
  rename(year = Year)

hbcu_all_long %>%
  filter(str_detect(metric, " - ")) %>%
  separate(metric, c("degree_length", "type"), sep = " - ") %>%
  filter(degree_length != "Total") %>%
  ggplot(aes(year, enrollment, color = type)) +
  geom_line() +
  facet_wrap(~ degree_length) +
  labs(y = "# enrolled in HBCU",
       color = "")

hbcu_all_long %>%
  filter(metric %in% c("Males", "Females")) %>%
  ggplot(aes(year, enrollment, color = metric)) +
  geom_line() +
  expand_limits(y = 0) +
  labs(y = "# enrolled in HBCU",
       color = "")

# ---- chunk_03 ----
hbcu_black_long <- tt$hbcu_black %>%
  gather(metric, black_enrollment, -Year) %>%
  rename(year = Year)

hbcu_compare_long <- hbcu_all_long %>%
  full_join(hbcu_black_long, by = c("year", "metric")) %>%
  mutate(pct_black = black_enrollment / enrollment)

hbcu_compare_long %>%
  filter(metric == "Total enrollment") %>%
  ggplot(aes(year, pct_black)) +
  geom_line() +
  scale_y_continuous(labels = percent) +
  expand_limits(y = 0) +
  labs(y = "% of HBCU enrollment that is Black")


hbcu_compare_long %>%
  filter(metric %in% c("Males", "Females")) %>%
  ggplot(aes(year, pct_black, color = metric)) +
  geom_line() +
  scale_y_continuous(labels = percent) +
  expand_limits(y = 0) +
  labs(y = "% of HBCU enrollment that is Black")

hbcu_compare_long %>%
  filter(str_detect(metric, "Total -")) %>%
  mutate(metric = str_remove(metric, "Total - ")) %>%
  ggplot(aes(year, pct_black, color = metric)) +
  geom_line() +
  scale_y_continuous(labels = percent) +
  expand_limits(y = 0) +
  labs(y = "% of HBCU enrollment that is Black",
       color = "")

# ---- chunk_04 ----
gather_race_ethnicity <- function(tbl) {
  tbl %>%
    mutate_if(is.character, parse_number) %>%
    rename(year = Total) %>%
    filter(!is.na(year)) %>%
    gather(race_ethnicity, value, -year) %>%
    mutate(column = ifelse(str_detect(race_ethnicity, "Standard Errors - "), "standard_error", "percent"),
           race_ethnicity = str_remove(race_ethnicity, "Standard Errors - ")) %>%
    spread(column, value) %>%
    mutate(standard_error = abs(standard_error)) %>%
    filter(!is.na(percent)) %>%
    mutate(race_ethnicity = str_remove(race_ethnicity, "1$"),
           percent = percent / 100,
           standard_error = standard_error / 100)
}

hs_over_time <- tt$hs_students %>%
  slice(-(1:3)) %>%
  gather_race_ethnicity()

bach_over_time <- tt$bach_students %>%
  gather_race_ethnicity()

education_over_time <- bind_rows(hs_over_time %>% mutate(degree = "High School"),
                                 bach_over_time %>% mutate(degree = "Bachelor's"))

hs_over_time %>%
  mutate(race_ethnicity = fct_reorder(race_ethnicity, -percent)) %>%
  ggplot(aes(year, percent, color = race_ethnicity)) +
  geom_line() +
  scale_y_continuous(labels = percent) +
  labs(color = "Race/ethnicity",
       y = "% of people aged >=25 who graduated HS") +
  expand_limits(y = 0)

bach_over_time %>%
  mutate(race_ethnicity = fct_reorder(race_ethnicity, -percent)) %>%
  ggplot(aes(year, percent, color = race_ethnicity)) +
  geom_line() +
  scale_y_continuous(labels = percent) +
  labs(color = "Race/ethnicity",
       y = "% of people aged >=25 who graduated a bachelor's program") +
  expand_limits(y = 0)

education_over_time %>%
  filter(year >= 1940,
         !str_detect(race_ethnicity, "Islander -")) %>%
  mutate(degree = fct_relevel(degree, "High School"),
         race_ethnicity = str_remove(race_ethnicity, "Total - ")) %>%
  mutate(race_ethnicity = fct_reorder(race_ethnicity, percent, last, .desc = TRUE)) %>%
  ggplot(aes(year, percent, color = race_ethnicity)) +
  geom_line() +
  facet_wrap(~ degree) +
  scale_y_continuous(labels = percent) +
  labs(x = "Year",
       color = "Race/ethnicity",
       y = "% of people aged >=25 who have this degree") +
  expand_limits(y = 0)

# ---- chunk_05 ----
a25 <- readxl::read_excel("~/Downloads/A-25.xls")

a25_cleaned <- a25 %>%
  select(-starts_with("...")) %>%
  rename(field_gender = 1) %>%
  mutate(group = cumsum(is.na(field_gender))) %>%
  filter(!is.na(field_gender)) %>%
  select(group, everything()) %>%
  mutate(field_gender = str_remove(field_gender, " \\.\\.\\..*")) %>%
  group_by(group) %>%
  mutate(field = first(field_gender),
         gender = ifelse(field_gender %in% c("Men", "Women"), field_gender, "Total")) %>%
  ungroup() %>%
  select(field, gender, everything()) %>%
  select(-field_gender, -group)

a25_cleaned %>%
  select(field, gender, contains("HBCU")) %>%
  rename(pct_hbcu_total = 3,
         pct_hbcu_black = 4) %>%
  filter(gender != "Total") %>%
  mutate(field = fct_reorder(field, pct_hbcu_black, na.rm = TRUE),
         pct_hbcu_black = pct_hbcu_black / 100) %>%
  ggplot(aes(pct_hbcu_black, field, fill = gender)) +
  geom_col(position = "dodge") +
  scale_x_continuous(labels = percent) +
  labs(x = "% of first degrees from an HBCU, among Black students",
       y = "Field",
       fill = "")
