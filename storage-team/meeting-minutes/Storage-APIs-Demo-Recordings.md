# Storage APIs — demo recordings (Confluence mirror)

**Location in repo:** `storage-team/meeting-minutes/` (same content idea as `storage-team/confluence-exports/Storage-APIs-Demo-Recordings.md`; keep one or both depending on how you like to organize.)

**Confluence source:** [Storage APIs Demo Recordings](https://nvidia.atlassian.net/wiki/spaces/OMNIVERSE/pages/2838740706/Storage+APIs+Demo+Recordings) (OMNIVERSE space)

**About this file:** Text was pulled from Confluence through **ECI / MaaS Confluence** (`confluence_get_page`). It is **not** a pixel-perfect wiki export: headings and tables may be flattened, and some blocks repeat (especially AI recap text). Treat the **live Confluence page** as canonical for links, recordings, and formatting.

If the **browser** shows an Atlassian “JavaScript load error” for `id-frontend.prod-east.frontend.public.atl-paas.net`, fix network/VPN or use **MCP** instead of the web UI.

**How to refresh:** In Cursor, ask the agent to run `confluence_get_page` with the same `page_url`, merge edits into this file, then commit and push (see `README.md` in this folder).

---

## Logistics

- **Series:** Storage: Sprint Demos — Weekly (2026)
- **When:** Every **Thursday**, **12:30–1:30 PM ET**
- **Meeting link:** (see Confluence page — not reproduced here)
- **Demos / agenda:** If you want to demo or suggest a topic, add a **comment on the Confluence page** or talk with your leads/managers.

### Demo format (from page)

1. **Part 1 — What I built**
2. **Part 2a — How LLMs were used in development**
3. **Part 2b — How I built it**
4. **Reflections** — what worked / what did not

### Table columns (on wiki)

Date · Demo / discussion topic(s) · Presenter(s) · AI summary · Transcript / recording

---

## Latest session highlights (2026-04-30) — summarized

**Topics called out in the export:** Storage Navigator CLI with Superpowers skill; comparison of Superpowers vs OpenSpec; security review / remediator skills with Claude/Cursor; OneDrive integration (auth, multi-user), OpenSpec workflow (proposal/design/spec/tasks, phases), Portal testing delays (Kit + Omni Storage API Auth extension), MVSB review status, performance (e.g. Astronaut USD graph API / load times), Kubernetes/operator and Helm discussion threads from prior weeks, Chaos Mesh resiliency testing, Live Edit / Rust service work, and more.

**Decisions (as phrased in export):**

- Distribute **Python** OneDrive integration code to **internal testers**.
- Deliver **customer-ready Python** OneDrive code to **BMW**.
- Schedule follow-up to merge **security reviewer / remediator** discussion and demo.

**Open questions (as phrased in export):**

- Provide **both code and skill** to BMW vs **code only** — still open.
- Investigate **issue-surfacing workflow** in Superpowers skills.
- Compare **Teams**, **OpenSpec**, **Superpowers** for quality and workflow granularity.
- Extending security reviewer for **live infiltration** testing — undecided.

**Agenda snippet:** Showcase completed work and process (~20 min built work, ~40 min LLM usage discussion).

---

## Earlier weeks (one line each, from export)

| Date (approx.) | Notes from export |
|----------------|-------------------|
| 2026-04-23 | Kit I/O modeling; Storage API k8s operator; scalable Live-Edit agentic process; broader “LLM and agentic development” themes. |
| 2026-03-25 | Kit test content migration / timestamps; Live Edit via Storage API; cluster resiliency (Chaos Mesh). |
| 2026-03-12 | Siemens EA2 / Kit upstreaming 2.0 themes; deployment doc automation; Storage API + refresh token demo; Navigator testing ideas. |

---

## Push this file to GitHub

From the **repo root** (the folder that contains `storage-team`):

```powershell
cd "C:\Users\jenni\OneDrive - NVIDIA Corporation\Cursor Projects\Daily Things"
git add storage-team\meeting-minutes\Storage-APIs-Demo-Recordings.md
git commit -m "Update Storage APIs demo recordings from Confluence"
git push
```

On GitHub it will appear as:  
[https://github.com/jkugler-ai/Storage_APIs/blob/main/storage-team/meeting-minutes/Storage-APIs-Demo-Recordings.md](https://github.com/jkugler-ai/Storage_APIs/blob/main/storage-team/meeting-minutes/Storage-APIs-Demo-Recordings.md)
