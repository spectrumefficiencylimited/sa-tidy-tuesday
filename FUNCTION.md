# Function Repository Overview

This file is the entry point for both the TidyTuesday function extraction effort
and the ndexr.io production function inventory.

## Two Function Tracks

### Track 1 — TidyTuesday (Analytical)
- `control_table.csv` — mapping of transcript titles, code files, function names, extraction status
- `knowledge register.md` — long-form KER for intent, thought patterns, data transformations
- `R/screencast_intent_stubs.R` — generated function stubs per episode
- `R/screencast_helpers.R` — shared helper functions (local-first TidyTuesday loading)
- `R/screencast_implementations.R` — actual implementations for selected episodes

### Track 2 — ndexr.io Production (Shiny)
Functions from the live console codebase at `/home/ubuntu/console/src/r/`.

## ndexr Production Function Inventory

### inputs/inputs.r (~1900 lines) — The Utility Core

**Null/Default:**
- `setDefault(value, default)` — null-coalesce for any type
- `if_is_null(x)` → NA_character_ if null
- `contains_guid(x)` — UUID regex check

**Notifications & Modals:**
- `pan(message, type, duration)` — toast notification (singleton per session)
- `modal_transition(message, easyClose, content)` — loading spinner modal
- `modal_message(title, message, body, type, size, ...)` — alert/info/error modal
- `handle_err(id, err, require, stdout)` — error display + state storage

**Form Controls:**
- `actionButton(id, label, icon, class, size, disabled)` — Bootstrap button with action-button class
- `passwordInput(id, label, placeholder, value, size, disabled)` — password field
- `lbl(ns, id, text, class)` — form label
- `txt(ns, id, value, placeholder, width, title)` — text input (sm)
- `num(ns, id, value, min, max, step, width, title)` — number input (sm)
- `sel(ns, id, children, title)` — select dropdown (sm)
- `check_inline(ns, id, label, title)` — inline checkbox
- `field(label, input, class, id, div_id)` — label + input wrapper
- `options_from(x)` — vector/list → option tags

**Layout:**
- `row_inline(..., gap, class)` — flex row with gap
- `control_minwidth(x, px)` — min-width wrapper
- `create_tabset_panel(..., sidebar, panel_name, justify)` — tabbed UI (horizontal or sidebar)
- `create_tab(tab_title, tab_content, icon, active_title)` — tab item
- `card(title, ..., collapse)` — collapsible card with fullscreen
- `section_card(title, ..., class)` — bordered section with divider
- `offcanvas(ns, label, title, ..., placement)` — sliding panel
- `accordion(id, ..., flush, always_open)` — accordion container
- `accordion_item(acc_id, header_id, collapse_id, title, body, open)` — accordion item
- `alert(..., type, icon, class, dismissible)` — Bootstrap alert
- `help_button(id, title, content, placement)` — popover help

**Spinner:**
- `ui_spinner(id, message, pattern)` — loading spinner with random image

**Theming:**
- `custom_plot_theme(...)` — ggplot2 theme (light)
- `theme_custom(base_size, base_family, dark)` — ggplot2 theme (dark/light toggle)

**Contact Form:**
- `ui_send_message(id, title, ...)` — full contact form UI
- `server_send_message(id, phone_number, ...)` — validation + SNS delivery

**Data:**
- `create_dynamic_card(ns, titles, values, buttons)` — data display card
- `format_time_diff(time_diff)` — "X ago" formatter

### connections/ — Data Layer

**postgres.r:**
- `connection_postgres(host, port, user, password, dbname)` — DBI connection (auto-creates DB)
- `table_create_or_upsert(data, where_cols, ...)` — insert-or-update with UNIQUE constraint
- `table_append(data, ...)` — simple append
- `table_get(dataname, ...)` → dplyr::tbl() lazy evaluation
- `table_exists(dataname, ...)` / `tables_list(...)` / `table_drop(dataname, ...)`
- `tables_row_retrieve(where_cols, id, table, ...)` / `tables_row_remove(...)`
- `instance_state(...)` — EC2 state to DB
- `refresh_materialized_view()` — admin dashboard refresh

**state.r:**
- `store_state(id, data)` — postgres + storr_dbi storage
- `get_state(id)` — retrieve with error fallback
- `key_exists(id)` — logical check

**storr.r:**
- `connection_storr()` — SQLite-backed storr_dbi

### aws/ — AWS Integration

**client.r:**
- `client(service, ns_common_store_user, region)` — boto3 client via reticulate
- `resource(service, ns_common_store_user)` — boto3 resource

**secrets/secrets.r:**
- `secret_set(key, value)` / `secret_get(key)` / `secret_delete(key)` / `secret_exists(fn)`

**ec2/:**
- `instance_manage.r` — create_instance, describe_instances, allocate/associate elastic IP
- `key_pairs.r` — list_key_pair, manage_key_pair
- `security_groups.r` — list_security_groups, manage_security_groups, security_group_envoke
- `ec2_backend.r` — ec2_list_elastic_ip, route53_list_hosted_zones
- `amis.r` — describe_images, ami_catalog
- `rbox_init.r` — full launch workflow (readiness → server → networking → scripts → launch)

**login_processing.r:**
- `login_processing(session)` — post-auth: log to DB, set up namespace, fetch AWS resources, check Stripe
- `fetch_resource(fetch_function, ...)` — tryCatch wrapper with notification

### stripe/ — Payments

- `connection(live)` — Stripe client (test vs live keys)
- `retrieve_or_create_customer(email, con)` — customer lookup/create
- `subscription_start/cancel/retrieve(data, ...)` — subscription CRUD
- `is_subscribed(session)` — check + mutate session
- `payment_methods_retrieve(data, customer_id)` — list cards
- `create_payment_method(data, card_info)` / `payment_method_detach(data, id)`

## Control Table Workflow (TidyTuesday Track)

Status flow: `needs_mapping` → `mapped` → `extracted` → `implemented` → `reviewed`

Fields: transcript_title, transcript_file, code_file, function_name, data_source,
analysis_intent, analysis_type, pattern_signature, adaptation_hint, ker_status, notes

## Goals

- Capture reusable patterns from BOTH tracks (analytical + production)
- Turn episode-level analysis intent into reusable R functions
- Document production patterns that apply to any R/Shiny deployment
- Preserve reasoning patterns, not just syntax
