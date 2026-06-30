#!/bin/bash
# Generate showcase report from latest run
# Usage: ./scripts/showcase-latest.sh [--open]

LATEST=$(ls -dt agent/runs/*/ 2>/dev/null | head -1)
if [ -z "$LATEST" ]; then
    echo "No runs found in agent/runs/"
    exit 1
fi

echo "Latest run: $LATEST"
python scripts/showcase.py "$LATEST" --output showcase.html
echo "Report: showcase.html"

if [ "$1" = "--open" ]; then
    open showcase.html
fi
