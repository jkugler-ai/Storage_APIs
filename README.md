# Storage_APIs

Workspace for **Storage team** notes (meeting minutes, Confluence mirrors) plus a **local-only** browser history export script.

## Daily website visit logging

Export browser history visits (Chrome, Edge, Firefox) to a daily CSV or JSONL file using a local Python script. No network calls; data stays on your PC unless you choose a sync folder.

## Policy, privacy, and employer rules

Before you schedule this on a work machine:

- **IT and security policy**: Automated logging of browsing may be restricted or subject to review. Confirm with your employer that **local-only** history export scripts are allowed.
- **Sensitive URLs**: History can include internal tools, query strings, and tokens. Keep output in a **protected folder**, avoid sharing logs, and use `--redact-domain` for hosts you never want written to disk.
- **OneDrive / cloud sync**: The default log folder is `logs/` under this project. If the project lives in OneDrive, those files **sync to the cloud**. Use `--output-dir` to point at a purely local path if that is safer for your situation.

**Incognito / InPrivate**: Chromium and Firefox normally **do not** write those visits to the standard history database, so they will **not** appear in this export.

## Requirements

- **Python 3.10+** (uses `Path | None` style unions; adjust if you need 3.9).
- Standard library only (`sqlite3`, `csv`, `json`, etc.).

## Usage

From this folder:

```powershell
python scripts/export_browser_history.py
```

Defaults:

- Browsers: `chrome`, `edge`, and `firefox` (omit any you do not use with `--browsers chrome,edge`).
- Chromium profiles: `Default` only. Add more with `--chromium-profiles "Default,Profile 1"`.
- Output: `logs/visits-YYYY-MM-DD.csv` (created next to this README).
- State: `state/watermarks.json` (incremental cursor per browser/profile; gitignored).

Examples:

```powershell
# JSON Lines instead of CSV
python scripts/export_browser_history.py --format jsonl

# Only Edge, custom output folder
python scripts/export_browser_history.py --browsers edge --output-dir "C:\Logs\BrowserHistory"

# Redact a host from written URLs
python scripts/export_browser_history.py --redact-domain example.com

# First run: how far back to scan when no watermark exists yet (default 7)
python scripts/export_browser_history.py --lookback-days 14

# Firefox: limit to one profile by name or path
python scripts/export_browser_history.py --browsers firefox --firefox-profile "ProfileName"
```

### Chromium `History` file locations (Windows)

Verify on your PC; typical paths:

| Browser | Path |
|--------|------|
| Chrome | `%LOCALAPPDATA%\Google\Chrome\User Data\<Profile>\History` |
| Edge   | `%LOCALAPPDATA%\Microsoft\Edge\User Data\<Profile>\History` |

`<Profile>` is usually `Default`, or `Profile 1`, `Profile 2`, … for extra profiles.

### Firefox

If `profiles.ini` exists under `%APPDATA%\Mozilla\Firefox\`, all profiles with `places.sqlite` are exported unless you pass `--firefox-profile`.

## Task Scheduler (daily)

1. Open **Task Scheduler** → **Create Task…** (not a simple “Create Basic Task” if you want full control).
2. **General**: Name e.g. `BrowserHistoryExport`; choose “Run only when user is logged on” unless you need otherwise; your history files are per-user.
3. **Triggers** → New → **Daily** at a time after you usually stop browsing, or at lunch — whenever you want the rollup.
4. **Actions** → New → **Start a program**:
   - **Program/script**: full path to your `python.exe` (or `py.exe`).
   - **Add arguments** (example):

     ```text
     "C:\Users\YOUR_USER\OneDrive - NVIDIA Corporation\Cursor Projects\Daily Things\scripts\export_browser_history.py"
     ```

   - **Start in**: the project root folder (the folder that contains `scripts\` and `logs\`).

5. **Conditions / Settings**: Uncheck “Start only if on AC power” if you use a laptop on battery and still want the task to run.

If the browser holds a lock on the database, the script **copies** the file first; if copy still fails, close the browser or run the task when the browser is idle. Warnings are printed to stderr.

## Repository layout

- `scripts/export_browser_history.py` — export logic.
- `state/` — holds `watermarks.json` at runtime (ignored by git).
- `logs/` — optional destination for daily files; ignored by git if you use the default under the repo.

## Follow-up workflow

Open the day’s CSV in Excel or any editor: columns include `timestamp_local`, `browser`, `profile`, `url`, `title`. For tracking “done vs not done,” use a **separate** notes file or spreadsheet so you do not corrupt the raw log.

## Other layout

- `storage-team/meeting-minutes/` — daily standup template, Confluence mirrors, and sync notes ([folder README](https://github.com/jkugler-ai/Storage_APIs/blob/main/storage-team/meeting-minutes/README.md)).
- `storage-team/confluence-exports/` — Markdown mirrors / summaries of Confluence pages.
- **OV-TPM-Team copy of demo recordings:** [Storage-APIs-Demo-Recordings.md](https://github.com/NVIDIA-dev/OV-TPM-Team/blob/main/Storage%20APIs/storage-demos/Storage-APIs-Demo-Recordings.md) (updated from this repo by [sync workflow](https://github.com/NVIDIA-dev/OV-TPM-Team/blob/main/.github/workflows/sync-storage-demo-recordings.yml); template in [`scripts/ov-tpm-team-sync-workflow.yml`](scripts/ov-tpm-team-sync-workflow.yml)).
