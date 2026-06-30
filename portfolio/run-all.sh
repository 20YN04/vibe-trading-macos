#!/usr/bin/env bash
# Portfolio builder — run all 8 MacroGlide projects and collect results
# Usage: ./portfolio/run-all.sh
set -euo pipefail

GREEN='\033[0;32m'; CYAN='\033[0;36m'; NC='\033[0m'
RESULTS_DIR="portfolio/results/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESULTS_DIR"

PROJECTS=(
    "ml-alpha-model"
    "options-pricing"
    "stat-arb"
    "factor-model"
    "risk-engine"
    "crypto-arb"
    "hft-simulator"
    "portfolio-optimizer"
)

echo ""
echo "  📊 Portfolio Builder — 8 Quant Projects"
echo "  Results: $RESULTS_DIR"
echo ""

for project in "${PROJECTS[@]}"; do
    echo -e "${CYAN}→${NC} Running: $project"
    vibe-trading run \
        -p "$(cat "portfolio/${project}.txt")" \
        --max-iter 20 \
        --json \
        > "$RESULTS_DIR/${project}.json" 2>&1

    status=$?
    if [ $status -eq 0 ]; then
        echo -e "  ${GREEN}✓${NC} $project complete"
    else
        echo "  ✗ $project failed (exit $status)"
    fi
    echo ""
done

echo -e "${GREEN}✓${NC} All projects done. Results in: $RESULTS_DIR"
ls -la "$RESULTS_DIR/"
