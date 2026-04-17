# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----
knitr::opts_chunk$set(echo = TRUE)

# ---- chunk_02 ----
library(tidyverse)
library(ggthemes)
theme_set(theme_light())

wwc_outcomes <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-07-09/wwc_outcomes.csv")
squads <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-07-09/squads.csv")
codes <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-07-09/codes.csv")

outcomes <- wwc_outcomes %>%
  left_join(codes, by = "team") %>%
  group_by(year, yearly_game_id) %>%
  mutate(opposing_score = rev(score)) %>%
  ungroup() %>%
  mutate(won_by = score - opposing_score)

# ---- chunk_03 ----
library(rvest)

# Leave this code as a web scraping example
fifa_country_codes <- read_html("https://simple.wikipedia.org/wiki/List_of_FIFA_country_codes") %>%
  html_nodes("table") %>%
  map(html_table, fill = TRUE) %>%
  .[2:5] %>%
  bind_rows() %>%
  tbl_df() %>%
  select(country = Country, team = Code)

# ---- chunk_04 ----
wwc_outcomes %>%
  ggplot(aes(score)) +
  geom_histogram() +
  facet_wrap(~ win_status)

outcomes %>%
  filter(year == 2019) %>%
  count(round, sort = TRUE)

# ---- chunk_05 ----
# Of the 3 games each country plays in the "group" round, how much did they win by on average?
avg_group_scores <- outcomes %>%
  filter(round == "Group") %>%
  group_by(year, team) %>%
  summarize(avg_group_score = mean(score),
            avg_group_won_by = mean(won_by)) %>%
  ungroup()

outcomes %>%
  inner_join(avg_group_scores, by = c("year", "team")) %>%
  filter(round == "Final") %>%
  ggplot(aes(country, avg_group_won_by, fill = win_status)) +
  geom_col() +
  facet_wrap(~ year, scales = "free_x") +
  labs(title = "Does performance in the group round predict the winner of the finals?",
       subtitle = "Yes in all years except 2011. (2015 had been tied)",
       y = "Average # of goals the team had won by in the Group round",
       x = "Country",
       fill = "Result")

# ---- chunk_06 ----
outcomes %>%
  inner_join(avg_group_scores, by = c("year", "team")) %>%
  filter(round != "Group") %>%
  group_by(year, yearly_game_id) %>%
  mutate(difference = diff(avg_group_won_by)) %>%
  ungroup() %>%
  filter(team_num == 2) %>%
  mutate(round = fct_reorder(round, round, length)) %>%
  ggplot(aes(difference, won_by)) +
  geom_point() +
  geom_smooth(method = "lm") +
  geom_abline(color = "red") +
  facet_wrap(~ round) +
  labs(x = "Difference in the team's average Group score from their opponent",
       y = "How much they won by",
       title = "Can we use a team's performance in the Group round to predict finals performance?",
       subtitle = "From 1991-2019")

# ---- chunk_07 ----
library(StatsBombR)

wwc_matches <- FreeMatches(72)

extract_match <- function(index) {
  wwc_match1 <- tbl_df(get.matchFree(wwc_matches[index, ])) %>%
    mutate(timestamp = as.difftime(timestamp))
}

matches <- map_df(1:12, extract_match, .id = "match_index")

matches %>%
  mutate(match_index = as.integer(match_index)) %>%
  inner_join(wwc_matches %>% mutate(match_index = row_number())) %>%
  transmute(index,
            location,
            possession,
            minute,
            second,
            type = fct_lump(type.name, 8)) %>%
  mutate(x = map_dbl(location, 1, .default = NA),
         y = map_dbl(location, 2, .default = NA),
         timestamp = minute * 60 + second)

ggplot(wwc_match1, aes(as.numeric(timestamp) / 60)) +
  geom_histogram()

match <- wwc_match1 %>%
  transmute(index,
            location,
            possession,
            minute,
            second,
            type = fct_lump(type.name, 8)) %>%
  mutate(x = map_dbl(location, 1, .default = NA),
         y = map_dbl(location, 2, .default = NA),
         timestamp = minute * 60 + second)

match %>%
  ggplot(aes(x, y, color = type)) +
  geom_point() +
  facet_wrap(~ type)

# ---- chunk_08 ----
library(gganimate)

p <- match %>%
  filter(minute < 5) %>%
  ggplot(aes(x, y, color = type)) +
  geom_point() +
  coord_fixed() +
  transition_reveal(index, timestamp)

animate(p, nframes = 20)

# ---- chunk_09 ----
wwc_matches <- FreeMatches(72)

extract_match <- function(index) {
  wwc_match1 <- tbl_df(get.matchFree(wwc_matches[index, ])) %>%
    mutate(timestamp = as.difftime(timestamp))
}

matches <- map_df(52, extract_match)

plays <- matches %>%
  inner_join(wwc_matches, by = "match_id") %>%
  transmute(match_id,
            index,
            location,
            possession,
            minute,
            second,
            duration,
            player = player.name,
            position = position.name,
            type = fct_lump(type.name, 8)) %>%
  mutate(x = map_dbl(location, 1, .default = NA),
         y = map_dbl(location, 2, .default = NA),
         timestamp = minute * 60 + second)

plays %>%
  filter(!is.na(player)) %>%
  mutate(player = glue::glue("{ player } ({ position })"),
         player = fct_lump(player, 9)) %>%
  count(player, type, sort = TRUE) %>%
  mutate(type = fct_reorder(type, n, sum),
         player = fct_reorder(player, -n, sum)) %>%
  filter(player != "Other") %>%
  ggplot(aes(type, n)) +
  geom_col() +
  coord_flip() +
  facet_wrap(~ player) +
  labs(x = "",
       y = "# of plays they were involved in",
       title = "Which players were involved in the most plays in the 2019 Final?")

plays %>%
  filter(!is.na(position)) %>%
  mutate(position = fct_lump(position, 15)) %>%
  ggplot(aes(x, y, color = position)) +
  geom_point() +
  facet_wrap(~ position)
