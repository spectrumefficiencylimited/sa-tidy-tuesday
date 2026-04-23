# Auto-generated from the episode R Markdown file.
# This script preserves code chunks in source order for reproducibility checks.

# ---- setup ----
knitr::opts_chunk$set(echo = TRUE)

# ---- chunk_02 ----
library(tidyverse)
library(lubridate)
library(scales)
theme_set(theme_light())

bike_traffic_raw <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-04-02/bike_traffic.csv")

bike_traffic <- bike_traffic_raw %>%
  mutate(date = mdy_hms(date)) %>%
  filter(bike_count < 2000) %>%
  select(-ped_count)

# ---- chunk_03 ----
bike_traffic %>%
  count(crossing, direction)

# ---- chunk_04 ----
bike_traffic %>%
  ggplot(aes(date, fill = is.na(bike_count))) +
  geom_histogram() +
  facet_grid(crossing ~ direction)

# ---- chunk_05 ----
bike_traffic %>%
  group_by(crossing,
           hour = hour(date)) %>%
  summarize(bike_count = sum(bike_count, na.rm = TRUE)) %>%
  mutate(pct_bike = bike_count / sum(bike_count)) %>%
  ggplot(aes(hour, pct_bike, color = crossing)) +
  geom_line() +
  geom_point() +
  scale_y_continuous(labels = percent_format()) +
  labs(title = "When in the day do people bike through these Seattle crossings?",
       subtitle = "Based on crossings from 2014-February 2019",
       color = "Crossing",
       x = "Time of day (local time)",
       y = "% of bike crossings that happen in this hour")

# ---- chunk_06 ----
bike_by_time_window <- bike_traffic %>%
  mutate(hour = hour(date)) %>%
  mutate(time_window = case_when(
    between(hour, 7, 10) ~ "Morning Commute",
    between(hour, 11, 15) ~ "Midday",
    between(hour, 16, 18) ~ "Evening Commute",
    TRUE ~ "Night"
  )) %>%
  group_by(crossing,
           time_window) %>%
  summarize(number_missing = sum(is.na(bike_count)),
            bike_count = sum(bike_count, na.rm = TRUE)) %>%
  mutate(pct_bike = bike_count / sum(bike_count))

bike_by_time_window %>%
  select(-number_missing, -bike_count) %>%
  spread(time_window, pct_bike) %>%
  mutate(TotalCommute = `Evening Commute` + `Morning Commute`) %>%
  arrange(desc(TotalCommute))

bike_by_time_window %>%
  ggplot(aes(time_window, pct_bike)) +
  geom_col() +
  coord_flip() +
  facet_wrap(~ crossing)

bike_by_time_window %>%
  group_by(crossing) %>%
  summarize(total_bikes = sum(bike_count),
            pct_commute = sum(bike_count[str_detect(time_window, "Commute")]) / total_bikes) %>%
  ggplot(aes(total_bikes, pct_commute)) +
  geom_point() +
  scale_x_log10()

# ---- chunk_07 ----
bike_traffic %>%
  group_by(crossing,
           weekday = wday(date, label = TRUE),
           hour = hour(date)) %>%
  summarize(total_bikes = sum(bike_count, na.rm = TRUE)) %>%
  group_by(crossing) %>%
  mutate(pct_bike = total_bikes / sum(total_bikes)) %>%
  ggplot(aes(hour, pct_bike, color = crossing)) +
  geom_line(show.legend = FALSE) +
  facet_grid(crossing ~ weekday) +
  scale_y_continuous(labels = percent_format()) +
  labs(x = "Time of week",
       y = "% of bike crossings happening in this hour",
       title = "When in the week do people in Seattle bike?",
       subtitle = "Based on crossings from 2014-February 2019")

# ---- chunk_08 ----
bike_traffic %>%
  filter(date < "2018-01-01") %>%
  group_by(crossing,
           month = fct_relevel(month.name[month(date)], month.name)) %>%
  summarize(total_bikes = sum(bike_count, na.rm = TRUE)) %>%
  mutate(pct_bike = total_bikes / sum(total_bikes)) %>%
  ggplot(aes(month, pct_bike, color = crossing, group = crossing)) +
  geom_line() +
  expand_limits(y = 0) +
  scale_y_continuous(labels = percent_format()) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
  labs(title = "What time of year do people bike?",
       subtitle = "Based on 2014-2017 bike crossings",
       y = "% of yearly trips in this month",
       x = "")

# ---- chunk_09 ----
bike_by_direction_hour_crossing <- bike_traffic %>%
  filter(crossing != "MTS Trail",
         !wday(date, label = TRUE) %in% c("Sat", "Sun"),
         direction %in% c("North", "South")) %>%
  mutate(hour = hour(date)) %>%
  group_by(crossing,
           direction,
           hour) %>%
  summarize(bike_count = sum(bike_count, na.rm = TRUE)) %>%
  mutate(pct_bike = bike_count / sum(bike_count))

bike_by_direction_hour_crossing %>%
  group_by(crossing) %>%
  mutate(average_hour = sum((hour * pct_bike)[direction == "North"])) %>%
  ungroup() %>%
  mutate(crossing = fct_reorder(crossing, average_hour)) %>%
  ggplot(aes(hour, pct_bike, color = direction)) +
  geom_line() +
  facet_grid(crossing ~ .) +
  scale_y_continuous(labels = percent_format()) +
  labs(x = "Time of day",
       y = "% of bike crossings happening in this hour",
       title = "In which directions do people commute by bike?",
       subtitle = "Based on weekday crossings at six Seattle locations from 2014-February 2019",
       color = "Direction")
