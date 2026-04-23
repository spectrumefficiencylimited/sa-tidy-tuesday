# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)
library(scales)
theme_set(theme_light())

# ---- Load ----

tt <- tt_load("2021-05-11")

broadband_county <- tt$broadband %>%
  janitor::clean_names() %>%
  rename(state = st) %>%
  mutate(state = state.name[match(state, state.abb)]) %>%
  mutate(state = ifelse(is.na(state), "District of Columbia", state),
         broadband_availability_per_fcc = parse_number(broadband_availability_per_fcc, na = "-"),
         broadband_usage = parse_number(broadband_usage, na = "-")) %>%
  mutate(county = paste0(str_remove(county_name, " County$"), ", ", state),
         county = fct_reorder(county, broadband_availability_per_fcc),
         county_id = sprintf("%05d", county_id))

broadband_zip <- tt$broadband_zip %>%
  janitor::clean_names() %>%
  rename(state = st) %>%
  mutate(state = state.name[match(state, state.abb)]) %>%
  mutate(state = ifelse(is.na(state), "District of Columbia", state)) %>%
  mutate(county = paste0(str_remove(county_name, " County$"), ", ", state),
         postal_code = sprintf("%05d", postal_code))

broadband_zip

# ---- chunk_03 ----
library(tidycensus)
library(readxl)
library(rio)

county_population <- read_excel("~/Downloads/co-est2019-annres.xlsx", skip = 3) %>%
  select(county = ...1,
         population_2017 = `2017`,
         population_2019 = `2019`) %>%
  separate(county, c("county_name", "state"), sep = ", ") %>%
  mutate(county_name = str_remove(county_name, "^\\."))

broadband_with_population <- broadband_county %>%
  inner_join(county_population, by = c("county_name", "state"))

broadband_with_population %>%
  arrange(desc(population_2017)) %>%
  head(40) %>%
  ggplot(aes(broadband_availability_per_fcc, county)) +
  geom_point() +
  scale_x_continuous(labels = percent_format())

broadband_with_population %>%
  arrange(desc(population_2017)) %>%
  filter(population_2017 >= 30000) %>%
  ggplot(aes(population_2017, broadband_availability_per_fcc)) +
  geom_point() +
  geom_text(aes(label = county), check_overlap = TRUE, vjust = 1, hjust = 1) +
  scale_x_log10(labels = comma_format()) +
  scale_y_continuous(labels = percent_format()) +
  expand_limits(x = 10000) +
  labs(y = "Broadband availability in 2017",
       x = "Population in 2017")

broadband_with_population %>%
  filter(population_2019 >= 10000) %>%
  ggplot(aes(population_2019, broadband_usage)) +
  geom_point() +
  geom_text(aes(label = county), check_overlap = TRUE, vjust = 1, hjust = 1) +
  geom_smooth(method = "lm") +
  scale_x_log10(labels = comma_format()) +
  scale_y_continuous(labels = percent_format()) +
  expand_limits(x = 10000) +
  labs(y = "Broadband usage in 2019",
       x = "Population in 2019")

# ---- chunk_04 ----
library(zipcodeR)

broadband_zip_joined <- broadband_zip %>%
  inner_join(zip_code_db %>% select(-state, -county),
             by = c(postal_code = "zipcode"))

broadband_zip_joined %>%
  ggplot(aes(population_density)) +
  geom_histogram() +
  scale_x_log10()

broadband_zip_joined %>%
  filter(population >= 10000) %>%
  filter(state %in% c("Texas", "New York", "California", "Pennsylvania")) %>%
  ggplot(aes(population_density, broadband_usage)) +
  geom_point() +
  scale_x_log10() +
  scale_y_continuous(labels = percent) +
  facet_wrap(~ state) +
  geom_smooth(method = "lm") +
  labs(x = "People / square mile in zip code",
       y = "Broadband usage")

as_tibble(zip_code_db)

# ---- chunk_05 ----
library(tigris)
library(sf)

zip_code_shapes <- zctas(starts_with = c("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"))

zip_code_shapes %>%
  head(20) %>%
  ggplot() +
  geom_sf()

counties_sf <- counties()

counties_sf %>%
  inner_join(broadband_with_population, by = c(GEOID = "county_id")) %>%
  ggplot() +
  geom_sf()

counties_sf %>%
  filter(GEOID == "01001")


counties %>%
  st_simplify(dTolerance = .1) %>%
  ggplot() +
  geom_sf()

counties %>%
  head(100) %>%
  ggplot() +
  geom_sf()

# ---- Readme ----

tt

# ---- Glimpse ----

tt %>% 
  map(glimpse)

# ---- Wrangle ----

# ---- Visualize ----

# ---- chunk_10 ----

# This will save your most recent plot
ggsave(
  filename = "My TidyTuesday Plot.png",
  device = "png")
