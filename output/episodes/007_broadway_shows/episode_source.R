# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----
knitr::opts_chunk$set(echo = TRUE)

# ---- chunk_02 ----
library(tidyverse)
library(scales)
theme_set(theme_light())

tuesdata <- tidytuesdayR::tt_load('2020-04-28')

# ---- chunk_03 ----
grosses <- tuesdata$grosses

grosses %>%
  filter(show %in% c("Hamilton", "The Lion King")) %>%
  ggplot(aes(week_ending, weekly_gross, color = show)) +
  geom_line() +
  scale_y_continuous(labels = scales::dollar) +
  expand_limits(y = 0)

# ---- chunk_04 ----
# devtools::install_github("ramnathv/tidymetrics")
library(tidymetrics)

shows_summarized <- grosses %>%
  filter(show %in% c("Hamilton", "The Lion King",
                     "Les Miserables", "Rent",
                     "The Phantom of the Opera", "Wicked",
                     "Harry Potter and the Cursed Child, Parts One and Two",
                     "The Book of Mormon")) %>%
  mutate(show = str_remove(show, "\\, Parts.*")) %>%
  rename(date = week_ending) %>%
  cross_by_dimensions(show) %>%
  cross_by_periods(c("month", "quarter", "year"),
                   windows = 28) %>%
  summarize(usd_gross = sum(weekly_gross),
            avg_ticket_price = mean(avg_ticket_price),
            pct_capacity = mean(pct_capacity)) %>%
  ungroup()

show_metrics <- create_metrics(shows_summarized)

# ---- chunk_05 ----
# devtools::install_github("ramnathv/shinymetrics")
library(shinymetrics)
saveRDS(show_metrics, "broadway-shinybones/show_metrics.rds")

preview_metric(show_metrics$broadway_revenue_usd_gross)
preview_metric(show_metrics$broadway_revenue_avg_ticket_price)
preview_metric(show_metrics$broadway_revenue_pct_capacity)

# ---- chunk_06 ----
shows_summarized %>%
  filter(period == "quarter",
         show != "All") %>%
  ggplot(aes(date, usd_gross, fill = show)) +
  geom_col()

shows_summarized %>%
  filter(period == "quarter",
         show != "All") %>%
  ggplot(aes(date, avg_ticket_price, col = show)) +
  geom_line() +
  expand_limits(y = 0)
