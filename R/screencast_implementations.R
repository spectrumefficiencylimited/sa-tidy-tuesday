# Implementations for selected screencast episodes

#' Himalayan climbers analysis
#' @description Analyze the 2020-09-22 TidyTuesday Himalayan climbers dataset.
#' @details Loads the weekly data if a named list is not provided.
#' @param data A named list from tidytuesdayR::tt_load() containing at least `peaks` and `expeditions`.
#' @param week A TidyTuesday week string to load if `data` is NULL. Defaults to "2020-09-22".
#' @param ... Additional arguments passed to lower-level helpers.
#' @return A list containing the prepared data, summary tables, and ggplot objects.
#' @export
himalayan_climbers <- function(data = NULL, week = "2020-09-22", ...) {
  if (is.null(data)) {
    data <- load_tidyweek_data(week)
  }

  if (!is.list(data) || !all(c("peaks", "expeditions") %in% names(data))) {
    stop("data must be a named list containing at least 'peaks' and 'expeditions'.")
  }

  peaks <- data$peaks %>%
    dplyr::rename(height_meters = height_metres)

  peaks_plot <- peaks %>%
    dplyr::arrange(dplyr::desc(height_meters)) %>%
    dplyr::slice_head(n = 50) %>%
    dplyr::mutate(peak_name = forcats::fct_reorder(peak_name, height_meters)) %>%
    ggplot2::ggplot(ggplot2::aes(height_meters, peak_name, fill = climbing_status)) +
    ggplot2::geom_col() +
    ggplot2::labs(
      x = "Height (meters)",
      y = "",
      title = "Tallest peaks in the Himalayas",
      fill = ""
    ) +
    ggplot2::theme_light()

  na_reasons <- c("Unknown", "Attempt rumoured", "Did not attempt climb", "Did not reach base camp")

  expeditions <- data$expeditions %>%
    dplyr::mutate(
      success = dplyr::case_when(
        stringr::str_detect(termination_reason, "Success") ~ "Success",
        termination_reason %in% na_reasons ~ "Other",
        TRUE ~ "Failure"
      ),
      days_to_highpoint = as.integer(highpoint_date - basecamp_date)
    )

  termination_counts <- expeditions %>%
    dplyr::count(termination_reason, sort = TRUE)

  expedition_duration_plot <- plot_days_to_highpoint(expeditions)

  peaks_summarized <- expeditions %>%
    dplyr::group_by(peak_id, peak_name) %>%
    summarize_expeditions() %>%
    dplyr::ungroup() %>%
    dplyr::arrange(dplyr::desc(n_climbs)) %>%
    dplyr::inner_join(peaks %>% dplyr::select(peak_id, height_meters), by = "peak_id")

  list(
    peaks = peaks,
    expeditions = expeditions,
    peaks_plot = peaks_plot,
    termination_counts = termination_counts,
    expedition_duration_plot = expedition_duration_plot,
    peaks_summarized = peaks_summarized
  )
}

#' Beyonce and Taylor Swift lyrics analysis
#' @description Analyze the 2020-09-29 TidyTuesday Beyonce and Taylor Swift lyrics dataset.
#' @details Loads the remote CSV files if a named list is not provided.
#' @param data A named list containing `beyonce_lyrics`, `taylor_swift_lyrics`, `sales`, and `charts`.
#' @param ... Additional arguments passed to lower-level helpers.
#' @return A list containing processed datasets, comparison tables, and ggplot objects.
#' @export
beyonce_taylor_swift_lyrics <- function(data = NULL, ...) {
  if (is.null(data)) {
    data <- list(
      beyonce_lyrics = load_remote_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-09-29/beyonce_lyrics.csv'),
      taylor_swift_lyrics = load_remote_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-09-29/taylor_swift_lyrics.csv'),
      sales = load_remote_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-09-29/sales.csv'),
      charts = load_remote_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-09-29/charts.csv')
    )
  }

  required_names <- c('beyonce_lyrics', 'taylor_swift_lyrics', 'sales', 'charts')
  if (!is.list(data) || !all(required_names %in% names(data))) {
    stop("data must be a named list containing: ", paste(required_names, collapse = ", "))
  }

  sales_plot_us <- data$sales %>%
    dplyr::filter(country == "US") %>%
    dplyr::mutate(title = forcats::fct_reorder(title, sales)) %>%
    ggplot2::ggplot(ggplot2::aes(sales, title, fill = artist)) +
    ggplot2::geom_col() +
    ggplot2::scale_x_continuous(labels = scales::dollar) +
    ggplot2::labs(x = "Sales (US)", y = "") +
    ggplot2::theme_light()

  sales_plot_world <- data$sales %>%
    dplyr::filter(country %in% c("World", "WW")) %>%
    dplyr::mutate(title = forcats::fct_reorder(title, sales)) %>%
    ggplot2::ggplot(ggplot2::aes(sales, title, fill = artist)) +
    ggplot2::geom_col() +
    ggplot2::scale_x_continuous(labels = scales::dollar) +
    ggplot2::labs(x = "Sales (World)", y = "") +
    ggplot2::theme_light()

  release_dates <- data$charts %>%
    dplyr::distinct(album = title, released) %>%
    dplyr::mutate(album = dplyr::recode(album,
                                       folklore = "Folklore",
                                       reputation = "Reputation"),
                  released = stringr::str_remove(released, " \\(.*"),
                  released = lubridate::mdy(released))

  taylor_swift_words <- data$taylor_swift_lyrics %>%
    dplyr::rename_with(stringr::str_to_lower) %>%
    dplyr::select(-artist) %>%
    prepare_lyrics_tokens(text_col = "lyrics") %>%
    dplyr::inner_join(release_dates, by = "album") %>%
    dplyr::mutate(album = forcats::fct_reorder(album, released))

  ts_top_words_plot <- taylor_swift_words %>%
    dplyr::count(word, sort = TRUE) %>%
    dplyr::slice_head(n = 25) %>%
    dplyr::mutate(word = forcats::fct_reorder(word, n)) %>%
    ggplot2::ggplot(ggplot2::aes(n, word)) +
    ggplot2::geom_col() +
    ggplot2::theme_light()

  ts_tf_idf <- taylor_swift_words %>%
    dplyr::count(album, word) %>%
    compute_tf_idf(document_col = "album", term_col = "word", count_col = "n") %>%
    dplyr::arrange(dplyr::desc(tf_idf))

  ts_tf_idf_plot <- ts_tf_idf %>%
    dplyr::group_by(album) %>%
    dplyr::slice_max(tf_idf, n = 10, with_ties = FALSE) %>%
    dplyr::ungroup() %>%
    tidytext::reorder_within(word, tf_idf, album) %>%
    ggplot2::ggplot(ggplot2::aes(tf_idf, word)) +
    ggplot2::geom_col() +
    ggplot2::facet_wrap(~ album, scales = "free_y") +
    tidytext::scale_y_reordered() +
    ggplot2::theme_light()

  ts_log_odds <- taylor_swift_words %>%
    dplyr::count(album, word) %>%
    compute_log_odds(group_col = "album", term_col = "word", count_col = "n") %>%
    dplyr::arrange(dplyr::desc(log_odds_weighted))

  ts_log_odds_plot <- ts_log_odds %>%
    dplyr::group_by(album) %>%
    dplyr::slice_max(log_odds_weighted, n = 10, with_ties = FALSE) %>%
    dplyr::ungroup() %>%
    tidytext::reorder_within(word, log_odds_weighted, album) %>%
    ggplot2::ggplot(ggplot2::aes(log_odds_weighted, word)) +
    ggplot2::geom_col() +
    ggplot2::facet_wrap(~ album, scales = "free_y") +
    tidytext::scale_y_reordered() +
    ggplot2::theme_light()

  beyonce <- data$beyonce_lyrics %>%
    dplyr::select(artist = artist_name, song = song_name, lyrics = line)

  ts <- data$taylor_swift_lyrics %>%
    dplyr::rename_with(stringr::str_to_lower) %>%
    dplyr::rename(song = title) %>%
    dplyr::select(-album)

  artist_song_words <- dplyr::bind_rows(ts, beyonce) %>%
    tidytext::unnest_tokens(word, lyrics) %>%
    dplyr::count(artist, song, word) %>%
    dplyr::anti_join(tidytext::stop_words, by = "word")

  by_artist_word <- artist_song_words %>%
    dplyr::group_by(artist, word) %>%
    dplyr::summarize(
      num_songs = dplyr::n(),
      num_words = sum(n),
      .groups = "drop_last"
    ) %>%
    dplyr::mutate(pct_words = num_words / sum(num_words)) %>%
    dplyr::group_by(word) %>%
    dplyr::mutate(num_words_total = sum(num_words)) %>%
    dplyr::ungroup()

  word_differences <- by_artist_word %>%
    compute_log_odds(group_col = "artist", term_col = "word", count_col = "num_words") %>%
    dplyr::arrange(dplyr::desc(abs(log_odds_weighted))) %>%
    dplyr::filter(artist == "Beyoncé") %>%
    dplyr::slice_max(num_words_total, n = 100, with_ties = FALSE) %>%
    dplyr::slice_max(abs(log_odds_weighted), n = 25, with_ties = FALSE) %>%
    dplyr::mutate(word = forcats::fct_reorder(word, log_odds_weighted),
                  direction = ifelse(log_odds_weighted > 0, "Beyoncé", "Taylor Swift"))

  word_differences_plot <- word_differences %>%
    ggplot2::ggplot(ggplot2::aes(log_odds_weighted, word, fill = direction)) +
    ggplot2::geom_col() +
    ggplot2::scale_x_continuous(breaks = log(2 ^ seq(-6, 9, 3)),
                                labels = paste0(2 ^ abs(seq(-6, 9, 3)), "X")) +
    ggplot2::labs(
      x = "Relative use in Beyoncé vs Taylor Swift (weighted)",
      y = "",
      title = "Which words most distinguish Beyoncé and Taylor Swift songs?",
      subtitle = "Among the 100 words most used by the artists (combined)",
      fill = ""
    ) +
    ggplot2::theme_light()

  comparison <- by_artist_word %>%
    dplyr::select(artist, word, pct_words, num_words_total) %>%
    tidyr::pivot_wider(names_from = artist, values_from = pct_words, values_fill = list(pct_words = 0)) %>%
    janitor::clean_names() %>%
    dplyr::slice_max(num_words_total, n = 200, with_ties = FALSE)

  comparison_scatter_plot <- comparison %>%
    ggplot2::ggplot(ggplot2::aes(taylor_swift, beyonce)) +
    ggplot2::geom_abline(color = "red") +
    ggplot2::geom_point() +
    ggplot2::geom_text(ggplot2::aes(label = word), vjust = 1, hjust = 1, check_overlap = TRUE) +
    ggplot2::scale_x_log10(labels = scales::percent) +
    ggplot2::scale_y_log10(labels = scales::percent) +
    ggplot2::theme_light()

  list(
    sales_plot_us = sales_plot_us,
    sales_plot_world = sales_plot_world,
    taylor_swift_words = taylor_swift_words,
    ts_top_words_plot = ts_top_words_plot,
    ts_tf_idf = ts_tf_idf,
    ts_tf_idf_plot = ts_tf_idf_plot,
    ts_log_odds = ts_log_odds,
    ts_log_odds_plot = ts_log_odds_plot,
    word_differences = word_differences,
    word_differences_plot = word_differences_plot,
    comparison = comparison,
    comparison_scatter_plot = comparison_scatter_plot
  )
}
