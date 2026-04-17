# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)
library(scales)
theme_set(theme_light())

# ---- Load ----

tt <- tt_load("2020-12-15")

ninja_warrior <- tt$ninja_warrior %>%
  mutate(round_stage = str_remove(round_stage, " \\(Regional/City\\)"))

# ---- chunk_03 ----
ninja_warrior %>%
  count(location, sort = TRUE)

ninja_warrior %>%
  count(round_stage, obstacle_name, sort = TRUE)

ninja_warrior %>%
  filter(location == "Venice") %>%
  View()

ninja_warrior %>%
  count(location, round_stage, sort = T) %>%
  view()

ninja_warrior %>%
  filter(!str_detect(round_stage, "National")) %>%
  count(season, location, round_stage) %>%
  ggplot(aes(n, fill = round_stage)) +
  geom_histogram() +
  scale_x_continuous(breaks = 1:10) +
  labs(x = "# of obstacles")

ninja_warrior %>%
  count(round_stage, sort = TRUE)

# ---- chunk_04 ----
library(tidylo)

ninja_warrior %>%
  filter(round_stage %in% c("Qualifying", "Finals")) %>%
  count(round_stage, obstacle_name, sort = TRUE) %>%
  bind_log_odds(round_stage, obstacle_name, n) %>%
  arrange(desc(log_odds_weighted)) %>%
  filter(round_stage == "Finals") %>%
  top_n(16, abs(log_odds_weighted)) %>%
  mutate(obstacle_name = fct_reorder(obstacle_name, log_odds_weighted)) %>%
  ggplot(aes(log_odds_weighted, obstacle_name)) +
  geom_col() +
  labs(x = "More / less likely in finals")

# ---- chunk_05 ----
total_rounds <- ninja_warrior %>%
  filter(round_stage == "Qualifying") %>%
  distinct(season, location) %>%
  nrow()
  
library(tidytext)

ninja_warrior %>%
  filter(round_stage %in% c("Qualifying", "Finals")) %>%
  unite(season_location, season, location, remove = FALSE) %>%
  group_by(round_stage) %>%
  mutate(total_rounds = n_distinct(season_location)) %>%
  group_by(round_stage, obstacle_name) %>%
  summarize(avg_position = mean(obstacle_order),
            n_rounds = n(),
            pct_rounds = n_rounds / first(total_rounds)) %>%
  arrange(desc(n_rounds)) %>%
  top_n(10, n_rounds) %>%
  ungroup() %>%
  mutate(obstacle_name = reorder_within(obstacle_name, avg_position, round_stage)) %>%
  ggplot(aes(avg_position, obstacle_name, size = pct_rounds)) +
  geom_point() +
  facet_wrap(~ round_stage, nrow = 2, scales = "free_y") +
  scale_x_continuous(breaks = 1:10) +
  scale_y_reordered() +
  scale_size_continuous(labels = percent) +
  labs(x = "Average position within the obstacle course",
       y = "",
       size = "% of courses")

# ---- chunk_06 ----
visualize_steps <- function(tbl) {
  tbl %>%
    add_count(obstacle_order, round_stage, name = "round_stage_total") %>%
    filter(round_stage_total >= 10) %>%
    mutate(obstacle_name = fct_lump(obstacle_name, 10)) %>%
    mutate(obstacle_name = fct_reorder(obstacle_name, obstacle_order)) %>%
    count(round_stage_total, obstacle_name, obstacle_order) %>%
    ggplot(aes(obstacle_order, n / round_stage_total, fill = obstacle_name)) +
    geom_col(width = 1) +
    scale_x_continuous(breaks = 1:10) +
    scale_y_continuous(labels = percent) +
    labs(x = "Step",
         y = "% of courses",
         fill = "Obstacle")
}

ninja_warrior %>%
  filter(round_stage == "Qualifying") %>%
  visualize_steps() +
  labs(title = "What does a typical Qualifying course look like?")

ninja_warrior %>%
  filter(round_stage == "Finals") %>%
  visualize_steps() +
  labs(title = "What does a typical Finals course look like?")

ninja_warrior %>%
  filter(round_stage == "Finals") %>%
  visualize_steps() +
  labs(title = "What does a typical Finals course look like?") +
  facet_wrap(~ obstacle_name) +
  theme(legend.position = "none")

# ---- chunk_07 ----
library(glue)

ninja_warrior %>%
  filter(round_stage == "Qualifying") %>%
  add_count(obstacle_order, round_stage, name = "round_stage_total") %>%
  filter(round_stage_total >= 10) %>%
  add_count(obstacle_name, name = "obstacle_total") %>%
  mutate(obstacle_name = glue("{ obstacle_name } ({ obstacle_total })")) %>%
  mutate(obstacle_name = fct_lump(obstacle_name, 10)) %>%
  mutate(obstacle_name = fct_reorder(obstacle_name, obstacle_order)) %>%
  ggplot(aes(obstacle_order, obstacle_name)) +
  geom_boxplot() +
  scale_x_continuous(breaks = 1:10) +
  labs(x = "Step",
       y = "% of courses",
       fill = "Obstacle")

# ---- chunk_08 ----
ninja_warrior %>%
  filter(round_stage == "Qualifying",
         obstacle_order <= 6) %>%
  mutate(lumped = fct_lump(obstacle_name, 12),
         lumped = fct_reorder(lumped, obstacle_order + season * .01)) %>%
  unite(season_location, season, location, sep = " - ", remove = FALSE) %>%
  mutate(season_location = fct_rev(fct_reorder(season_location, season))) %>%
  ggplot(aes(obstacle_order, season_location, fill = lumped)) +
  geom_tile() +
  geom_text(aes(label = obstacle_name), size = 3) +
  theme(legend.position = "none") +
  scale_x_continuous(breaks = 1:6) +
  labs(x = "Step",
       y = "")

ninja_warrior %>%
  filter(round_stage == "Finals",
         obstacle_order <= 10) %>%
  mutate(obstacle_name = str_trunc(obstacle_name, 15),
         lumped = fct_lump(obstacle_name, 12),
         lumped = fct_reorder(lumped, obstacle_order + season * .01)) %>%
  unite(season_location, season, location, sep = " - ", remove = FALSE) %>%
  mutate(season_location = fct_rev(fct_reorder(season_location, season))) %>%
  ggplot(aes(obstacle_order, season_location, fill = lumped)) +
  geom_tile() +
  geom_text(aes(label = obstacle_name), size = 3) +
  theme(legend.position = "none") +
  scale_x_continuous(breaks = 1:10) +
  labs(x = "Step",
       y = "")

# ---- chunk_09 ----
ninja_warrior %>%
  filter(round_stage == "Qualifying") %>%
  mutate(obstacle_name = fct_lump(obstacle_name, 15)) %>%
  mutate(obstacle_name = fct_reorder(obstacle_name, season)) %>%
  ggplot(aes(season, obstacle_name)) +
  geom_boxplot() +
  scale_x_continuous(breaks = 1:10)

ninja_warrior %>%
  filter(round_stage == "Qualifying") %>%
  mutate(obstacle_name = fct_lump(obstacle_name, 8)) %>%
  mutate(obstacle_name = fct_rev(fct_reorder(obstacle_name, season))) %>%
  count(obstacle_name, season) %>%
  group_by(season) %>%
  mutate(pct = n / sum(n)) %>%
  ggplot(aes(season, pct, fill = obstacle_name)) +
  geom_col() +
  scale_x_continuous(breaks = 1:10) +
  scale_y_continuous(labels = percent) +
  labs(y = "% of obstacles")

# ---- chunk_10 ----
ninja_warrior %>%
  filter()

# ---- Readme ----

tt

# ---- Glimpse ----

tt %>% 
  map(glimpse)

# ---- Wrangle ----

# ---- Visualize ----

# ---- chunk_15 ----

# This will save your most recent plot
ggsave(
  filename = "My TidyTuesday Plot.png",
  device = "png")
