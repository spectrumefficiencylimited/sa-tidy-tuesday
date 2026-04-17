# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----
knitr::opts_chunk$set(echo = TRUE)

# ---- chunk_02 ----
library(tidyverse)
theme_set(theme_light())

nyc_squirrels <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-10-29/nyc_squirrels.csv")

# ---- chunk_03 ----
nyc_squirrels %>%
  count(zip_codes, sort = TRUE)

# ---- chunk_04 ----
nyc_squirrels %>%
  ggplot(aes(long, lat)) +
  geom_point()

by_hectare <- nyc_squirrels %>%
  filter(!is.na(primary_fur_color)) %>%
  group_by(hectare) %>%
  summarize(long = mean(long),
            lat = mean(lat),
            pct_gray = mean(primary_fur_color == "Gray", na.rm = TRUE),
            n = n())

by_hectare %>%
  filter(n >= 10) %>%
  ggplot(aes(long, lat, size = n, color = pct_gray)) +
  geom_point() +
  theme_void()

by_hectare %>%
  filter(n >= 10) %>%
  ggplot(aes(lat, pct_gray)) +
  geom_point() +
  geom_smooth()

by_hectare %>%
  mutate(n_gray = round(pct_gray * n)) %>%
  glm(cbind(n_gray, n - n_gray) ~ lat, data = ., family = "binomial") %>%
  summary()

# ---- chunk_05 ----
nyc_squirrels %>%
  count(highlight_fur_color, sort = TRUE)

nyc_squirrels %>%
  count(approaches, indifferent, runs_from, sort = TRUE)

# ---- chunk_06 ----
glm(runs_from ~ lat, data = nyc_squirrels, family = "binomial") %>%
  summary()

# ---- chunk_07 ----
library(sf)

central_park_sf <- read_sf("~/Downloads/CentralAndProspectParks/")

by_hectare <- nyc_squirrels %>%
  add_count(hectare) %>%
  mutate(above_ground = !is.na(location) & location == "Above Ground") %>%
  group_by(hectare, n) %>%
  summarize_at(vars(long, lat, approaches:runs_from,  ends_with("ing"), above_ground), mean) %>%
  ungroup()

by_hectare %>%
  filter(n >= 10) %>%
  ggplot() +
  geom_sf(data = central_park_sf) +  
  geom_point(aes(long, lat, size = n, color = runs_from)) +
  theme_void() +
  scale_color_gradient2(low = "blue", high = "red", mid = "pink",
                        midpoint = .3, labels = scales::percent) +
  labs(color = "% of squirrels run",
       size = "# of squirrels",
       title = "Squirrels in the northwest corner of Central Park are more likely to run away") +
  coord_sf(datum = NA)

# ---- chunk_08 ----
central_park_sf %>%
  count(lanes, sort = TRUE)

ggplot(central_park_sf) +
  geom_sf() +
  geom_point(aes(long, lat, color = runs_from), data = by_hectare) +
  coord_sf(datum = NA)

# ---- chunk_09 ----
central_park_sf %>%
  ggplot() +
  geom_sf(aes(color = bicycle)) +
  coord_sf(datum = NA)
