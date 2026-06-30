#!/usr/bin/env bash
# vibe-trading-macos setup — one command to get everything running
# Usage: ./scripts/setup.sh
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
say()  { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
err()  { echo -e "${RED}✗${NC} $1"; exit 1; }
info() { echo -e "${CYAN}→${NC} $1"; }

echo ""
echo "  🍎 vibe-trading-macos setup"
echo "  ───────────────────────────"
echo ""

# ── Python check ──────────────────────────────────────────────────
info "Checking Python..."
PYTHON=""
for py in python3.12 python3.11 python3.13; do
    if command -v $py &>/dev/null; then
        PYTHON=$py
        break
    fi
done
[ -n "$PYTHON" ] || err "Python 3.11+ required. Install: brew install python@3.12"
say "Using $PYTHON ($($PYTHON --version))"

# ── macOS ARM check ────────────────────────────────────────────
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    say "Apple Silicon detected — applying BLAS fixes"
else
    warn "Intel Mac detected — BLAS fixes not needed but won't hurt"
fi

# ── Venv ──────────────────────────────────────────────────────────
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    info "Creating virtual environment..."
    $PYTHON -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
say "Virtual environment active"

# ── Dependencies ──────────────────────────────────────────────────
info "Installing dependencies..."
pip install -e ".[dev]" --quiet 2>&1 | tail -1
say "Dependencies installed"

# ── Config ────────────────────────────────────────────────────────
CONFIG="$HOME/.vibe-trading/.env"
if [ ! -f "$CONFIG" ]; then
    info "Running interactive config setup..."
    vibe-trading init
else
    say "Config found: $CONFIG"
fi

# ── Verify ────────────────────────────────────────────────────────
info "Running preflight check..."
vibe-trading run -p "Say ready" --max-iter 1 --no-rich 2>/dev/null && \
    say "Preflight OK — agent is working" || \
    warn "Preflight returned non-zero (may need API key)"

# ── Activation convenience ────────────────────────────────────────
ACTIVATE_SCRIPT="$HOME/activate-vibe-trading.sh"
cat > "$ACTIVATE_SCRIPT" << ACTIVATE
#!/bin/bash
cd "$(pwd)"
source "$VENV_DIR/bin/activate"
export VECLIB_MAXIMUM_THREADS=1
export ACCELERATE_NEW_LAPACK=0
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
echo "Vibe-Trading \$(vibe-trading --version 2>/dev/null) — macOS ARM native"
echo "Commands: vibe-trading chat | vibe-trading serve | vibe-trading alpha bench ..."
ACTIVATE
chmod +x "$ACTIVATE_SCRIPT"
say "Activation script: $ACTIVATE_SCRIPT"

echo ""
say "Setup complete. Start with: source ~/activate-vibe-trading.sh"
