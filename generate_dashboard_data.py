#!/usr/bin/env python3
"""
Generate dashboard_data.json from cron job logs.
Run daily and push to git so GitHub Pages dashboard stays current.
"""

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

HOME = Path.home()
OUT_JSON = Path(__file__).parent / "dashboard_data.json"
OUT_JS   = Path(__file__).parent / "dashboard_data.js"

BACKUP_FOLDERS = [
    "tryhackme", "monochrome", "mcloud_download", "mcloud_playlists",
    "shazams", "language-study", "dabmusic", "daily",
    "snowflake_data_engineering(coursera)",
]

KCRW_SCRIPTS = [
    "import_kcrw.py", "kcrw_dedup.py", "kcrw_monochrome_import.py",
    "local_kcrw_import.py", "soundcloud_search.py",
    "download_soundcloud_errors.py", "shazam_monochrome_import.py",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _no_log(name, schedule, hour):
    return {
        "name": name,
        "schedule": schedule,
        "hour": hour,
        "last_run": None,
        "status": "no_log",
        "progress": 0,
        "steps": [],
        "counts": {},
        "log_tail": [],
    }


def _read(path):
    try:
        return Path(path).read_text(errors="replace").splitlines()
    except Exception:
        return []


def _last_ts(lines, pattern=r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"):
    for line in reversed(lines):
        m = re.search(pattern, line)
        if m:
            return m.group(1)
    return None


def _find_last_block(lines, marker):
    """Return lines from the last occurrence of a line containing `marker`."""
    idx = -1
    for i, line in enumerate(lines):
        if marker in line:
            idx = i
    return lines[idx:] if idx >= 0 else []


# ---------------------------------------------------------------------------
# Per-job parsers
# ---------------------------------------------------------------------------

def parse_backup():
    lines = _read(HOME / "backup_to_q.log")
    if not lines:
        return _no_log("Backup to Q (rsync)", "Daily 12:00", 12)

    run = _find_last_block(lines, "Starting backup to")
    if not run:
        return _no_log("Backup to Q (rsync)", "Daily 12:00", 12)

    run_text = "\n".join(run)
    start_time = None
    m = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", run[0])
    if m:
        start_time = m.group(1)

    synced, skipped = set(), set()
    for line in run:
        m = re.match(r"\[.*?\] Synced: (.+)", line)
        if m:
            synced.add(m.group(1).strip())
        m = re.match(r"\[.*?\] SKIP \(not found\): (.+)", line)
        if m:
            skipped.add(m.group(1).strip())

    complete = "Backup complete." in run_text

    steps = []
    for folder in BACKUP_FOLDERS:
        if folder in synced:
            # Check for rsync error in the context before "Synced: folder"
            idx = run_text.find(f"Synced: {folder}")
            context = run_text[max(0, idx - 3000):idx]
            has_err = "rsync error:" in context
            steps.append({"name": folder, "status": "warning" if has_err else "ok"})
        elif folder in skipped:
            steps.append({"name": folder, "status": "skip"})
        else:
            steps.append({"name": folder, "status": "pending"})

    has_any_err = "rsync error:" in run_text
    done = len(synced) + len(skipped)
    progress = min(100, int(done / len(BACKUP_FOLDERS) * 100))
    overall = "ok" if complete and not has_any_err else ("warning" if complete or has_any_err else "running")

    return {
        "name": "Backup to Q (rsync)",
        "schedule": "Daily 12:00",
        "hour": 12,
        "last_run": start_time,
        "status": overall,
        "progress": progress,
        "steps": steps,
        "counts": {
            "Folders synced": len(synced),
            "Folders skipped": len(skipped),
            "Rsync errors": run_text.count("rsync error:"),
        },
        "log_tail": run[-10:],
    }


def parse_kcrw_daily():
    lines = _read(HOME / "mcloud_playlists/run_kcrw_daily.log")
    if not lines:
        return _no_log("Run KCRW Daily", "Daily 14:00", 14)

    # Find last run (lines with "=== ... — starting ===")
    run = _find_last_block(lines, "— starting")
    if not run:
        run = _find_last_block(lines, "starting")
    if not run:
        return _no_log("Run KCRW Daily", "Daily 14:00", 14)

    start_time = None
    m = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", run[0])
    if m:
        start_time = m.group(1)

    # Parse "--- script.py ---" + "✓ done" / "✗ failed"
    steps = []
    current = None
    for line in run:
        m = re.match(r"^--- (.+?) ---$", line)
        if m:
            current = m.group(1)
        elif current:
            if "✓ done" in line or "done" in line.lower():
                steps.append({"name": current, "status": "ok"})
                current = None
            elif "✗ failed" in line or "failed" in line.lower():
                steps.append({"name": current, "status": "error"})
                current = None

    run_text = "\n".join(run)
    finished = "— finished" in run_text

    ok = sum(1 for s in steps if s["status"] == "ok")
    err = sum(1 for s in steps if s["status"] == "error")
    done = ok + err
    progress = min(100, int(done / len(KCRW_SCRIPTS) * 100))
    overall = "ok" if finished and err == 0 else ("warning" if finished and err > 0 else ("error" if err > 0 else "running"))

    return {
        "name": "Run KCRW Daily",
        "schedule": "Daily 14:00",
        "hour": 14,
        "last_run": start_time,
        "status": overall,
        "progress": progress,
        "steps": steps,
        "counts": {
            "Scripts OK": ok,
            "Scripts failed": err,
        },
        "log_tail": run[-10:],
    }


def parse_spotify():
    lines = _read(HOME / "mcloud_playlists/import_spotify.log")
    if not lines:
        return _no_log("Import Spotify", "Daily 13:00", 13)

    last_run = _last_ts(lines)

    # Count unique tracks: lines matching "INFO   + Artist - Track [id]"
    seen_ids = set()
    for line in lines:
        m = re.search(r"INFO\s+\+\s+.+\[(\d+)\]", line)
        if m:
            seen_ids.add(m.group(1))

    has_error = any("ERROR" in l or "Traceback" in l for l in lines[-100:])
    status = "error" if has_error else "ok"

    return {
        "name": "Import Spotify",
        "schedule": "Daily 13:00",
        "hour": 13,
        "last_run": last_run,
        "status": status,
        "progress": 100 if status == "ok" else 50,
        "steps": [],
        "counts": {
            "Tracks imported (total)": len(seen_ids),
        },
        "log_tail": lines[-10:],
    }


def parse_kcrw_sync():
    lines = _read(HOME / "dabmusic/sync_kcrw.log")
    if not lines:
        return _no_log("Sync KCRW", "Daily 14:00", 14)

    last_run = _last_ts(lines)

    seen_ids = set()
    for line in lines:
        m = re.search(r"INFO\s+\+\s+.+\[(\d+)\]", line)
        if m:
            seen_ids.add(m.group(1))

    has_error = any("ERROR" in l or "Traceback" in l for l in lines[-100:])
    status = "error" if has_error else "ok"

    return {
        "name": "Sync KCRW",
        "schedule": "Daily 14:00",
        "hour": 14,
        "last_run": last_run,
        "status": status,
        "progress": 100 if status == "ok" else 50,
        "steps": [],
        "counts": {
            "Tracks synced (total)": len(seen_ids),
        },
        "log_tail": lines[-10:],
    }


def parse_vocab():
    lines = _read(HOME / "tryhackme/scripts/update_vocab.log")
    if not lines:
        return _no_log("Update TryHackMe Vocab", "Daily 15:00", 15)

    run = _find_last_block(lines, "===")
    if not run:
        return _no_log("Update TryHackMe Vocab", "Daily 15:00", 15)

    start_time = None
    m = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}|\w+ \w+ +\d+ \d{2}:\d{2}:\d{2} \w+ \d{4})", run[0])
    if m:
        raw = m.group(1)
        # Try parsing as ISO first, else as ctime
        try:
            start_time = datetime.strptime(raw, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                start_time = datetime.strptime(raw, "%a %b %d %H:%M:%S %Z %Y").strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                start_time = raw

    run_text = "\n".join(run)
    done = "Done." in run_text
    has_error = any(w in run_text for w in ["ERROR", "fatal:", "error:", "Traceback"])
    status = "ok" if done and not has_error else ("warning" if has_error else "running")

    # Count vocab files updated via git commit lines
    commits = run_text.count("Auto-update vocabulary")
    changed = run_text.count("changed,")  # from git diff --stat

    return {
        "name": "Update TryHackMe Vocab",
        "schedule": "Daily 15:00",
        "hour": 15,
        "last_run": start_time,
        "status": status,
        "progress": 100 if done else 50,
        "steps": [],
        "counts": {
            "Auto-commits": commits,
            "Vocab files changed": changed,
        },
        "log_tail": run[-10:],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    jobs = [
        parse_backup(),
        parse_spotify(),
        parse_kcrw_sync(),
        parse_kcrw_daily(),
        parse_vocab(),
    ]

    # Compute next_run for each job
    now = datetime.now()
    for job in jobs:
        h = job.get("hour", 0)
        candidate = now.replace(hour=h, minute=0, second=0, microsecond=0)
        if candidate <= now:
            from datetime import timedelta
            candidate += timedelta(days=1)
        job["next_run"] = candidate.strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "jobs": jobs,
    }

    OUT_JSON.write_text(json.dumps(data, indent=2))
    OUT_JS.write_text("window.DASHBOARD_DATA = " + json.dumps(data, indent=2) + ";\n")
    print(f"Wrote {OUT_JSON} and {OUT_JS}")


if __name__ == "__main__":
    main()
