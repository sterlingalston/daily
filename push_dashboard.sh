#!/bin/bash
# Generate dashboard data and push to GitHub Pages.
# Run daily by cron at 16:00.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$REPO/push_dashboard.log"
PYTHON="/home/malston/miniconda3/bin/python3"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting dashboard push" >> "$LOG"

cd "$REPO"

# Generate fresh data
"$PYTHON" generate_dashboard_data.py >> "$LOG" 2>&1

# Commit and push if there are changes
if git diff --quiet dashboard_data.json 2>/dev/null; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] No changes to dashboard_data.json, skipping push" >> "$LOG"
else
    git add dashboard_data.json
    git commit -m "chore: update dashboard data $(date '+%Y-%m-%d %H:%M')" >> "$LOG" 2>&1
    git push origin main >> "$LOG" 2>&1
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Pushed dashboard_data.json" >> "$LOG"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Done" >> "$LOG"
