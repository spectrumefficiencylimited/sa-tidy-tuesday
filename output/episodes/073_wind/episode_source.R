# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----
knitr::opts_chunk$set(echo = TRUE)

# ---- chunk_02 ----
library(tidyverse)

us_wind <- read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-11-06/us_wind.csv")

# ---- chunk_03 ----
us_wind_processed <- us_wind %>%
  filter(!t_state %in% c("AK", "HI", "GU", "PR")) %>%
  mutate(t_cap = ifelse(t_cap < 0, NA, t_cap)) %>%
  mutate_if(is.numeric, ~ ifelse(. == -9999, NA, .))

wind_projects <- us_wind_processed %>%
  group_by(p_name, t_state) %>%
  summarize(year = min(p_year, na.rm = TRUE),
            turbines = n(),
            total_capacity = sum(t_cap),
            lon = mean(xlong),
            lat = mean(ylat),
            lon_sd = sd(xlong),
            lat_sd = sd(ylat)) %>%
  ungroup()

# ---- chunk_04 ----
turbine_models <- us_wind_processed %>%
  group_by(t_model) %>%
  summarize(t_cap = median(t_cap),
            t_hh = median(t_hh),
            t_rd = median(t_rd),
            t_rsa = median(t_rsa),
            t_ttlh = median(t_ttlh),
            turbines = n(),
            projects = n_distinct(p_name)) %>%
  arrange(desc(projects))

turbine_models %>%
  ggplot(aes(t_ttlh, t_cap)) +
  geom_point() +
  labs(title = "When it comes to turbines, bigger is better!",
       x = "Turbine total height (meters)",
       y = "Turbine capacity (kW)")

turbine_models %>%
  ggplot(aes(t_rsa, t_cap)) +
  geom_point() +
  labs(title = "When it comes to turbines, bigger is better!",
       x = "Turbine rotor swept area (meters ^ 2)",
       y = "Turbine capacity (kW)")

# ---- chunk_05 ----
wind_projects %>%
  ggplot(aes(year, total_capacity)) +
  geom_point()

wind_projects %>%
  ggplot(aes(year, total_capacity / turbines)) +
  geom_point()

# ---- chunk_06 ----
wind_projects %>%
  ggplot(aes(lon, lat, size = turbines, color = year)) +
  borders("state") +
  geom_point() +
  coord_map() +
  theme_void()

# ---- chunk_07 ----
library(gganimate)

ggplot(mtcars, aes(factor(cyl), mpg)) + 
  geom_boxplot() + 
  # Here comes the gganimate code
  transition_states(
    gear,
    transition_length = 2,
    state_length = 1
  ) +
  enter_fade() + 
  exit_shrink() +
  ease_aes('sine-in-out')

# ---- chunk_08 ----
wind_projects

wind_projects %>%
  filter(!is.na(year), !is.infinite(year)) %>%
  crossing(time = 1981:2018) %>%
  filter(year <= time) %>%
  ggplot(aes(lon, lat, size = turbines, color = year)) +
  borders("state") +
  geom_point() +
  transition_manual(time) +
  scale_color_continuous(guide = FALSE) +
  labs(title = "Locations of wind turbine projects in continental US (1981-2018)") +
  coord_map() +
  theme_void()

p
anim_save("turbines.gif")

# ---- chunk_09 ----
us_wind_processed
