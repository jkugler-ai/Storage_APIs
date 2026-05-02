# Session reference — Markdown, GitHub, Confluence, mirrors

*Paste this page into Microsoft OneNote if you want it there: open this file in Cursor → Select All → Copy → paste into a OneNote page.*

---

## Markdown (`.md`) and GitHub

- **`.md`** = Markdown: plain text that GitHub (and Cursor) can render (headings, lists, **tables**, links).
- **On GitHub:** **Add file** / pencil **Edit**, or edit locally → `git add` → `git commit` → `git push`.
- **Tables:** every row needs the **same number of `|` columns** as the header. Common mistake: you **remove a column from the header** but leave an **extra `|---|` segment** in the separator row — the table breaks.

---

## Git & `Storage_APIs`

- **Repo:** [jkugler-ai/Storage_APIs](https://github.com/jkugler-ai/Storage_APIs) (public for raw URLs + sync).
- **`git push` rejected (“fetch first”):** the remote has commits you don’t. Run **`git pull origin main --rebase`**, fix conflicts if any, then **`git push`**.
- **`.gitignore` (highlights):** `__pycache__/`, `*.pyc`, `logs/`, `state/watermarks.json`, `storage-team/meeting-minutes/_eci_latest/`, `_ov-tpm-team-clone/`, `_ovstorage-clone/`.

---

## Cursor `mcp.json` (GitHub MCP)

- **Single JSON root** — don’t concatenate two top-level `{ ... }{ ... }` objects.
- **`Authorization`:** one valid string: `"Bearer <token>"` — missing closing `"` or truncated token → **“Unexpected end of string”**.
- Prefer **official GitHub MCP** / hosted URL; avoid deprecated **`@modelcontextprotocol/server-github`** npm package.

---

## Meeting minutes & Confluence

- **Local folder:** `storage-team/meeting-minutes/` — `_TEMPLATE-daily.md`, `README.md`, demo recordings mirror.
- **Confluence:** [Storage APIs Demo Recordings](https://nvidia.atlassian.net/wiki/spaces/OMNIVERSE/pages/2838740706/Storage+APIs+Demo+Recordings). Browser may show **Atlassian / JS** errors; **MaaS Confluence MCP** (`confluence_get_page`) can still return text.
- **ECI ≠ full wiki UI:** MCP returns **flattened text chunks**, not guaranteed parity with **expanded** Confluence tables/macros. For true expanded content, copy from Confluence or export — see **`CONFLUENCE-COPY-EXPANDED-TABLE.md`** in this folder.
- **Repo tooling:**
  - `eci-page.json` — ECI `content[]` snapshot.
  - `scripts/confluence_eci_flat_to_markdown.py` → **`Storage-APIs-Demo-Recordings-from-eci.md`** (parsed date table + `<details>` per segment).
  - `scripts/assemble_eci_json_from_segments.py` — rebuild `eci-page.json` from `_eci_latest/00.txt` … `28.txt`.

---

## Ongoing mirror (NVIDIA org repos)

- **Idea:** workflow in the **destination** repo `curl`s the **public raw** file from `Storage_APIs` and commits only if changed; uses **`GITHUB_TOKEN`**; **`actions/checkout@v5`** (Node 24).
- **OV-TPM-Team:** [workflow](https://github.com/NVIDIA-dev/OV-TPM-Team/blob/main/.github/workflows/sync-storage-demo-recordings.yml) · [mirrored doc](https://github.com/NVIDIA-dev/OV-TPM-Team/blob/main/docs/storage-demos/Storage-APIs-Demo-Recordings.md). After changes, run the workflow once from **Actions**.
- **ovstorage:** same workflow + file were prepared locally; **push needed write access** (403). When you have access: push from clone or add files manually. **Template:** [scripts/ov-tpm-team-sync-workflow.yml](https://github.com/jkugler-ai/Storage_APIs/blob/main/scripts/ov-tpm-team-sync-workflow.yml).

---

## Commands you reuse

```powershell
cd "C:\Users\jenni\OneDrive - NVIDIA Corporation\Cursor Projects\Daily Things"

git add .
git commit -m "Describe change"
git pull origin main --rebase   # if push rejected
git push

python scripts\confluence_eci_flat_to_markdown.py storage-team\meeting-minutes\eci-page.json -o storage-team\meeting-minutes\Storage-APIs-Demo-Recordings-from-eci.md
```

---

## Security / hygiene

- Don’t commit **PATs** or material that shouldn’t be on a **public** repo.
- Treat **Teams / SharePoint** links like any internal link.
