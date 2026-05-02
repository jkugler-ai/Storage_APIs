# Storage Team — meeting minutes

Daily notes live here as Markdown (`.md`) files.

**Confluence mirror in this folder:** [Storage-APIs-Demo-Recordings.md](./Storage-APIs-Demo-Recordings.md) — sprint demo page exported/summarized from [Confluence](https://nvidia.atlassian.net/wiki/spaces/OMNIVERSE/pages/2838740706/Storage+APIs+Demo+Recordings). Refresh via Cursor **MaaS Confluence** (`confluence_get_page`) or copy from the browser, then commit and push.

**Expanded Confluence tables → Markdown:** [CONFLUENCE-COPY-EXPANDED-TABLE.md](./CONFLUENCE-COPY-EXPANDED-TABLE.md) (browser copy / export) and `python scripts/confluence_eci_flat_to_markdown.py` (all ECI text into `<details>` sections).

## How to add a new day

1. Copy `_TEMPLATE-daily.md`.
2. Rename to **`YYYY-MM-DD.md`** (example: `2026-05-02.md`).
3. Optionally put it under a year folder (`2026/2026-05-02.md`) if the list gets long.
4. Fill in during or right after the meeting.

## Tips

- **Search**: Cursor / VS Code search across this folder to find decisions or names later.
- **Privacy**: This project folder may sync with OneDrive. Do not paste secrets, credentials, or customer data. If you later connect this repo to **public** GitHub, either keep minutes out of git (see `.gitignore`) or scrub sensitive lines first.

## Optional: team wiki instead

If your team already standardizes on **Confluence** or **SharePoint**, those can be better for shared editing and permissions. This folder is ideal for **personal** scratch minutes you own and can reorganize anytime.

## GitHub — [Storage_APIs](https://github.com/jkugler-ai/Storage_APIs)

This **Daily Things** project root is a Git repo whose `origin` is `https://github.com/jkugler-ai/Storage_APIs.git`. Meeting minutes, the export script, and `README.md` live there; `logs\` and `state/watermarks.json` stay local (`.gitignore`).

**First push on your machine:** open a terminal in the project root and run `git push -u origin main` if the branch is not on GitHub yet. Sign in when prompted, or use a [personal access token](https://github.com/settings/tokens) as the HTTPS password.

**Day-to-day:**

```powershell
cd "C:\Users\jenni\OneDrive - NVIDIA Corporation\Cursor Projects\Daily Things"
git add storage-team\meeting-minutes
git commit -m "Meeting notes 2026-05-02"
git push
```

You can also use **Cursor → Source Control**: stage, commit, push.
