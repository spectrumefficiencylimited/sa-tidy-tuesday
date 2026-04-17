#!/usr/bin/env bash
# render_all.sh — TheDataShrink™ Marathon Render Script
#
# Renders all episode QMDs for the marathon.
# Run from the sa-tidy-tuesday root directory.
#
# Usage:
#   ./render_all.sh              # render all 3-hour QMDs for all episodes
#   ./render_all.sh --hour h1    # only hour 1 EDA for all episodes
#   ./render_all.sh --ep 001     # only episode 001 (all hours)
#   ./render_all.sh --guide      # only episode_guide.qmd for all (original reproduction)
#
# Prerequisites:
#   brew install quarto
#   R packages: tidyverse, tidytext, broom, glmnet, survival, ggraph, etc.

set -euo pipefail

HOUR=""
EP_FILTER=""
GUIDE_ONLY=false
EPISODES_ROOT="output/episodes"

# Parse args
while [[ $# -gt 0 ]]; do
    case $1 in
        --hour) HOUR="$2"; shift 2 ;;
        --ep)   EP_FILTER="$2"; shift 2 ;;
        --guide) GUIDE_ONLY=true; shift ;;
        *) echo "Unknown arg: $1"; exit 1 ;;
    esac
done

rendered=0
skipped=0
failed=0

for ep_dir in "$EPISODES_ROOT"/*/; do
    ep_name=$(basename "$ep_dir")

    # Filter by episode prefix if specified
    if [[ -n "$EP_FILTER" ]] && [[ "$ep_name" != ${EP_FILTER}* ]]; then
        continue
    fi

    fn=$(echo "$ep_name" | sed 's/^[0-9]*_//')

    echo ""
    echo "━━━ $ep_name ━━━"

    render_qmd() {
        local qmd="$1"
        if [[ -f "$qmd" ]]; then
            echo "  Rendering: $(basename $qmd)"
            if quarto render "$qmd" --quiet 2>/dev/null; then
                ((rendered++)) || true
                echo "  ✓ $(basename ${qmd%.qmd}).html"
            else
                ((failed++)) || true
                echo "  ✗ FAILED: $qmd"
            fi
        fi
    }

    if $GUIDE_ONLY; then
        render_qmd "$ep_dir/episode_guide.qmd"
    elif [[ -n "$HOUR" ]]; then
        render_qmd "$ep_dir/${HOUR}_*_${fn}.qmd"
    else
        # Render all 3 hours
        render_qmd "$ep_dir/h1_eda_${fn}.qmd"
        render_qmd "$ep_dir/h2_modeling_${fn}.qmd"
        render_qmd "$ep_dir/h3_communicate_${fn}.qmd"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✓ Rendered:  $rendered"
echo "✗ Failed:    $failed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
