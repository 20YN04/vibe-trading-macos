#!/bin/bash
# Pre-commit hook: block .env file commits
if git diff --cached --name-only | grep -q "\.env$"; then
    echo "BLOCKED: .env files must not be committed (contains secrets)"
    echo "Add .env to .gitignore or use .env.example instead"
    exit 1
fi
exit 0
