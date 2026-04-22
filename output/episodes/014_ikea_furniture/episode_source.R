# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)
library(scales)
theme_set(theme_light())

# ---- Load ----

tt <- tt_load("2020-11-03")

# ---- chunk_03 ----
ikea <- tt$ikea %>%
  select(-X1) %>%
  mutate(price_usd = 0.27 * price,
         short_description = str_squish(short_description)) %>%
  add_count(category, name = "category_total")

ikea %>%
  count(category, sort = TRUE) %>%
  mutate(category = fct_reorder(category, n)) %>%
  ggplot(aes(n, category)) +
  geom_col() +
  labs(x = "# of items",
       y = "",
       title = "Most common categories of IKEA items")

# ---- chunk_04 ----
library(glue)

ikea %>%
  mutate(category = glue("{ category } ({ category_total })"),
         category = fct_reorder(category, price_usd)) %>%
  ggplot(aes(price_usd, category)) +
  geom_boxplot() +
  # geom_jitter(width = 0, height = .1, alpha = .25) +
  scale_x_log10(labels = dollar) +
  labs(x = "Price (USD)",
       y = "",
       title = "How much do items in each category cost?")

# ---- chunk_05 ----
library(ggridges)

ikea %>%
  mutate(category = glue("{ category } ({ category_total })"),
         category = fct_reorder(category, price_usd)) %>%
  ggplot(aes(price_usd, category)) +
  geom_density_ridges() +
  # geom_jitter(width = 0, height = .1, alpha = .25) +
  scale_x_log10(labels = dollar) +
  labs(x = "Price (USD)",
       y = "",
       title = "How much do items in each category cost?")

# ---- chunk_06 ----
ikea %>%
  mutate(category = glue("{ category } ({ category_total })"),
         category = fct_reorder(category, price_usd)) %>%
  ggplot(aes(price_usd, category, fill = other_colors)) +
  geom_density_ridges(alpha = .5) +
  # geom_jitter(width = 0, height = .1, alpha = .25) +
  scale_x_log10(labels = dollar) +
  labs(x = "Price (USD)",
       y = "",
       title = "How much do items in each category cost?")

# ---- chunk_07 ----
ikea %>%
  mutate(name = fct_lump(name, 20)) %>%
  filter(name != "Other") %>%
  count(name, category, sort = TRUE) %>%
  mutate(name = fct_reorder(name, n, sum),
         category = fct_reorder(category, n, sum)) %>%
  ggplot(aes(n, name, fill = category)) +
  geom_col() +
  scale_fill_discrete(guide = guide_legend(reverse = TRUE)) +
  labs(x = "# of items",
       y = "Name of item")

# ---- chunk_08 ----
ikea %>%
  separate(short_description,
           c("main_description", "rest"),
           sep = ", ",
           extra = "merge",
           fill = "right",
           remove = FALSE) %>%
  extract(rest, "description_cm", "([\\d\\-xX]+) cm", remove = FALSE) %>%
  unite(category_and_description, category, main_description, sep = " - ") %>%
  count(category_and_description, sort = TRUE)

# ---- chunk_09 ----
ikea_volume <- ikea %>%
  mutate(volume_m3 = depth * height * width / 1e6) %>%
  filter(!is.na(volume_m3),
         volume_m3 >= .001) %>%
  arrange(desc(volume_m3)) %>%
  add_count(category, name = "category_total")

ikea_volume %>%
  arrange(desc(volume_m3))

ikea_volume %>%
  mutate(category = glue("{ category } ({ category_total })"),
         category = fct_reorder(category, volume_m3)) %>%
  ggplot(aes(volume_m3, category)) +
  geom_boxplot() +
  # geom_jitter(width = 0, height = .1, alpha = .25) +
  scale_x_log10() +
  labs(x = "Volume of furniture (cubic meters)",
       y = "",
       title = "How much space do items in each category take up?")

# ---- chunk_10 ----
ikea_volume %>%
  mutate(category = fct_lump(category, 6)) %>%
  ggplot(aes(volume_m3, price_usd, color = category)) +
  geom_point() +
  geom_smooth(method = "lm") +
  scale_x_log10() +
  scale_y_log10()

ikea_volume %>%
  mutate(dollar_per_m3 = price_usd / volume_m3) %>%
  arrange(desc(dollar_per_m3)) %>%
  View()

# ---- chunk_11 ----
ikea %>%
  group_by(designer) %>%
  summarize(n_items = n(),
            n_names = n_distinct(name),
            n_category = n_distinct(category)) %>%
  arrange(desc(n_names))

# ---- chunk_12 ----
library(broom)

ikea_volume %>%
  mutate(category = fct_relevel(category, "Tables & desks")) %>%
  lm(log2(price_usd) ~ log2(volume_m3) + category + other_colors, data = .) %>%
  tidy(conf.int = TRUE) %>%
  filter(term != "(Intercept)") %>%
  mutate(term = ifelse(term == "log2(volume_m3)", "Item volume (doubling)", term),
         term = str_remove(term, "^category")) %>%
  mutate(term = fct_reorder(term, estimate)) %>%
  ggplot(aes(estimate, term)) +
  geom_point() +
  geom_errorbarh(aes(xmin = conf.low, xmax = conf.high), height = .1) +
  geom_vline(xintercept = 0, color = "red", lty = 2) +
  labs(x = "Impact on price (relative to Tables & desks)",
       y = "",
       title = "What objects are unusually expensive/inexpensive relative to volume?")
