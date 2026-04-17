# Shared helper functions for screencast analysis

find_tidyweek_path <- function(week_id, local_root = "tidytuesday/data") {
  file.path(local_root, substr(week_id, 1, 4), week_id)
}

read_tidyweek_file <- function(path) {
  extension <- tolower(tools::file_ext(path))

  if (extension == "csv") {
    if (requireNamespace("readr", quietly = TRUE)) {
      return(readr::read_csv(path, show_col_types = FALSE))
    }
    return(utils::read.csv(path, stringsAsFactors = FALSE))
  }

  if (extension %in% c("tsv", "txt")) {
    if (requireNamespace("readr", quietly = TRUE)) {
      return(readr::read_tsv(path, show_col_types = FALSE))
    }
    return(utils::read.delim(path, stringsAsFactors = FALSE))
  }

  if (extension == "rds") {
    return(readRDS(path))
  }

  if (extension %in% c("rda", "rdata")) {
    env <- new.env(parent = emptyenv())
    loaded <- load(path, envir = env)
    if (length(loaded) == 1) {
      return(env[[loaded]])
    }
    return(mget(loaded, envir = env))
  }

  if (extension == "json") {
    if (!requireNamespace("jsonlite", quietly = TRUE)) {
      stop("jsonlite is required to read local JSON TidyTuesday files. Install it with install.packages('jsonlite').")
    }
    return(jsonlite::fromJSON(path))
  }

  if (extension %in% c("xls", "xlsx")) {
    if (!requireNamespace("readxl", quietly = TRUE)) {
      stop("readxl is required to read local Excel TidyTuesday files. Install it with install.packages('readxl').")
    }
    return(readxl::read_excel(path))
  }

  stop("Unsupported local TidyTuesday file type: ", basename(path))
}

load_local_tidyweek_data <- function(week_id, local_root = "tidytuesday/data") {
  week_path <- find_tidyweek_path(week_id, local_root = local_root)

  if (!dir.exists(week_path)) {
    return(NULL)
  }

  candidates <- list.files(
    week_path,
    pattern = "\\.(csv|tsv|txt|rds|rda|rdata|json|xls|xlsx)$",
    full.names = TRUE
  )

  if (length(candidates) == 0) {
    return(NULL)
  }

  data <- lapply(candidates, read_tidyweek_file)
  names(data) <- tools::file_path_sans_ext(basename(candidates))
  data
}

load_tidyweek_data <- function(week_id, local_root = "tidytuesday/data", prefer_local = TRUE) {
  if (prefer_local) {
    local_data <- load_local_tidyweek_data(week_id, local_root = local_root)
    if (!is.null(local_data) && length(local_data) > 0) {
      return(local_data)
    }
  }

  if (!requireNamespace("tidytuesdayR", quietly = TRUE)) {
    stop(
      "tidytuesdayR is required when local mirrored data is unavailable. ",
      "Install it with install.packages('tidytuesdayR')."
    )
  }

  data <- tryCatch(
    tidytuesdayR::tt_load(week_id),
    error = function(err) {
      stop(
        "Could not load TidyTuesday data for week ", week_id, ". ",
        "Local files were not found under '", local_root, "' and the GitHub fallback failed. ",
        "If you are hitting GitHub rate limits, set a Personal Access Token in the GITHUB_PAT environment variable before retrying. ",
        "Original error: ", conditionMessage(err)
      )
    }
  )

  if (!is.list(data) || length(data) == 0) {
    stop("Could not load TidyTuesday data for week: ", week_id)
  }
  data
}

prepare_text_tokens <- function(tbl, text_col = "text", stop_words = tidytext::stop_words) {
  if (!requireNamespace("tidytext", quietly = TRUE)) {
    stop("tidytext is required for tokenization. Install it with install.packages('tidytext').")
  }
  if (!text_col %in% names(tbl)) {
    stop("Text column not found: ", text_col)
  }
  tidytext::unnest_tokens(tbl, word, !!rlang::sym(text_col))
}

plot_top_bars <- function(tbl, label_col, value_col, fill_col = NULL, top_n = 20, title = NULL, x_label = NULL, y_label = NULL) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("ggplot2 is required to create plots. Install it with install.packages('ggplot2').")
  }
  required_cols <- c(label_col, value_col)
  if (!all(required_cols %in% names(tbl))) {
    stop("tbl must contain columns: ", paste(required_cols, collapse = ", "))
  }
  plot_data <- tbl %>%
    dplyr::arrange(dplyr::desc(!!rlang::sym(value_col))) %>%
    dplyr::slice_head(n = top_n)

  if (!is.null(fill_col) && fill_col %in% names(plot_data)) {
    p <- ggplot2::ggplot(plot_data, ggplot2::aes_string(x = label_col, y = value_col, fill = fill_col))
  } else {
    p <- ggplot2::ggplot(plot_data, ggplot2::aes_string(x = label_col, y = value_col))
  }

  p +
    ggplot2::geom_col() +
    ggplot2::coord_flip() +
    ggplot2::labs(
      title = if (!is.null(title)) title else NULL,
      x = if (!is.null(x_label)) x_label else label_col,
      y = if (!is.null(y_label)) y_label else value_col,
      fill = if (!is.null(fill_col) && fill_col %in% names(plot_data)) fill_col else NULL
    ) +
    ggplot2::theme_minimal()
}

summarize_expeditions <- function(tbl) {
  tbl %>%
    dplyr::summarize(
      n_climbs = dplyr::n(),
      pct_success = mean(success == "Success", na.rm = TRUE),
      dplyr::across(members:hired_staff_deaths, ~ sum(.x, na.rm = TRUE)),
      first_climb = min(year, na.rm = TRUE)
    ) %>%
    dplyr::mutate(
      pct_death = member_deaths / members,
      pct_hired_staff_deaths = hired_staff_deaths / hired_staff
    )
}

plot_days_to_highpoint <- function(tbl, top_n = 10, title = NULL, subtitle = NULL) {
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    stop("ggplot2 is required to create plots. Install it with install.packages('ggplot2').")
  }
  required_cols <- c("days_to_highpoint", "peak_name", "success")
  if (!all(required_cols %in% names(tbl))) {
    stop("tbl must contain columns: days_to_highpoint, peak_name, success")
  }
  plot_data <- tbl %>%
    dplyr::filter(!is.na(days_to_highpoint), !is.na(peak_name), success == "Success") %>%
    dplyr::mutate(peak_name = forcats::fct_lump(peak_name, 10),
                  peak_name = forcats::fct_reorder(peak_name, days_to_highpoint))

  ggplot2::ggplot(plot_data, ggplot2::aes(days_to_highpoint, peak_name)) +
    ggplot2::geom_boxplot() +
    ggplot2::labs(
      x = "Days from basecamp to highpoint",
      y = "",
      title = if (!is.null(title)) title else "How long does it take to get to the high point?",
      subtitle = if (!is.null(subtitle)) subtitle else "Successful climbs only"
    ) +
    ggplot2::theme_minimal()
}

load_remote_csv <- function(url) {
  if (!requireNamespace("readr", quietly = TRUE)) {
    stop("readr is required to load remote CSVs. Install it with install.packages('readr').")
  }
  readr::read_csv(url)
}

prepare_lyrics_tokens <- function(tbl, text_col = "lyrics", group_cols = NULL) {
  if (!requireNamespace("tidytext", quietly = TRUE)) {
    stop("tidytext is required for lyrics tokenization. Install it with install.packages('tidytext').")
  }
  if (!requireNamespace("rlang", quietly = TRUE)) {
    stop("rlang is required for tidy evaluation. Install it with install.packages('rlang').")
  }

  if (!text_col %in% names(tbl)) {
    stop("Text column not found: ", text_col)
  }

  tbl <- tbl %>%
    dplyr::rename_with(stringr::str_to_lower)

  tokenized <- tbl %>%
    tidytext::unnest_tokens(word, !!rlang::sym(text_col)) %>%
    dplyr::anti_join(tidytext::stop_words, by = "word")

  if (!is.null(group_cols)) {
    grouping <- intersect(group_cols, names(tokenized))
    if (length(grouping) > 0) {
      tokenized <- tokenized %>% dplyr::group_by(dplyr::across(dplyr::all_of(grouping))) %>% dplyr::ungroup()
    }
  }
  tokenized
}

compute_tf_idf <- function(tbl, document_col, term_col, count_col = "n") {
  if (!requireNamespace("tidytext", quietly = TRUE)) {
    stop("tidytext is required for tf-idf computations. Install it with install.packages('tidytext').")
  }
  if (!requireNamespace("rlang", quietly = TRUE)) {
    stop("rlang is required for tidy evaluation. Install it with install.packages('rlang').")
  }
  if (!all(c(document_col, term_col, count_col) %in% names(tbl))) {
    stop("tbl must contain document, term, and count columns for tf-idf.")
  }

  tbl %>%
    dplyr::rename(
      document = !!rlang::sym(document_col),
      term = !!rlang::sym(term_col),
      count = !!rlang::sym(count_col)
    ) %>%
    tidytext::bind_tf_idf(term, document, count)
}

compute_log_odds <- function(tbl, group_col, term_col, count_col = "n") {
  if (!requireNamespace("tidylo", quietly = TRUE)) {
    stop("tidylo is required for log odds computations. Install it with install.packages('tidylo').")
  }
  if (!requireNamespace("rlang", quietly = TRUE)) {
    stop("rlang is required for tidy evaluation. Install it with install.packages('rlang').")
  }
  if (!all(c(group_col, term_col, count_col) %in% names(tbl))) {
    stop("tbl must contain group, term, and count columns for log odds.")
  }

  tbl %>%
    dplyr::rename(
      group = !!rlang::sym(group_col),
      term = !!rlang::sym(term_col),
      count = !!rlang::sym(count_col)
    ) %>%
    tidylo::bind_log_odds(group, term, count)
}
