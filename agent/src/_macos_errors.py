"""macOS ARM error helper — catches common Apple Silicon crashes and explains them.

Import this module early (before numpy/pandas) to get clear error messages
instead of cryptic "Bus error: 10" crashes.
"""
import os
import sys
import signal


def _bus_error_handler(signum, frame):
    """Handle SIGBUS with a helpful message instead of a cryptic crash."""
    msg = (
        "\n"
        "  ┌─────────────────────────────────────────────────────────────┐\n"
        "  │  🍎 BUS ERROR — Apple Accelerate BLAS thread conflict        │\n"
        "  │                                                             │\n"
        "  │  numpy/pandas crashed because two threads called Apple's     │\n"
        "  │  Accelerate BLAS framework simultaneously.                   │\n"
        "  │                                                             │\n"
        "  │  Fix: run vibe-trading via the setup script which sets       │\n"
        "  │       VECLIB_MAXIMUM_THREADS=1 before starting.              │\n"
        "  │                                                             │\n"
        "  │       source ~/activate-vibe-trading.sh                      │\n"
        "  │                                                             │\n"
        "  │  If this persists, the upstream model may have changed.      │\n"
        "  │  Report at: github.com/20YN04/vibe-trading-macos/issues      │\n"
        "  └─────────────────────────────────────────────────────────────┘\n"
    )
    sys.stderr.write(msg)
    sys.exit(138)


def _ensure_blas_env() -> None:
    """Set BLAS environment variables before numpy loads."""
    if sys.platform != "darwin":
        return
    blas_vars = {
        "VECLIB_MAXIMUM_THREADS": "1",
        "ACCELERATE_NEW_LAPACK": "0",
        "OPENBLAS_NUM_THREADS": "1",
        "OMP_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1",
        "BLIS_NUM_THREADS": "1",
    }
    for var, val in blas_vars.items():
        if var not in os.environ:
            os.environ[var] = val


# Install early — before any numpy import
_ensure_blas_env()
signal.signal(signal.SIGBUS, _bus_error_handler)
