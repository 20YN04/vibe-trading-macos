"""Vibe-Trading core package.

macOS ARM compatibility layer — loaded before any numpy/pandas import.
"""
import os
import sys

# ── macOS ARM: Apple Accelerate BLAS threading workaround ──────────────
# On Apple Silicon, numpy uses Apple's Accelerate framework for BLAS.
# Accelerate's internal threading crashes (bus error) when called from
# multiple Python threads simultaneously because C extensions release
# the GIL during BLAS calls.
#
# Fix: force all BLAS libraries to single-threaded mode BEFORE numpy loads.
# This prevents concurrent Accelerate calls across threads.

if sys.platform == "darwin":
    _blas_vars = {
        "VECLIB_MAXIMUM_THREADS": "1",   # Apple Accelerate
        "ACCELERATE_NEW_LAPACK": "0",     # Use legacy LAPACK (more stable)
        "OPENBLAS_NUM_THREADS": "1",      # OpenBLAS (if installed)
        "MKL_NUM_THREADS": "1",           # Intel MKL
        "OMP_NUM_THREADS": "1",           # OpenMP
        "NUMEXPR_NUM_THREADS": "1",       # NumExpr
        "BLIS_NUM_THREADS": "1",          # BLIS
    }
    for _var, _val in _blas_vars.items():
        if _var not in os.environ:
            os.environ[_var] = _val
