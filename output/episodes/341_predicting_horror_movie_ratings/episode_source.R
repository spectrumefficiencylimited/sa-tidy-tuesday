# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----
knitr::opts_chunk$set(echo = TRUE)

# ---- chunk_02 ----
library(tidyverse)
theme_set(theme_light())

horror_movies_raw <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-10-22/horror_movies.csv")

# ---- chunk_03 ----
horror_movies <- horror_movies_raw %>%
  arrange(desc(review_rating)) %>%
  extract(title, "year", "\\((\\d\\d\\d\\d)\\)$", remove = FALSE, convert = TRUE) %>%
  mutate(budget = parse_number(budget)) %>%
  separate(plot, c("director", "cast_sentence", "plot"), extra = "merge", sep = "\\. ", fill = "right") %>%
  distinct(title, .keep_all = TRUE)

# ---- chunk_04 ----
horror_movies %>%
  count(genres, sort = TRUE)

horror_movies %>%
  count(language, sort = TRUE)

horror_movies %>%
  ggplot(aes(budget)) +
  geom_histogram() +
  scale_x_log10(labels = scales::dollar)

# ---- chunk_05 ----
horror_movies %>%
  ggplot(aes(budget, review_rating)) +
  geom_point() +
  scale_x_log10(labels = scales::dollar) +
  geom_smooth(method = "lm")

# ---- chunk_06 ----
horror_movies %>%
  mutate(movie_rating = fct_lump(movie_rating, 5),
         movie_rating = fct_reorder(movie_rating, review_rating, na.rm = TRUE)) %>%
  ggplot(aes(movie_rating, review_rating)) +
  geom_boxplot() +
  coord_flip()

horror_movies %>%
  filter(!is.na(movie_rating)) %>%
  mutate(movie_rating = fct_lump(movie_rating, 5)) %>%
  lm(review_rating ~ movie_rating, data = .) %>%
  anova()

# ---- chunk_07 ----
horror_movies %>%
  separate_rows(genres, sep = "\\| ") %>%
  mutate(genre = fct_lump(genres, 5)) %>%
  ggplot(aes(genre, review_rating)) +
  geom_boxplot()

# ---- chunk_08 ----
library(tidytext)

horror_movies_unnested <- horror_movies %>%
  unnest_tokens(word, plot) %>%
  anti_join(stop_words, by = "word") %>%
  filter(!is.na(word))

horror_movies_unnested %>%
  filter(!is.na(review_rating)) %>%
  group_by(word) %>%
  summarize(movies = n(),
            avg_rating = mean(review_rating)) %>%
  arrange(desc(movies)) %>%
  filter(movies >= 100) %>%
  mutate(word = fct_reorder(word, avg_rating)) %>%
  ggplot(aes(avg_rating, word)) +
  geom_point()

# ---- chunk_09 ----
library(glmnet)
library(Matrix)

movie_word_matrix <- horror_movies_unnested %>%
  filter(!is.na(review_rating)) %>%
  add_count(word) %>%
  filter(n >= 20) %>%
  count(title, word) %>%
  cast_sparse(title, word, n)

rating <- horror_movies$review_rating[match(rownames(movie_word_matrix), horror_movies$title)]

lasso_model <- cv.glmnet(movie_word_matrix, rating)

# ---- chunk_10 ----
library(broom)

tidy(lasso_model$glmnet.fit) %>%
  filter(term %in% c("quickly", "seek", "army", "teacher", "unexpected", "friends", "evil")) %>%
  ggplot(aes(lambda, estimate, color = term)) +
  geom_line() +
  scale_x_log10() +
  geom_vline(xintercept = lasso_model$lambda.min) +
  geom_hline(yintercept = 0, lty = 2)

# ---- chunk_11 ----
plot(lasso_model)

tidy(lasso_model$glmnet.fit) %>%
  filter(lambda == lasso_model$lambda.min,
         term != "(Intercept)") %>%
  mutate(term = fct_reorder(term, estimate)) %>%
  ggplot(aes(term, estimate)) +
  geom_col() +
  coord_flip()

# ---- chunk_12 ----
features <- horror_movies %>%
  filter(!is.na(review_rating)) %>%
  select(title, genres, director, cast, movie_rating, language, release_country) %>%
  mutate(director = str_remove(director, "Directed by ")) %>%
  gather(type, value, -title) %>%
  filter(!is.na(value)) %>%
  separate_rows(value, sep = "\\| ?") %>%
  unite(feature, type, value, sep = ": ") %>%
  mutate(n = 1)

movie_feature_matrix <- horror_movies_unnested %>%
  filter(!is.na(review_rating)) %>%
  count(title, feature = paste0("word: ", word)) %>%
  bind_rows(features) %>%
  add_count(feature) %>%
  filter(n >= 10) %>%
  cast_sparse(title, feature)

rating <- horror_movies$review_rating[match(rownames(movie_feature_matrix), horror_movies$title)]

feature_lasso_model <- cv.glmnet(movie_feature_matrix, rating)

# ---- chunk_13 ----
plot(feature_lasso_model)

tidy(feature_lasso_model$glmnet.fit) %>%
  filter(lambda == feature_lasso_model$lambda.1se,
         term != "(Intercept)") %>%
  mutate(term = fct_reorder(term, estimate)) %>%
  ggplot(aes(term, estimate)) +
  geom_col() +
  coord_flip() +
  labs(x = "",
       y = "Coefficient for predicting movie rating",
       title = "What affects a horror movie rating?",
       subtitle = "Based on a lasso regression to predict IMDb ratings of ~3000 movies")

# ---- chunk_14 ----
horror_movies %>%
  filter(str_detect(genres, "Comedy"),
         !is.na(movie_rating),
         !is.na(budget),
         movie_rating != "PG") %>%
  arrange(desc(review_rating)) %>%
  select(title, review_rating, movie_rating, plot, director, budget, language) %>%
  View()
