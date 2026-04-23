# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)
library(scales)
library(countrycode)
theme_set(theme_light())

# ---- Load ----
library(lubridate)

tt <- tt_load("2021-05-04")

water <- tt$water %>%
  mutate(report_date = mdy(report_date)) %>%
  rename(lat = lat_deg,
         lon = lon_deg,
         country = country_name) %>%
  separate(water_tech, c("water_tech", "brand"), sep = " - ",
           fill = "right") %>%
  mutate(install_year = ifelse(install_year > 2021, NA_real_, install_year)) %>%
  filter(!country %in% c("Peru", "Dominican Republic", "Timor-Leste"),
         !is.na(country)) %>%
  filter(between(lat, -35, 37),
         between(lon, -40, 60))

# ---- chunk_03 ----
water %>%
  count(status_id)

water %>%
  count(water_tech, sort = TRUE)

water %>%
  count(water_source, sort = TRUE)

water %>%
  count(water_source, water_tech, sort = TRUE)

# ---- chunk_04 ----
water %>%
  filter(install_year > 2021) %>%
  View()

water %>%
  filter(install_year > 1980) %>%
  count(install_year) %>%
  ggplot(aes(install_year, n)) +
  geom_col()

water %>%
  count(installer, sort = TRUE) %>%
  View()

# ---- chunk_05 ----
water %>%
  count(status_id, status, sort = TRUE)

# ---- chunk_06 ----
library(ggthemes)

water %>%
  group_by(country) %>%
  summarize(lat = mean(lat),
            lon = mean(lon)) %>%
  ggplot(aes(lon, lat)) +
  geom_point() +
  geom_text(aes(label = country), vjust = 1, hjust = 1)

countries <- unique(water$country)

africa_map_data <- map_data("world") %>%
  as_tibble() %>%
  mutate(continent = countrycode(region, "country.name", "continent")) %>%
  filter(continent == "Africa")

water %>%
  sample_n(10000) %>%
  ggplot(aes(lon, lat)) +
  geom_polygon(aes(long, lat, group = group),
               color = "gray",
               fill = "white",
               data = africa_map_data,
               size = .25) +
  geom_point(size = .1, alpha = .25) +
  theme_map()

water %>%
  count(country, sort = TRUE)

water %>%
  filter(country == "Uganda") %>%
  sample_n(10000) %>%
  ggplot(aes(lon, lat)) +
  geom_polygon(aes(long, lat, group = group),
               color = "gray",
               fill = "white",
               data = africa_map_data,
               size = .25) +
  geom_point(size = .1, alpha = .25) +
  theme_map()

# ---- chunk_07 ----
water_uganda <- water %>%
  filter(country == "Uganda",
         between(lat, -2, 4),
         between(lon, 29, 40))

water_uganda %>%
  #sample_n(20000) %>%
  ggplot(aes(lon, lat, color = status_id)) +
  borders("world", regions = "Uganda") +
  geom_point(size = .1, alpha = .25) +
  theme_map() +
  scale_color_discrete(guide = guide_legend(override.aes = list(size = 2, alpha = 1)))

# ---- chunk_08 ----
bbox <- c(left = 29.2, bottom = -2, right = 35, top = 4.2)

uganda_map <- get_stamenmap(bbox, zoom = 8)

# ---- chunk_09 ----
water_uganda_lumped <- water_uganda %>%
  mutate(water_source = fct_lump(water_source, 5)) %>%
  replace_na(list(water_source = "Other")) %>%
  mutate(water_source = fct_reorder(water_source, water_source, length, .desc = TRUE))

ggmap(uganda_map) +
  geom_point(aes(lon, lat),
             data = water_uganda_lumped, size = .1, alpha = .1) +
  facet_wrap(~ water_source)

water_uganda %>%
  count(water_source, sort = TRUE)

water_uganda %>%
  count(pay, sort = T)

# ---- chunk_10 ----
water_uganda_lumped %>%
  mutate(report_year = year(report_date)) %>%
  count(report_year, water_source) %>%
  complete(report_year, water_source, fill = list(n = 0)) %>%
  group_by(report_year) %>%
  mutate(year_total = sum(n)) %>%
  filter(year_total >= 500) %>%
  ggplot(aes(report_year, n / year_total, fill = water_source)) +
  geom_area()

water_uganda_lumped %>%
  count(water_tech, sort = TRUE)

water_uganda_lumped %>%
  mutate(water_tech = fct_lump(water_tech, 5)) %>%
  mutate(report_year = year(report_date)) %>%
  count(report_year, water_tech) %>%
  complete(report_year, water_tech, fill = list(n = 0)) %>%
  group_by(report_year) %>%
  mutate(year_total = sum(n)) %>%
  filter(year_total >= 500) %>%
  ggplot(aes(report_year, n, fill = water_tech)) +
  geom_area()

# ---- chunk_11 ----
water_uganda %>%
  ggplot(aes(report_date, install_year)) +
  geom_point()

# ---- chunk_12 ----
ggmap(uganda_map) +
  geom_point(aes(lon, lat, color = install_year),
             data = water_uganda %>% sample_n(20000),
             size = .2) +
  scale_color_gradient2(low = "red", high = "brown",
                        midpoint = 1990)

library(gganimate)

water_uganda %>%
  filter(!is.na(install_year)) %>%
  sample_n(10000) %>%
  mutate(install_year = pmax(1990, install_year)) %>%
  mutate(year = map(install_year, ~ seq(., 2021))) %>%
  unnest(year) %>%
  ggplot(aes(lon, lat)) +
  borders("world", regions = "Uganda") +
  geom_point(size = .1, alpha = .25) +
  theme_map() +
  transition_manual(year) +
  labs(title = "Water sources in Uganda in year: { current_frame }")

# ---- chunk_13 ----
point_data <- water_uganda %>%
  filter(!is.na(install_year)) %>%
  mutate(install_year = pmax(1990, install_year)) %>%
  mutate(year = map(install_year, ~ seq(., 2021))) %>%
  unnest(year)

ggmap(uganda_map) +
  geom_point(aes(lon, lat), data = point_data, size = .1, alpha = .25) +
  transition_manual(year) +
  labs(title = "Water sources in Uganda in year: { current_frame }")

# ---- chunk_14 ----
get_map(c(lon = -95.3632715, lat = 29.7632836),
        source = "osm")

# ---- chunk_15 ----
water_uganda %>%
