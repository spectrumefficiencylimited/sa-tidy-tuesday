# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)
library(scales)
theme_set(theme_light())

# ---- Load ----

tt <- tt_load("2020-08-25")

tt

chopped <- tt$chopped

# ---- chunk_03 ----
chopped %>%
  ggplot(aes(episode_rating)) +
  geom_histogram()

chopped %>%
  arrange(episode_rating) %>%
  View()

chopped %>%
  filter(!is.na(episode_rating)) %>%
  ggplot(aes(series_episode, episode_rating)) +
  geom_line(alpha = .5, color = "gray") +
  geom_point(aes(color = factor(season))) +
  geom_text(aes(label = episode_name), hjust = 1,
            check_overlap = TRUE) +
  theme(legend.position = "none")

chopped %>%
  filter(!is.na(episode_rating)) %>%
  group_by(season) %>%
  summarize(n_episodes = n(),
            avg_rating = mean(episode_rating)) %>%
  ggplot(aes(season, avg_rating)) +
  geom_line() +
  geom_point(aes(size = n_episodes)) +
  theme(legend.position = "none") +
  labs(x = "Season",
       y = "Average Rating")

# ---- chunk_04 ----
library(glue)

chopped %>%
  arrange(desc(episode_rating)) %>%
  head(25) %>%
  mutate(name = glue("{ season }.{season_episode} { episode_name }"),
         name = fct_reorder(name, episode_rating)) %>%
  ggplot(aes(episode_rating, name)) +
  geom_point()

# ---- chunk_05 ----
ingredients <- chopped %>%
  select(season, season_episode, series_episode, episode_name,
         episode_rating, appetizer:dessert) %>%
  pivot_longer(cols = c(appetizer:dessert),
               names_to = "course",
               values_to = "ingredient") %>%
  separate_rows(ingredient, sep = ", ") %>%
  mutate(course = fct_relevel(course, c("appetizer", "entree")))

ingredients %>%
  count(course, ingredient, sort = TRUE) %>%
  filter(fct_lump(ingredient, 25, w = n) != "Other") %>%
  mutate(ingredient = fct_reorder(ingredient, n, sum),
         course = fct_rev(course)) %>%
  ggplot(aes(n, ingredient, fill = course)) +
  geom_col() +
  scale_fill_discrete(guide = guide_legend(reverse = TRUE)) +
  labs(x = "# of episodes",
       y = "",
       title = "Most common ingredients in Chopped",
       fill = "Course")

# ---- chunk_06 ----
library(widyr)
library(ggraph)
library(tidygraph)

ingredients_filtered <- ingredients %>%
  add_count(ingredient) %>%
  filter(n >= 8)

ingredient_correlations <- ingredients_filtered %>%
  pairwise_cor(ingredient, series_episode, sort = TRUE)

ingredients_filtered %>%
  pairwise_count(ingredient, series_episode, sort = TRUE)

# Not sure this is useful since they appear across courses
ingredient_correlations %>%
  head(75) %>%
  ggraph(layout = "fr") +
  geom_edge_link(aes(edge_alpha = correlation)) +
  geom_node_point() +
  geom_node_text(aes(label = name), repel = TRUE)

# Do any pairs of ingredients appear together in the same course
# across episodes?
ingredients_filtered %>%
  unite(episode_course, series_episode, course) %>%
  pairwise_count(ingredient, episode_course, sort = TRUE)

# ---- chunk_07 ----
early_late_ingredients <- ingredients_filtered %>%
  group_by(ingredient) %>%
  summarize(first_season = min(season),
            avg_season = mean(season),
            last_season = max(season),
            n_appearances = n()) %>%
  arrange(desc(avg_season)) %>%
  slice(c(1:6, tail(row_number())))

ingredients_filtered %>%
  semi_join(early_late_ingredients, by = "ingredient") %>%
  mutate(ingredient = fct_reorder(ingredient, season)) %>%
  ggplot(aes(season, ingredient)) +
  geom_boxplot()

# ---- chunk_08 ----
ingredients_wide <- ingredients_filtered %>%
  select(season, series_episode, episode_rating, ingredient) %>%
  mutate(value = 1) %>%
  pivot_wider(names_from = ingredient,
              values_from = value,
              values_fill = list(value = 0)) %>%
  select(-series_episode) %>%
  janitor::clean_names()

lm(episode_rating ~ season, data = ingredients_wide) %>%
  summary()

library(tidymodels)

set.seed(2020)
split_data <- ingredients_wide %>%
  filter(!is.na(episode_rating)) %>%
  initial_split()

training_set <- training(split_data)

# ---- chunk_09 ----
cv_samples <- training_set %>%
  vfold_cv(v = 10)

# ---- chunk_10 ----
model_spec <- linear_reg(penalty = tune()) %>%
  set_engine("glmnet")

parameter_search <- model_spec %>%
  tune_grid(episode_rating ~ ., resamples = cv_samples)

parameter_search %>%
  collect_metrics() %>%
  filter(.metric == "rmse") %>%
  ggplot(aes(penalty, mean)) +
  geom_line() +
  scale_x_log10() +
  labs(y = "Mean Squared Error")

# ---- chunk_11 ----
rf_spec <- rand_forest(mode = "regression",
                       trees = tune()) %>%
  set_engine("ranger")

cv_samples <- training_set %>%
  vfold_cv(v = 10)

parameter_search <- rf_spec %>%
  tune_grid(episode_rating ~ ., resamples = cv_samples)

parameter_search %>%
  collect_metrics() %>%
  filter(.metric == "rmse") %>%
  ggplot(aes(trees, mean)) +
  geom_line() +
#   scale_x_log10() +
  labs(x = "# of trees in random forest",
       y = "Mean Squared Error")

model <- rand_forest(mode = "regression", mtry = 3, trees = 500) %>%
  set_engine("ranger") %>%
  fit(episode_rating ~ ., training_set)

test_set <- testing(split_data)

predict(model, test_set) %>%
  bind_cols(test_set) %>%
  rmse(.pred, episode_rating)

test_set %>%
  mutate(average = mean(episode_rating)) %>%
  rmse(average, episode_rating)

# ---- chunk_12 ----
rec <- recipe(episode_rating ~ season, training_set) %>%
  step_ns(season, deg_free = tune())

parameter_search_df <- linear_reg() %>%
  set_engine("lm") %>%
  tune_grid(rec, resamples = cv_samples)

parameter_search_df %>%
  collect_metrics() %>%
  filter(.metric == "rmse") %>%
  ggplot(aes(deg_free, mean)) +
  geom_line()

training_data_processed <- recipe(episode_rating ~ season, training_set) %>%
  step_ns(season, deg_free = 2) %>%
  prep() %>%
  juice()

spline_model <- linear_reg() %>%
  set_engine("lm") %>%
  fit(episode_rating ~ season, data = juice(training_data_processed))
