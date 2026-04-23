# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)
library(scales)
theme_set(theme_light())

# ---- Load ----

tt <- tt_load("2020-09-08")

# ---- chunk_03 ----
library(glue)

episodes <- tt$friends_info %>%
  mutate(full_title = glue("{ season }.{ episode } { title }"),
         full_title = fct_reorder(full_title, season + .001 * episode))

friends <- tt$friends %>%
  inner_join(episodes, by = c("season", "episode"))
  
friends %>%
  count(season, full_title)

tt$friends %>%
  count(speaker, sort = TRUE)

# ---- chunk_04 ----
episodes %>%
  ggplot(aes(as.integer(full_title), us_views_millions)) +
  geom_line() +
  geom_point(aes(color = factor(season))) +
  geom_text(aes(label = title), vjust = 1, hjust = 1,
            check_overlap = TRUE,
            size = 2) +
  expand_limits(y = 0) +
  labs(x = "Episode number",
       color = "Season")

episodes %>%
  ggplot(aes(as.integer(full_title), imdb_rating)) +
  geom_line() +
  geom_point(aes(color = factor(season))) +
  geom_text(aes(label = title), vjust = 1, hjust = 1,
            check_overlap = TRUE,
            size = 2) +
  labs(x = "Episode number",
       y = "IMDB Rating",
       color = "Season")

# ---- chunk_05 ----
speaker_lines_per_episode <- friends %>%
  count(speaker, title, imdb_rating, season) %>%
  complete(speaker, title, fill = list(n = 0)) %>%
  group_by(title) %>%
  fill(imdb_rating, season, .direction = "downup") %>%
  ungroup() %>%
  add_count(title, wt = n, name = "episode_total") %>%
  mutate(pct = n / episode_total)

speaker_lines_per_episode %>%
  semi_join(main_cast, by = "speaker") %>%
  mutate(speaker = fct_reorder(speaker, pct)) %>%
  ggplot(aes(pct, speaker)) +
  geom_boxplot() +
  scale_x_log10()

speaker_lines_per_episode %>%
  semi_join(main_cast, by = "speaker") %>%
  group_by(speaker) %>%
  summarize(correlation = cor(log2(pct), imdb_rating))

friends %>%
  count(season, episode, title) %>%
  inner_join(distinct(episodes, season, episode, imdb_rating)) %>%
  filter(n <= 500) %>%
  ggplot(aes(n, imdb_rating)) +
  geom_point() +
  geom_smooth(method = "lm")

# ---- chunk_06 ----
speakers_per_episode_wide <- speaker_lines_per_episode %>%
  semi_join(main_cast, by = "speaker") %>%
  select(-n) %>%
  spread(speaker, pct) %>%
  select(-title)

speakers_per_episode_wide %>%
  select(-season) %>%
  mutate(across(.cols = -c(imdb_rating), log2)) %>%
  lm(imdb_rating ~ ., data = .) %>%
  summary()

# ---- chunk_07 ----
library(tidytext)

words_unnested <- friends %>%
  select(text, speaker, season, episode, full_title) %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words, by = "word") %>%
  filter(!word %in% c("hey", "yeah", "gonna", "uh"))

library(tidylo)

by_speaker_word <- words_unnested %>%
  semi_join(main_cast, by = "speaker") %>%
  count(speaker, word) %>%
  add_count(word, wt = n, name = "word_total") %>%
  filter(word_total >= 50)

by_speaker_word %>%
  bind_log_odds(speaker, word, n) %>%
  group_by(speaker) %>%
  top_n(16, log_odds_weighted) %>%
  ungroup() %>%
  mutate(word = reorder_within(word, log_odds_weighted, speaker)) %>%
  ggplot(aes(log_odds_weighted, word)) +
  geom_col(aes(fill = speaker), show.legend = FALSE) +
  scale_y_reordered() +
  facet_wrap(~ speaker, scales = "free") +
  labs(x = "Log odds (this character) / (other characters)",
       title = "What words are most characteristic of each character")

words_unnested %>%
  count(word, sort = TRUE)

# ---- chunk_08 ----
library(widyr)

friends %>%
  unite(scene_id, season, episode, scene) %>%
  count(speaker, scene_id) %>%
  semi_join(main_cast, by = "speaker") %>%
  pairwise_cor(speaker, scene_id, n, sort = TRUE) %>%
  mutate(item2 = reorder_within(item2, correlation, item1)) %>%
  ggplot(aes(correlation, item2)) +
  geom_col(aes(fill = item1), show.legend = FALSE) +
  scale_y_reordered() +
  facet_wrap(~ item1, scales = "free_y") +
  labs(x = "Correlation between characters appearing in a scene",
       y = "Other character")

# ---- chunk_09 ----
friends %>%
  unite(scene_id, season, episode, scene) %>%
  add_count(speaker, name = "speaker_total") %>%
  filter(speaker_total >= 50) %>%
  count(speaker, scene_id) %>%
  pairwise_cor(speaker, scene_id, n, sort = TRUE) %>%
  filter(item1 == "Ross Geller")

# ---- chunk_10 ----
friends %>%
  count(season, episode, sort = TRUE)

main_cast <- friends %>%
  count(speaker, sort = TRUE) %>%
  head(6)

main_cast %>%
  mutate(speaker = fct_reorder(speaker, n)) %>%
  ggplot(aes(n, speaker)) +
  geom_col()

friends %>%
  semi_join(main_cast, by = "speaker") %>%
  group_by(speaker) %>%
  summarize(n_episodes = n_distinct())



friends %>%
  count(season)

friends %>%
  count(speaker, season) %>%
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
