# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----

knitr::opts_chunk$set(echo = TRUE)

library(tidyverse)
library(tidytuesdayR)

# ---- Load ----

tt <- tt_load("2020-12-22")
library(scales)
theme_set(theme_light())

tt$`big-mac` %>%
  View()

big_mac <- tt$`big-mac` %>%
  rename(country = name) %>%
  add_count(country, name = "country_total") %>%
  filter(country_total == max(country_total)) %>%
  arrange(country, date)

# ---- chunk_03 ----
big_mac %>%
  mutate(country = fct_reorder(country, local_price, function(.) last(.) / first(.))) %>%
  ggplot(aes(date, local_price, color = country)) +
  geom_line() +
  expand_limits(y = 0) +
  facet_wrap(~ country, scales = "free_y") +
  theme(legend.position = "none") +
  labs(x = "Time",
       y = "Price of Big Mac in local currency")

# ---- chunk_04 ----
big_mac %>%
  group_by(country) %>%
  summarize(big_mac_inflation = last(local_price) / first(local_price)) %>%
  arrange(desc(big_mac_inflation)) %>%
  mutate(country = fct_reorder(country, big_mac_inflation)) %>%
  ggplot(aes(big_mac_inflation, country)) +
  geom_col() +
  geom_text(aes(label = paste0(round(big_mac_inflation, 1), "X")), hjust = 0) +
  scale_x_log10(breaks = c(1, 3, 10, 30, 100)) +
  expand_limits(x = 130) +
  labs(x = "Price of Big Mac in 2020 / Price of Big Mac in 2000",
       y = "")

# ---- chunk_05 ----
big_mac %>%
  group_by(date) %>%
  mutate(usd_price = local_price[iso_a3 == "USA"],
         us_gdp = gdp_dollar[iso_a3 == "USA"]) %>%
  ungroup() %>%
  mutate(big_mac_ex = local_price / usd_price) %>%
  select(date, iso_a3, country, local_price, dollar_ex, usd_price, big_mac_ex, usd_raw, gdp_dollar, us_gdp, usd_adjusted)

# ---- chunk_06 ----
big_mac %>%
  group_by(date) %>%
  mutate(usd_price = local_price[iso_a3 == "USA"],
         us_gdp = gdp_dollar[iso_a3 == "USA"]) %>%
  ungroup() %>%
  filter(country == "Argentina",
         !is.na(gdp_dollar)) %>%
  mutate(price_from_usd = usd_price * dollar_ex) %>%
  ggplot(aes(date, local_price)) +
  geom_line(aes(color = "Price (in local currency)")) +
  geom_line(aes(y = price_from_usd, color = "Price from USD"))

# ---- chunk_07 ----
big_mac %>%
  filter(country != "United States") %>%
  select(date, country, local_price, dollar_ex, usd_raw, gdp_dollar, usd_adjusted) %>%
  filter(!is.na(gdp_dollar)) %>%
  mutate(country = fct_reorder(country, usd_raw)) %>%
  ggplot(aes(date, usd_adjusted)) +
  geom_line() +
  geom_hline(color = "red", lty = 2, yintercept = 0) +
  expand_limits(y = 0) +
  facet_wrap(~ country) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  labs(y = "GDP-adjusted Big Max Index relative to USD",
       x = "")

library(ggrepel)

big_mac %>%
  filter(date == max(date)) %>%
  ggplot(aes(gdp_dollar, usd_raw)) +
  geom_point() +
  geom_smooth(method = "lm") +
  geom_text_repel(aes(label = country)) +
  labs(x = "GDP per capita (dollars)",
       y = "Raw Big Max Index relative to USD")

# ---- chunk_08 ----
big_mac %>%
  filter(date == max(date)) %>%
  ggplot(aes(gdp_dollar, usd_adjusted)) +
  geom_point() +
  geom_smooth(method = "lm") +
  geom_text_repel(aes(label = country)) +
  labs(x = "GDP per capita (dollars)",
       y = "Adjusted Big Max Index relative to USD")

# ---- chunk_09 ----
library(gganimate)

big_mac %>%
  filter(!is.na(gdp_dollar)) %>%
  ggplot(aes(gdp_dollar, usd_adjusted)) +
  geom_point() +
  geom_smooth(method = "lm") +
  geom_text_repel(aes(label = country)) +
  transition_time(date) +
  labs(x = "GDP per capita (dollars)",
       y = "Adjusted Big Max Index relative to USD",
       title = "{frame_time }")

# ---- chunk_10 ----
big_mac %>%
  filter(date == max(date)) %>%
  mutate(country = fct_reorder(country, usd_adjusted)) %>%
  ggplot(aes(usd_adjusted, country)) +
  geom_col() +
  labs(x = "Big Mac Index relative to USD (GDP-adjusted)",
       y = "")

# ---- chunk_11 ----
big_mac %>%
  select(date, country, local_price, dollar_ex, usd_raw, gdp_dollar,
         ends_with("adjusted")) %>%
  pivot_longer(ends_with("adjusted"), names_to = "base_currency",
               values_to = "adjusted") %>%
  mutate(base_currency = str_to_upper(str_remove(base_currency, "_adjusted"))) %>%
  filter(!is.na(gdp_dollar)) %>%
  mutate(country = fct_reorder(country, adjusted)) %>%
  ggplot(aes(date, adjusted, color = base_currency)) +
  geom_line() +
  geom_hline(color = "red", lty = 2, yintercept = 0) +
  expand_limits(y = 0) +
  facet_wrap(~ country) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  labs(y = "GDP-adjusted Big Max Index relative to each currency",
       x = "",
       color = "Base Currency")

# ---- chunk_12 ----
library(widyr)

big_mac %>%
  pairwise_cor(country, date, local_price, sort = TRUE) %>%
  filter(item1 == "United States")

# ---- Readme ----

tt

# ---- Glimpse ----

tt %>% 
  map(glimpse)

# ---- Wrangle ----

# ---- Visualize ----

# ---- chunk_17 ----

# This will save your most recent plot
ggsave(
  filename = "My TidyTuesday Plot.png",
  device = "png")
