# Confluence → GitHub (Markdown)

This folder holds **Markdown mirrors** of selected Confluence pages (for example [Storage APIs Demo Recordings](https://nvidia.atlassian.net/wiki/spaces/OMNIVERSE/pages/2838740706/Storage+APIs+Demo+Recordings)).

## Flow

1. **Fetch** page text with Cursor + **MaaS Confluence** MCP (`confluence_get_page` + `page_url`), or copy from the browser.
2. **Edit** into `.md` (structure, headings, tables). The Confluence page remains the source of truth for permissions and rich embeds.
3. **Commit** from the repo root and **`git push`** to [jkugler-ai/Storage_APIs](https://github.com/jkugler-ai/Storage_APIs).

## Policy reminder

Do not commit **secrets**, credentials, or **export-controlled / confidential** material your org would not put on GitHub. Prefer **private** repos for internal runbooks.
