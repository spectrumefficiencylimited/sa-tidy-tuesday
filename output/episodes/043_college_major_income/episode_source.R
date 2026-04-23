# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----
knitr::opts_chunk$set(echo = TRUE)

# ---- chunk_02 ----
library(tidyverse)
library(scales)

theme_set(theme_light())

# ---- chunk_03 ----
recent_grads <- read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2018-10-16/recent-grads.csv")

majors_processed <- recent_grads %>%
  arrange(desc(Median)) %>%
  mutate(Major = str_to_title(Major),
         Major = fct_reorder(Major, Median))

# ---- by_major_category ----
by_major_category <- majors_processed %>%
  filter(!is.na(Total)) %>%
  group_by(Major_category) %>%
  summarize(Men = sum(Men),
            Women = sum(Women),
            Total = sum(Total),
            MedianSalary = sum(Median * Sample_size) / sum(Sample_size)) %>%
  mutate(ShareWomen = Women / Total) %>%
  arrange(desc(ShareWomen))

# ---- chunk_05 ----
majors_processed %>%
  mutate(Major_category = fct_reorder(Major_category, Median)) %>%
  ggplot(aes(Major_category, Median, fill = Major_category)) +
  geom_boxplot() +
  scale_y_continuous(labels = dollar_format()) +
  expand_limits(y = 0) +
  coord_flip() +
  theme(legend.position = "none")

# ---- chunk_06 ----
majors_processed %>%
  filter(Sample_size >= 100) %>%
  head(20) %>%
  ggplot(aes(Major, Median, color = Major_category)) +
  geom_point() +
  geom_errorbar(aes(ymin = P25th, ymax = P75th)) +
  expand_limits(y = 0) +
  scale_y_continuous(labels = dollar_format()) +
  coord_flip() +
  labs(title = "What are the highest-earning majors?",
       subtitle = "Top 20 majors with at least 100 graduates surveyed. Bars represent the 25th to 75th percentile.",
       x = "",
       y = "Median salary of gradates")

# ---- chunk_07 ----
majors_processed %>%
  arrange(desc(Total)) %>%
  head(20) %>%
  mutate(Major = fct_reorder(Major, Total)) %>%
  gather(Gender, Number, Men, Women) %>%
  ggplot(aes(Major, Number, fill = Gender)) +
  geom_col() +
  coord_flip()

# ---- chunk_08 ----
library(ggrepel)

by_major_category %>%
  mutate(Major_category = fct_lump(Major_category, 6)) %>%
  ggplot(aes(ShareWomen, MedianSalary, color = Major_category)) +
  geom_point() +
  geom_smooth(method = "lm") +
  geom_text_repel(aes(label = Major_category), force = .2) +
  expand_limits(y = 0)

# ---- chunk_09 ----
library(plotly)

g <- majors_processed %>%
  mutate(Major_category = fct_lump(Major_category, 4)) %>%
  ggplot(aes(ShareWomen, Median, color = Major_category, size = Sample_size, label = Major)) +
  geom_point() +
  geom_smooth(aes(group = 1), method = "lm") +
  scale_x_continuous(labels = percent_format()) +
  scale_y_continuous(labels = dollar_format()) +
  expand_limits(y = 0)

ggplotly(g)

# ---- chunk_10 ----
majors_processed %>%
  select(Major, Total, ShareWomen, Sample_size, Median) %>%
  lm(Median ~ ShareWomen, data = ., weights = Sample_size) %>%
  summary()

# ---- chunk_11 ----
library(broom)

majors_processed %>%
  select(Major, Major_category, Total, ShareWomen, Sample_size, Median) %>%
  add_count(Major_category) %>%
  filter(n >= 10) %>%
  nest(-Major_category) %>%
  mutate(model = map(data, ~ lm(Median ~ ShareWomen, data = ., weights = Sample_size)),
         tidied = map(model, tidy)) %>%
  unnest(tidied) %>%
  filter(term == "ShareWomen") %>%
  arrange(estimate) %>%
  mutate(fdr = p.adjust(p.value, method = "fdr"))

# ---- chunk_12 ----
majors_processed %>%
  filter(Sample_size >= 100) %>%
  mutate(IQR = P75th - P25th) %>%
  arrange(desc(IQR))

# ---- chunk_13 ----
majors_processed %>%
  ggplot(aes(Sample_size, Median)) +
  geom_point() +
  geom_text(aes(label = Major), check_overlap = TRUE, vjust = 1, hjust = 1) +
  scale_x_log10()

# ---- chunk_14 ----
knitr::knit_exit()

# ---- chunk_15 ----
majors_processed %>%
  mutate(Major = fct_reorder(Major, Total)) %>%
  arrange(desc(Total)) %>%
  head(20) %>%
  ggplot(aes(Major, Total, fill = Major_category)) +
  geom_col() +
  coord_flip() +
  scale_y_continuous(labels = comma_format()) +
  labs(x = "",
       y = "Total # of graduates")

# ---- chunk_16 ----
majors_processed %>%
  group_by(Major_category) %>%
  summarize(Median = median(Median)) %>%
  mutate(Major_category = fct_reorder(Major_category, Median)) %>%
  ggplot(aes(Major_category, Median)) +
  geom_col() +
  scale_y_continuous(labels = dollar_format()) +
  coord_flip()

# ---- chunk_17 ----
majors_processed %>%
  filter(Sample_size >= 100) %>%
  tail(20) %>%
  ggplot(aes(Major, Median, color = Major_category)) +
  geom_point() +
  geom_errorbar(aes(ymin = P25th, ymax = P75th)) +
  expand_limits(y = 0) +
  coord_flip()
