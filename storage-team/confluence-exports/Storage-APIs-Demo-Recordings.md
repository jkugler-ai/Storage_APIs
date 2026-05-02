# Storage APIs — demo recordings (Confluence mirror)

**Confluence source:** [Storage APIs Demo Recordings](https://nvidia.atlassian.net/wiki/spaces/OMNIVERSE/pages/2838740706/Storage+APIs+Demo+Recordings) (OMNIVERSE space)

**About this file:** Text below was pulled from Confluence through **ECI / MaaS Confluence** (`confluence_get_page`). It is **not** a pixel-perfect wiki export: headings and tables may be flattened, and some blocks repeat (especially AI recap text). Treat the **live Confluence page** as canonical for links, recordings, and formatting.

**How to refresh:** In Cursor, ask the agent to run `confluence_get_page` with the same `page_url`, then replace the body under “Exported body” or merge edits as you prefer. Commit and `git push` to [Storage_APIs](https://github.com/jkugler-ai/Storage_APIs).

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

**Topics called out in the export:** Storage Navigator CLI with Superpowers skill; comparison of Superpowers vs OpenSpec; security review / remediator skills with Claude/Cursor; OneDrive integration (auth, multi-user), OpenSpec workflow (proposal/design/spec/tasks, phases), Portal testing delays (Kit + Omni Storage API Auth extension), MVSB review status, performance (e.g. Astronaut USD graph API / load times), Kubernetes/operator and Helm discussion threads from prior weeks, Chaos Mesh resiliency testing, Live Edit / Rust service work, and more (see long recap segments in **Exported body**).

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

## Full verbatim text (optional)

The live Confluence page can be long, and ECI often returns **many long “AI summary” paragraphs** that repeat. Putting the entire raw `content[]` dump into Git makes the repo noisy and this patch channel is not ideal for megabyte-sized blobs.

**To append the full raw export into this repo as Markdown:**

1. In Cursor chat, ask the agent to call **`confluence_get_page`** with  
   `page_url` = `https://nvidia.atlassian.net/wiki/spaces/OMNIVERSE/pages/2838740706/Storage+APIs+Demo+Recordings`  
   and `max_length` = `100000` (raise if the tool errors on size).
2. Paste the returned `content` strings into a new section at the bottom of this file (for example under `## Appendix — raw ECI segments`), or save them as a second file such as `Storage-APIs-Demo-Recordings-appendix.md`.
3. From the **Daily Things** repo root:

```powershell
cd "C:\Users\jenni\OneDrive - NVIDIA Corporation\Cursor Projects\Daily Things"
git add storage-team\confluence-exports
git commit -m "Refresh Storage APIs demo recordings from Confluence"
git push
```

**Alternative (no MCP):** In the browser, open the [Confluence page](https://nvidia.atlassian.net/wiki/spaces/OMNIVERSE/pages/2838740706/Storage+APIs+Demo+Recordings), copy sections, paste into a `.md` file, then commit and push. If your space supports **Export** (Word/PDF), you can export and then convert—results vary.
