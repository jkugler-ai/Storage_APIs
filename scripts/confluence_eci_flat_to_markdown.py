"""
Turn a Confluence ECI / MCP `confluence_get_page` JSON payload into Markdown.

Input shapes supported:
  - Full tool wrapper: {"success": true, "data": {"results": [{"content": ["...", ...]}]}}
  - {"data": {"results": [{"content": [...]}]}}
  - {"results": [{"content": [...]}]}
  - {"content": ["...", ...]}
  - JSON Lines: one JSON string per line (each line is a quoted string)

Output:
  - Front matter + intro
  - A GitHub-flavored Markdown table for rows that look like: "# YYYY-MM-DD , ..."
  - An appendix with every segment in <details> blocks (good for long "expanded" text)
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


DATE_ROW = re.compile(r"^#\s*(\d{4}-\d{2}-\d{2})\s*,\s*(.*)$", re.DOTALL)
HEADER_ROW = re.compile(r"^#\s*Date\s*,", re.IGNORECASE)


def _load_payload(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        out: list[str] = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
        return out

    data = json.loads(raw)
    if isinstance(data, list) and data and isinstance(data[0], str):
        return data  # type: ignore[return-value]

    if isinstance(data, dict):
        if "content" in data and isinstance(data["content"], list):
            return [str(x) for x in data["content"]]  # type: ignore[arg-type]
        results = data.get("results") or data.get("data", {}).get("results")
        if isinstance(results, list) and results:
            first = results[0]
            if isinstance(first, dict) and isinstance(first.get("content"), list):
                return [str(x) for x in first["content"]]  # type: ignore[index]

        data2 = data.get("data")
        if isinstance(data2, dict):
            results2 = data2.get("results")
            if isinstance(results2, list) and results2:
                first2 = results2[0]
                if isinstance(first2, dict) and isinstance(first2.get("content"), list):
                    return [str(x) for x in first2["content"]]  # type: ignore[index]

    raise SystemExit("Could not find a string list under content / data.results[0].content")


def _md_cell(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n").strip()
    s = s.replace("|", "\\|")
    s = re.sub(r"\s+", " ", s)
    return s


def _segments_to_markdown(segments: Iterable[str], source_url: str) -> str:
    segs = list(segments)
    lines: list[str] = []
    lines.append("# Confluence export (ECI flatten → Markdown)\n")
    lines.append(
        "**Source:** "
        + (f"<{source_url}>\n" if source_url else "(add your Confluence URL)\n")
    )
    lines.append(
        "\n**Note:** This file is generated from `confluence_get_page` text chunks. "
        "It is **not** identical to Confluence’s live UI (macros, true column widths, "
        "or some expand/collapse states). For pixel-perfect copies of expanded table rows, "
        "see `storage-team/meeting-minutes/CONFLUENCE-COPY-EXPANDED-TABLE.md`.\n"
    )

    lines.append("\n## Demo / recording table (parsed `# YYYY-MM-DD , …` rows)\n\n")
    lines.append("| Date | Demo / discussion (ECI text) |\n")
    lines.append("|------|--------------------------------|\n")

    found = False
    for s in segs:
        m = DATE_ROW.match(s.strip())
        if not m:
            continue
        found = True
        date, rest = m.group(1), m.group(2)
        lines.append(f"| {_md_cell(date)} | {_md_cell(rest)} |\n")
    if not found:
        lines.append("| *(none)* | No rows matched `# YYYY-MM-DD , …` in this payload. |\n")

    lines.append("\n## Appendix — all ECI segments\n")
    for i, s in enumerate(segs):
        title = f"Segment {i}"
        body = html.escape(s, quote=False)
        lines.append(f"\n<details><summary>{html.escape(title)}</summary>\n\n")
        lines.append(f"<pre>{body}</pre>\n\n")
        lines.append("</details>\n")

    return "".join(lines)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path, help="Path to JSON or .jsonl from MCP/ECI")
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("-"),
        help="Output Markdown path (default: stdout)",
    )
    p.add_argument(
        "--source-url",
        default="https://nvidia.atlassian.net/wiki/spaces/OMNIVERSE/pages/2838740706/Storage+APIs+Demo+Recordings",
        help="Confluence page URL to cite in the Markdown header",
    )
    args = p.parse_args()

    segments = _load_payload(args.input)
    md = _segments_to_markdown(segments, args.source_url.strip())

    if str(args.output) == "-":
        sys.stdout.write(md)
    else:
        args.output.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
