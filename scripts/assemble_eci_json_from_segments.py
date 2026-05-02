"""Merge `storage-team/meeting-minutes/_eci_latest/00.txt` … `28.txt` into `eci-page.json`."""

from __future__ import annotations

import json
import re
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    seg_dir = root / "storage-team" / "meeting-minutes" / "_eci_latest"
    paths = sorted(seg_dir.glob("[0-9][0-9].txt"), key=lambda p: int(re.findall(r"\d+", p.stem)[0]))
    if len(paths) != 29:
        raise SystemExit(f"Expected 29 segment files in {seg_dir}, found {len(paths)}")
    content = [p.read_text(encoding="utf-8").rstrip("\n") for p in paths]
    out = root / "storage-team" / "meeting-minutes" / "eci-page.json"
    out.write_text(json.dumps({"content": content}, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out} ({len(content)} segments)")


if __name__ == "__main__":
    main()
