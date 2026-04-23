# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----
knitr::opts_chunk$set(echo = TRUE)

# ---- chunk_02 ----
library(tidyverse)
theme_set(theme_light())

# ---- chunk_03 ----
big_epa_cars <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-10-15/big_epa_cars.csv") %>%
  mutate(uses_electricity = ifelse(highwayE > 0, "Uses Electricity", "Doesn't Use Electricity"))

# ---- chunk_04 ----
big_epa_cars_alphabetical <- big_epa_cars %>%
  select(sort(colnames(big_epa_cars)))

# ---- chunk_05 ----
big_epa_cars %>%
  ggplot(aes(highway08, city08)) +
  geom_point() +
  geom_abline(color = "red") +
  facet_wrap(~ uses_electricity, scales = "free") +
  expand_limits(x = 0, y = 0) +
  labs(x = "Highway MPG",
       y = "City MPG",
       title = "How does fuel efficiency differ between city + highway?")

# ---- chunk_06 ----
big_epa_cars %>%
  select(city08, highway08, make, model, cylinders, displ, drive, engId, eng_dscr)

# ---- chunk_07 ----
big_epa_cars %>%
  filter(cityE == 0) %>%
  mutate(VClass = fct_lump(VClass, 8),
         VClass = fct_reorder(VClass, city08)) %>%
  ggplot(aes(VClass, city08)) +
  geom_boxplot() +
  coord_flip()

big_epa_cars %>%
  filter(cityE == 0) %>%
  mutate(drive = fct_reorder(drive, city08)) %>%
  ggplot(aes(drive, city08)) +
  geom_boxplot() +
  coord_flip()

big_epa_cars %>%
  filter(cityE == 0) %>%
  ggplot(aes(cylinders, city08, group = cylinders)) +
  geom_boxplot()

big_epa_cars %>%
  filter(cityE == 0) %>%
  ggplot(aes(displ, city08)) +
  geom_point() +
  expand_limits(x = 0, y = 0)

# ---- chunk_08 ----
# Cross validation holdout set
non_electric_cars <- big_epa_cars %>%
  filter(cityA08 == 0,
         cityE == 0) %>%
  sample_frac(1)

training_set <- non_electric_cars %>%
  filter(row_number() %% 5 != 0)

# ---- chunk_09 ----
library(broom)

training_set %>%
  ggplot(aes(displ, city08)) +
  geom_point() +
  geom_smooth(method = "lm")

library(splines)
augmented_data <- lm(city08 ~ ns(displ, 2), data = training_set) %>%
  augment(data = training_set)

augmented_data %>%
  ggplot(aes(displ, city08)) +
  geom_point() +
  geom_line(aes(y = .fitted), color = "red", size = 2)

models <- tibble(df = 1:10) %>%
  mutate(lm_model = map(df, ~ lm(city08 ~ ns(displ, df = .), data = training_set)))

augmented_unnested <- models %>%
  mutate(augmented = map(lm_model, augment, data = training_set)) %>%
  unnest(augmented)

augmented_unnested %>%
  ggplot(aes(displ, city08)) +
  geom_point(data = training_set) +
  geom_line(aes(y = .fitted, color = factor(df)), size = 2) +
  labs(x = "Engine volume (L)",
       y = "City MPG",
       color = "# of degrees of freedom") +
  expand_limits(x = 0, y = 0)

augmented_unnested %>%
  ggplot(aes(displ, .resid)) +
  geom_point() +
  facet_wrap(~ df)

glanced_models <- models %>%
  rename(spline_df = df) %>%
  mutate(glanced = map(lm_model, glance, data = training_set)) %>%
  unnest(glanced)

glanced_models %>%
  ggplot(aes(spline_df, adj.r.squared)) +
  geom_line()

# ---- chunk_10 ----
lm(city08 ~ ns(displ, 4), data = training_set) %>%
  anova() %>%
  tidy() %>%
  mutate(pct_variation = sumsq / sum(sumsq))

ggplot(training_set, aes(cylinders, displ, group = cylinders)) +
  geom_boxplot()

# ---- chunk_11 ----
training_set %>%
  ggplot(aes(year, city08)) +
  geom_point() +
  geom_smooth(method = "loess")

efficiency_time <- training_set %>%
  mutate(VClass = fct_lump(VClass, 6),
         guzzler = !is.na(guzzler)) %>%
  group_by(year = 2 * floor(year / 2), VClass) %>%
  summarize_at(vars(city08, cylinders, displ, guzzler), mean)

efficiency_time %>%
  ggplot(aes(year, city08, color = VClass)) +
  geom_line() +
  expand_limits(y = 0)

efficiency_time %>%
  ggplot(aes(year, displ, color = VClass)) +
  geom_line() +
  expand_limits(y = 0)

efficiency_time %>%
  ggplot(aes(year, guzzler, color = VClass)) +
  geom_line() +
  expand_limits(y = 0)
