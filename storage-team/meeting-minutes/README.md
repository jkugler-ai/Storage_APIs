# Storage Team — meeting minutes

Daily notes live here as Markdown (`.md`) files.

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

## Save these `.md` files on GitHub

Your **Daily Things** folder is not a Git repo until you run `git init` once at the project root. After that, each new or edited `.md` file is committed and pushed like any other file.

### 1. Create a repository on GitHub

1. Open [github.com/new](https://github.com/new).
2. Name it (for example `daily-things` or `storage-meeting-minutes`).
3. Choose **Public** or **Private** (private if minutes mention internal projects).
4. Leave **Add a README** unchecked so your first push is simple.

### 2. Turn the project folder into a repo and push (PowerShell)

Run these from the **Daily Things** project root (the folder that contains `storage-team\`, `scripts\`, and `.gitignore`):

```powershell
cd "C:\Users\jenni\OneDrive - NVIDIA Corporation\Cursor Projects\Daily Things"
git init
git add .
git commit -m "Initial commit: Storage meeting minutes and project files"
git branch -M main
git remote add origin https://github.com/jkugler-ai/YOUR_REPO_NAME.git
git push -u origin main
```

Replace `YOUR_REPO_NAME` with the name you chose on GitHub. GitHub may ask you to sign in or use a **personal access token** as the password when using HTTPS.

`logs\` and `state\` stay **out** of GitHub because they are listed in `.gitignore` (good for privacy). Your `.md` files under `storage-team\` **will** be pushed.

### 3. Day-to-day after that

```powershell
cd "C:\Users\jenni\OneDrive - NVIDIA Corporation\Cursor Projects\Daily Things"
git add storage-team\meeting-minutes
git commit -m "Meeting notes 2026-05-02"
git push
```

You can also use **Cursor’s Source Control** view: stage changed files, commit, push.

### Repo with only meeting minutes (optional)

If you want a **separate** GitHub repo that contains **only** this `meeting-minutes` folder, say so and we can set that layout up (either a subfolder-only repo or a split project).
