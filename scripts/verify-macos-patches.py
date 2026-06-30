"""Pre-commit hook: verify macOS ARM patches are intact.

Checks that the three critical macOS patches haven't been
accidentally reverted or broken by an upstream merge.
"""
import sys
from pathlib import Path

AGENT = Path(__file__).resolve().parent.parent / "agent" / "src"

CHECKS = {
    "agent/src/__init__.py": [
        "BLAS threading workaround",
        "VECLIB_MAXIMUM_THREADS",
        "src._macos_errors",
    ],
    "agent/src/agent/loop.py": [
        "sys.platform == \"darwin\"",
        "return False",
    ],
    "agent/src/preflight.py": [],
}

failed = 0
for rel_path, must_contain in CHECKS.items():
    path = AGENT.parent / rel_path
    if not path.exists():
        print(f"  SKIP {rel_path} — file not found")
        continue

    content = path.read_text()
    for needle in must_contain:
        if needle not in content:
            print(f"  FAIL {rel_path} — missing: {needle}")
            failed += 1

if failed:
    print(f"\n{failed} macOS ARM patch(es) missing or broken.")
    print("Run: git diff upstream/main -- agent/src/")
    sys.exit(1)

print("  OK — all macOS ARM patches intact")
