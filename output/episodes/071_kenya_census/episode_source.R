# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)
theme_set(theme_light())
library(scales)
library(janitor)

# ---- Load ----
tt <- tt_load("2021-01-19")

gender <- tt$gender %>%
  clean_names()

respace <- function(x) {
  str_replace_all(x, "([a-z])([A-Z])", "\\1 \\2")
}

households <- tt$households %>%
  clean_names() %>%
  mutate(county = str_trim(county)) %>%
  mutate(county = respace(county))

# ---- chunk_03 ----
gender %>%
  filter(county != "Total") %>%
  mutate(county = fct_reorder(county, total)) %>%
  ggplot(aes(total, county)) +
  geom_col() +
  scale_x_continuous(labels = comma)

gender %>%
  filter(county != "Total") %>%
  gather(gender, population, male, female, intersex) %>%
  mutate(gender = str_to_title(gender)) %>%
  mutate(county = fct_reorder(county, total, sum)) %>%
  ggplot(aes(population, county, fill = gender)) +
  geom_col() +
  scale_x_continuous(labels = comma)

gender %>%
  filter(county != "Total") %>%
  mutate(pct_male = male / total) %>%
  arrange(desc(pct_male)) %>%
  ggplot(aes(total, pct_male)) +
  geom_point() +
  geom_text(aes(label = county),
            vjust = 1, hjust = 1) +
  geom_hline(color = "red", yintercept = .5) +
  scale_y_continuous(labels = percent)

# ---- chunk_04 ----
households %>%
  filter(county != "Kenya") %>%
  arrange(desc(average_household_size)) %>%
  ggplot(aes(population, average_household_size)) +
  geom_point() +
  geom_text(aes(label = county),
            vjust = 1, hjust = 1) +
  scale_x_log10(labels = comma) +
  expand_limits(y = 0)
  # geom_hline(color = "red", yintercept = .5) +
  scale_y_continuous(labels = percent)

# ---- chunk_05 ----
crop_counties <- tt$crops %>%
  gather(crop, households, -SubCounty, -Farming) %>%
  filter(!is.na(households)) %>%
  mutate(county = str_to_title(SubCounty)) %>%
  filter(county != "Kenya") %>%
  select(-SubCounty) %>%
  inner_join(households, by = "county") %>%
  mutate(county = fct_reorder(county, households, sum),
         crop = fct_reorder(crop, households, sum)) %>%
  complete(crop, county, fill = list(number_of_households = 0))

crop_counties %>%
  ggplot(aes(households, county, fill = crop)) +
  geom_col() +
  labs(x = "# of households farming this crop",
       y = "",
       fill = "Crop")

crop_counties %>%
  complete(crop, county, fill = list(households = 0)) %>%
  ggplot(aes(crop, county, fill = households)) +
  geom_tile() +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  labs(x = "Crop",
       y = "",
       fill = "# of households")

crop_counties %>%
  mutate(pct_households = households / number_of_households) %>%
  arrange(desc(pct_households)) %>%
  ggplot(aes(number_of_households, pct_households)) +
  geom_point() +
  geom_text(aes(label = county), vjust = 1, hjust = 1,
            check_overlap = TRUE) +
  scale_y_continuous(labels = percent) +
  labs(y = "% of households growing this crop") +
  facet_wrap(~ crop)

# ---- chunk_06 ----
library(rKenyaCensus)
library(sf)
library(ggthemes)

kenya_sf <- rKenyaCensus::KenyaCounties_SHP %>%
  st_as_sf() %>%
  st_simplify(dTolerance = 200) %>%
  mutate(county = str_to_title(County)) %>%
  left_join(crop_counties %>%
              filter(crop == "Avocado"), by = "county")

kenya_sf %>%
  ggplot(aes(fill = number_of_households)) +
  geom_sf() +
  theme_map() +
  labs(fill = "Households growing avocado")

# ---- chunk_07 ----
graph_by_county <- function(tbl) {
  tbl %>%
    tibble() %>%
    gather(category, population, -County) %>%
    filter(!is.na(population)) %>%
    mutate(category = respace(category)) %>%
    mutate(county = str_to_title(County)) %>%
    filter(county != "Kenya") %>%
    mutate(category = fct_reorder(category, population, sum),
           county = fct_reorder(county, population, sum)) %>%
    ggplot(aes(population, county, fill = category)) +
    geom_col()
}

V4_T2.30 %>%
  select(-Total) %>%
  graph_by_county()

V4_T2.19 %>%
  filter(AdminArea == "County") %>%
  gather(category, value, MainsElectricity:NotStated) %>%
  filter(!is.na(value)) %>%
  mutate(value = ConventionalHouseholds / 100 * value) %>%
  group_by(County, category = fct_lump(category, 5, w = value)) %>%
  summarize(value = sum(value)) %>%
  spread(category, value) %>%
  graph_by_county()

V4_T2.33 %>%
  ungroup() %>%
  filter(AdminArea == "County") %>%
  mutate(County = str_to_title(County),
         County = fct_reorder(County, UoI_Total_Perc)) %>%
  ggplot(aes(UoI_Total_Perc / 100, County)) +
  geom_col() +
  scale_x_continuous(labels = percent)
