#!/usr/bin/env python3
"""
Export Chromium (Chrome/Edge) and Firefox history visits incrementally to CSV or JSONL.

Copies each locked SQLite DB to a temp file before reading. Watermarks are stored per
(browser, profile) in state/watermarks.json under the repo or paths you pass.
"""

from __future__ import annotations

import argparse
import configparser
import csv
import json
import os
import shutil
import sqlite3
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator
from urllib.parse import urlparse

# Chromium visit_time: microseconds since January 1, 1601 UTC (Windows FILETIME epoch)
CHROME_EPOCH_UTC = datetime(1601, 1, 1, tzinfo=timezone.utc)
UNIX_EPOCH_UTC = datetime(1970, 1, 1, tzinfo=timezone.utc)


def chrome_us_to_utc(us: int) -> datetime:
    return CHROME_EPOCH_UTC + timedelta(microseconds=int(us))


def utc_to_local_iso(dt: datetime) -> str:
    return dt.astimezone().replace(microsecond=0).isoformat()


def firefox_us_to_utc(us: int) -> datetime:
    """Firefox moz_historyvisits.visit_date: microseconds since Unix epoch."""
    return UNIX_EPOCH_UTC + timedelta(microseconds=int(us))


def datetime_to_chrome_us(dt: datetime) -> int:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return int((dt - CHROME_EPOCH_UTC) / timedelta(microseconds=1))


def datetime_to_firefox_us(dt: datetime) -> int:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return int((dt - UNIX_EPOCH_UTC) / timedelta(microseconds=1))


def redact_url(url: str, domains: list[str]) -> str:
    if not domains:
        return url
    try:
        p = urlparse(url)
        host = (p.hostname or "").lower()
    except Exception:
        return url
    for d in domains:
        d = d.strip().lower()
        if d and (host == d or host.endswith("." + d)):
            return "[REDACTED]"
    return url


def load_watermarks(path: Path) -> dict[str, int]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {str(k): int(v) for k, v in data.items()}
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return {}


def save_watermarks(path: Path, marks: dict[str, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(marks, indent=2, sort_keys=True), encoding="utf-8")


def copy_sqlite_src(src: Path) -> Path:
    """Copy DB so we can read while the browser holds a lock on the original."""
    fd, tmp = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    tmp_path = Path(tmp)
    try:
        shutil.copy2(src, tmp_path)
    except OSError as e:
        tmp_path.unlink(missing_ok=True)
        raise RuntimeError(f"Could not copy {src}: {e}") from e
    return tmp_path


@dataclass(frozen=True)
class VisitRow:
    visit_id: int
    visit_time_raw: int
    url: str
    title: str
    transition: int | None

    def as_dict(self, browser: str, profile: str, redact_domains: list[str]) -> dict[str, Any]:
        return {
            "timestamp_local": utc_to_local_iso(self.visit_ts_utc()),
            "browser": browser,
            "profile": profile,
            "url": redact_url(self.url, redact_domains),
            "title": self.title or "",
            "visit_id": self.visit_id,
            "transition": self.transition if self.transition is not None else "",
        }

    def visit_ts_utc(self) -> datetime:
        raise NotImplementedError


@dataclass(frozen=True)
class ChromiumVisit(VisitRow):
    def visit_ts_utc(self) -> datetime:
        return chrome_us_to_utc(self.visit_time_raw)


@dataclass(frozen=True)
class FirefoxVisit(VisitRow):
    def visit_ts_utc(self) -> datetime:
        return firefox_us_to_utc(self.visit_time_raw)


def iter_chromium_visits(db_path: Path, min_visit_time: int) -> Iterator[ChromiumVisit]:
    tmp = copy_sqlite_src(db_path)
    try:
        con = sqlite3.connect(f"file:{tmp}?mode=ro", uri=True)
        try:
            cur = con.execute(
                """
                SELECT v.id, v.visit_time, u.url, u.title, v.transition
                FROM visits v
                JOIN urls u ON u.id = v.url
                WHERE v.visit_time > ?
                ORDER BY v.visit_time ASC
                """,
                (min_visit_time,),
            )
            for vid, vt, url, title, trans in cur:
                yield ChromiumVisit(
                    visit_id=int(vid),
                    visit_time_raw=int(vt),
                    url=str(url or ""),
                    title=str(title or ""),
                    transition=int(trans) if trans is not None else None,
                )
        finally:
            con.close()
    finally:
        tmp.unlink(missing_ok=True)


def iter_firefox_visits(db_path: Path, min_visit_date: int) -> Iterator[FirefoxVisit]:
    tmp = copy_sqlite_src(db_path)
    try:
        con = sqlite3.connect(f"file:{tmp}?mode=ro", uri=True)
        try:
            cur = con.execute(
                """
                SELECT v.id, v.visit_date, p.url, p.title, NULL
                FROM moz_historyvisits v
                JOIN moz_places p ON p.id = v.place_id
                WHERE v.visit_date > ?
                ORDER BY v.visit_date ASC
                """,
                (min_visit_date,),
            )
            for vid, vd, url, title, _ in cur:
                yield FirefoxVisit(
                    visit_id=int(vid),
                    visit_time_raw=int(vd),
                    url=str(url or ""),
                    title=str(title or ""),
                    transition=None,
                )
        finally:
            con.close()
    finally:
        tmp.unlink(missing_ok=True)


def firefox_profile_dirs() -> list[tuple[str, Path]]:
    """Return (profile_name, places.sqlite path) for local Firefox profiles."""
    appdata = os.environ.get("APPDATA")
    if not appdata:
        return []
    ini_path = Path(appdata) / "Mozilla" / "Firefox" / "profiles.ini"
    if not ini_path.is_file():
        return []
    cfg = configparser.ConfigParser()
    cfg.read(ini_path, encoding="utf-8")
    out: list[tuple[str, Path]] = []
    for section in cfg.sections():
        if not section.startswith("Profile"):
            continue
        path_rel = cfg.get(section, "Path", fallback="").strip()
        if not path_rel:
            continue
        is_rel = cfg.get(section, "IsRelative", fallback="1").strip() == "1"
        prof_dir = (
            Path(appdata) / "Mozilla" / "Firefox" / path_rel
            if is_rel
            else Path(path_rel)
        )
        places = prof_dir / "places.sqlite"
        if places.is_file():
            name = cfg.get(section, "Name", fallback=prof_dir.name)
            out.append((name, places))
    return out


def chromium_user_data_base(browser: str) -> Path | None:
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        return None
    base = Path(local)
    if browser == "chrome":
        return base / "Google" / "Chrome" / "User Data"
    if browser == "edge":
        return base / "Microsoft" / "Edge" / "User Data"
    return None


def history_path_chromium(user_data: Path, profile_folder: str) -> Path:
    return user_data / profile_folder / "History"


def default_output_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "logs"


def default_state_path() -> Path:
    return Path(__file__).resolve().parent.parent / "state" / "watermarks.json"


def append_csv(path: Path, rows: list[dict[str, Any]], write_header: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "timestamp_local",
        "browser",
        "profile",
        "url",
        "title",
        "visit_id",
        "transition",
    ]
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        if write_header:
            w.writeheader()
        for r in rows:
            w.writerow(r)


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main() -> int:
    p = argparse.ArgumentParser(description="Export browser history visits to CSV or JSONL.")
    p.add_argument(
        "--browsers",
        default="chrome,edge,firefox",
        help="Comma list: chrome,edge,firefox (default: all three)",
    )
    p.add_argument(
        "--chromium-profiles",
        default="Default",
        help="Comma-separated Chromium profile folders under User Data (e.g. Default,Profile 1)",
    )
    p.add_argument(
        "--firefox-profile",
        action="append",
        default=[],
        metavar="NAME_OR_PATH",
        help="Firefox profile name from profiles.ini, or full path to profile folder containing places.sqlite. "
        "Repeatable. If omitted with firefox enabled, all discovered profiles are used.",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=f"Daily files written here (default: {default_output_dir()})",
    )
    p.add_argument(
        "--state-file",
        type=Path,
        default=None,
        help=f"Watermark JSON path (default: {default_state_path()})",
    )
    p.add_argument(
        "--format",
        choices=("csv", "jsonl"),
        default="csv",
        help="Output format (default: csv)",
    )
    p.add_argument(
        "--lookback-days",
        type=int,
        default=7,
        help="When no watermark exists yet, only export visits from this many days ago (default: 7)",
    )
    p.add_argument(
        "--redact-domain",
        action="append",
        default=[],
        metavar="HOST",
        help="If URL host matches, replace URL with [REDACTED]. Repeatable.",
    )
    args = p.parse_args()

    browsers = {b.strip().lower() for b in args.browsers.split(",") if b.strip()}
    output_dir = (args.output_dir or default_output_dir()).resolve()
    state_file = (args.state_file or default_state_path()).resolve()
    redact = list(args.redact_domain or [])
    lookback = max(1, int(args.lookback_days))

    now_utc = datetime.now(timezone.utc)
    chrome_floor = datetime_to_chrome_us(now_utc - timedelta(days=lookback))
    firefox_floor = int((now_utc - timedelta(days=lookback) - UNIX_EPOCH_UTC) / timedelta(microseconds=1))

    watermarks = load_watermarks(state_file)
    chromium_profiles = [s.strip() for s in args.chromium_profiles.split(",") if s.strip()]

    day_stamp = datetime.now().astimezone().date().isoformat()
    out_file = output_dir / f"visits-{day_stamp}.{args.format}"
    first_write = not out_file.exists()

    total = 0
    errors: list[str] = []

    def state_key(browser: str, profile: str) -> str:
        return f"{browser}:{profile}"

    def process_chromium(browser_label: str, profile_folder: str) -> None:
        nonlocal total, first_write
        base = chromium_user_data_base(browser_label)
        if base is None or not base.is_dir():
            errors.append(f"{browser_label}: User Data not found ({base})")
            return
        hist = history_path_chromium(base, profile_folder)
        if not hist.is_file():
            errors.append(f"{browser_label}/{profile_folder}: no History file")
            return
        key = state_key(browser_label, profile_folder)
        key_wm = watermarks.get(key, 0)
        min_vt = key_wm if key_wm > 0 else chrome_floor
        rows_out: list[dict[str, Any]] = []
        max_vt = min_vt
        try:
            for v in iter_chromium_visits(hist, min_vt):
                max_vt = max(max_vt, v.visit_time_raw)
                rows_out.append(
                    v.as_dict(
                        browser=browser_label,
                        profile=profile_folder,
                        redact_domains=redact,
                    )
                )
        except RuntimeError as e:
            errors.append(str(e))
            return
        if rows_out:
            if args.format == "csv":
                append_csv(out_file, rows_out, write_header=first_write)
                first_write = False
            else:
                append_jsonl(out_file, rows_out)
            total += len(rows_out)
            watermarks[key] = max_vt
        elif key_wm == 0:
            watermarks[key] = datetime_to_chrome_us(now_utc)

    if "chrome" in browsers:
        for prof in chromium_profiles:
            process_chromium("chrome", prof)
    if "edge" in browsers:
        for prof in chromium_profiles:
            process_chromium("edge", prof)

    if "firefox" in browsers:
        ff_specs: list[tuple[str, Path]] = []
        if args.firefox_profile:
            for spec in args.firefox_profile:
                spec = spec.strip()
                path = Path(spec)
                if path.is_dir() and (path / "places.sqlite").is_file():
                    ff_specs.append((path.name, path / "places.sqlite"))
                elif path.is_file() and path.name == "places.sqlite":
                    ff_specs.append((path.parent.name, path))
                else:
                    for name, pl in firefox_profile_dirs():
                        if name == spec or Path(name).name == spec:
                            ff_specs.append((name, pl))
                            break
                    else:
                        errors.append(f"firefox: could not resolve profile {spec!r}")
        else:
            ff_specs = firefox_profile_dirs()
            if not ff_specs:
                errors.append("firefox: no profiles.ini or places.sqlite found")

        for prof_name, places_path in ff_specs:
            key = state_key("firefox", prof_name)
            key_wm = watermarks.get(key, 0)
            min_vd = key_wm if key_wm > 0 else firefox_floor
            rows_out: list[dict[str, Any]] = []
            max_vd = min_vd
            try:
                for v in iter_firefox_visits(places_path, min_vd):
                    max_vd = max(max_vd, v.visit_time_raw)
                    rows_out.append(
                        v.as_dict(
                            browser="firefox",
                            profile=prof_name,
                            redact_domains=redact,
                        )
                    )
            except RuntimeError as e:
                errors.append(str(e))
                continue
            if rows_out:
                if args.format == "csv":
                    append_csv(out_file, rows_out, write_header=first_write)
                    first_write = False
                else:
                    append_jsonl(out_file, rows_out)
                total += len(rows_out)
                watermarks[key] = max_vd
            elif key_wm == 0:
                watermarks[key] = datetime_to_firefox_us(now_utc)

    save_watermarks(state_file, watermarks)

    if total:
        print(f"Wrote {total} visit(s) to {out_file}")
    else:
        print(f"No new visits in this run. Next rows append to: {out_file}")
    if errors:
        print("Warnings:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
