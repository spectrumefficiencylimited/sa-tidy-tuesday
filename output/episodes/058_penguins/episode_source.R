# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)
theme_set(theme_light())

# ---- Load ----

tt <- tt_load("2020-07-28")

# ---- chunk_03 ----
penguins <- tt$penguins

# ---- chunk_04 ----
penguins %>%
  count(species, sort = TRUE)

penguins %>%
  count(island, sort = TRUE)

penguins_pivoted <- penguins %>%
  pivot_longer(cols = bill_length_mm:body_mass_g,
               names_to = "metric",
               values_to = "value")

penguins_pivoted %>%
  ggplot(aes(value, fill = species)) +
  geom_histogram(bins = 20) +
  facet_wrap(~ metric, scales = "free_x")

penguins_pivoted %>%
  ggplot(aes(value, fill = species)) +
  geom_density(alpha = .5) +
  facet_wrap(~ metric, scales = "free")

penguins_pivoted %>%
  ggplot(aes(species, value)) +
  geom_boxplot() +
  facet_wrap(~ metric, scales = "free_y")

# ---- chunk_05 ----
penguins %>%
  ggplot(aes(year, fill = species)) +
  geom_bar()

penguins %>%
  ggplot(aes(island, fill = species)) +
  geom_bar()

# ---- chunk_06 ----
library(tidymodels)

set.seed(2020)
split <- penguins %>%
  filter(!is.na(bill_length_mm)) %>%
  mutate(species = fct_lump(species, 1)) %>%
  initial_split()

training_data <- training(split)

splits <- training_data %>%
  rsample::vfold_cv(v = 10)

my_metrics <- metric_set(accuracy, kap, roc_auc)
control <- control_resamples(extract = extract_model,
                             save_pred = TRUE)
logistic_spec <- logistic_reg(mode = "classification") %>%
  set_engine("glm")

logistic_model <- logistic_spec %>%
  fit_resamples(species ~ bill_length_mm,
                resamples = splits,
                metrics = my_metrics)

logistic_model_extended <- logistic_spec %>%
  fit_resamples(species ~ bill_length_mm + bill_depth_mm +
                  flipper_length_mm + body_mass_g,
                resamples = splits,
                metrics = my_metrics)

nn <- nearest_neighbor(mode = "classification",
                 neighbors = 10) %>%
  set_engine("kknn") %>%
  fit_resamples(species ~ bill_length_mm + bill_depth_mm +
                  flipper_length_mm + body_mass_g,
                resamples = splits,
                metrics = my_metrics)

dt <- decision_tree(mode = "classification") %>%
  set_engine("rpart") %>%
  fit_resamples(species ~ bill_length_mm + bill_depth_mm +
                  flipper_length_mm + body_mass_g,
                resamples = splits,
                control = control,
                metrics = my_metrics)

# Look at one decision tree
dt$.extracts[[1]]$.extracts[[1]]

bind_rows(
  collect_metrics(logistic_model) %>% mutate(model = "Logistic: bill length"),
  collect_metrics(logistic_model_extended) %>% mutate(model = "Logistic: 4 predictors"),
  collect_metrics(nn) %>% mutate(model = "KNN: 10 neighbors"),
  collect_metrics(dt) %>% mutate(model = "Decision Tree")
) %>%
  ggplot(aes(mean, .metric, color = model)) +
  geom_point() +
  geom_errorbarh(aes(xmin = mean - std_err,
                     xmax = mean + std_err)) +
  labs(title = "Cross validated accuracy metrics across models",
       x = "Estimated metric (+/- standard error)",
       y = "")

# ---- chunk_07 ----
knn_trained <- nearest_neighbor(mode = "classification",
                 neighbors = 10) %>%
  set_engine("kknn") %>%
  fit(species ~ bill_length_mm + bill_depth_mm +
                  flipper_length_mm + body_mass_g,
      data = training(split))

predictions <- bind_cols(predict(knn_trained, new_data = testing(split)),
                         predict(knn_trained, new_data = testing(split), type = "prob")) %>%
  bind_cols(testing(split))

metric_set(kap, accuracy)(predictions, species, estimate = .pred_class)
metric_set(roc_auc)(predictions, species, .pred_Adelie)

predictions %>%
  ggplot(aes(species, .pred_Adelie)) +
  geom_boxplot()

# ---- chunk_08 ----
split_multiclass <- penguins %>%
  filter(!is.na(bill_length_mm)) %>%
  mutate(species = factor(species)) %>%
  initial_split()

splits_multiclass <- training(split_multiclass) %>%
  vfold_cv(10)

multiclass <- multinom_reg(penalty = 0) %>%
  set_engine("glmnet") %>%
  fit_resamples(species ~ bill_length_mm + bill_depth_mm +
                  flipper_length_mm + body_mass_g,
                resamples = splits_multiclass,
                control = control,
                metrics = my_metrics)

multiclass %>%
  unnest(.predictions) %>%
  pivot_longer(cols = c(.pred_Adelie, .pred_Chinstrap, .pred_Gentoo),
               names_to = "predicted_class",
               values_to = "prob") %>%
  ggplot(aes(predicted_class, prob)) +
  geom_boxplot() +
  facet_wrap(~ species)

# ---- chunk_09 ----
predict(model, new_data = testing(split)) %>%
  bind_cols(testing(split)) %>%
  metrics(species, .pred_class)

# ---- chunk_10 ----
library(modeldata)
data("lending_club")
lr_mod <- logistic_reg()

using_formula <-
  lr_mod %>%
  set_engine("glm") %>%
  fit(Class ~ funded_amnt + int_rate, data = lending_club)

using_formula
