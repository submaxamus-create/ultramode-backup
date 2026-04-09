#!/usr/bin/env python3
# =============================================================================
# FILENAME: um_script_map_builder.py
# FOLDER PATH: /userdata/system/ultramode/modules/tools/script_indexer/
# DESTINATION: /userdata/system/ultramode/modules/tools/script_indexer/um_script_map_builder.py
# PATCH TYPE: FULL
# VERSION: 1
# REVISION: 1
# SUMMARY: Scans UltraMode folders, reads headers and notation, and writes an
# append-friendly AI-readable master script index log with file paths, purpose,
# version/revision, and summary information.
# =============================================================================

# ### ULTRAMODE PROTECTED START
# Hi Mom.
# ### ULTRAMODE PROTECTED END

# ULTRAMODE NOTATION BLOCK — DO NOT DELETE OR MODIFY EXISTING LINES — ONLY APPEND
#
# [CHANGELOG]
# - 2026-04-04 03:18pm: Initial scanner skeleton created for append-friendly
#   UltraMode script/file index mapping.
#
# [GOAL]
# - Build a readable shared map of scripts and selected txt/log files.
# - Help AI and user know what files exist, where they are, and what they do.
# - Produce an append-friendly log that can also be replaced when desired.
#
# [CURRENT_SCOPE]
# - Scans .py and selected .txt files.
# - Reads patcher headers when present.
# - Extracts purpose/summary/version/revision.
# - Writes a structured index log.
#
# [FUTURE_IDEAS]
# - best-current-file detection
# - duplicate version detection
# - obsolete file warnings
# - header quality score
# - module grouping
# - sidecar/log relationship detection
# - export to multiple reports

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List

DEFAULT_ROOT = Path("/userdata/system/ultramode")
DEFAULT_OUTPUT = Path("/userdata/system/ultramode/um_master_logs/index/um_script_index_log.txt")
SCAN_EXTENSIONS = {".py", ".txt"}
SKIP_DIR_NAMES = {"__pycache__", ".git", ".mypy_cache", ".pytest_cache", ".venv", "venv"}
SKIP_FILE_PREFIXES = {"."}
MAX_READ_BYTES = 512 * 1024
HEADER_SCAN_LINES = 80
BODY_SCAN_LINES = 220

@dataclass
class FileRecord:
    filename: str
    full_path: str
    relative_path: str
    extension: str
    size_bytes: int
    modified_time: str
    file_hash12: str
    header_filename: str = ""
    header_folder_path: str = ""
    header_destination: str = ""
    patch_type: str = ""
    version: str = ""
    revision: str = ""
    summary: str = ""
    purpose_guess: str = ""
    categories_found: str = ""
    protected_block: str = ""
    has_notation_block: str = ""
    has_header: str = ""
    status_guess: str = ""
    sidecar_guess: str = ""
    related_files: str = ""

def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %I:%M%p").lower()

def safe_read_text(path: Path) -> str:
    try:
        with path.open("rb") as f:
            data = f.read(MAX_READ_BYTES)
        return data.decode("utf-8", errors="replace")
    except Exception as exc:
        return f"[READ_ERROR] {exc}"

def file_hash12(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with path.open("rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                h.update(chunk)
    except Exception:
        return "read_error"
    return h.hexdigest()[:12]

def should_skip_dir(dirname: str) -> bool:
    return dirname in SKIP_DIR_NAMES

def should_skip_file(path: Path) -> bool:
    if path.suffix.lower() not in SCAN_EXTENSIONS:
        return True
    return any(path.name.startswith(prefix) for prefix in SKIP_FILE_PREFIXES)

def detect_sidecar_guess(path: Path) -> str:
    name = path.name.lower()
    if name.endswith("_log.txt"):
        return "log_sidecar"
    if name.endswith("_help.txt") or name.endswith("_help_log.txt"):
        return "help_sidecar"
    if name.endswith("_thinktank.txt") or name.endswith("_thinktank_log.txt"):
        return "thinktank_sidecar"
    if path.suffix.lower() == ".txt":
        return "txt_misc"
    return ""

HEADER_KEYS = {
    "FILENAME": "header_filename",
    "FOLDER PATH": "header_folder_path",
    "DESTINATION": "header_destination",
    "PATCH TYPE": "patch_type",
    "VERSION": "version",
    "REVISION": "revision",
    "SUMMARY": "summary",
}
CATEGORY_RE = re.compile(r"^\[(.+?)\]\s*$", re.MULTILINE)

def parse_header_fields(text: str) -> Dict[str, str]:
    result = {v: "" for v in HEADER_KEYS.values()}
    for line in text.splitlines()[:HEADER_SCAN_LINES]:
        clean = line.strip().lstrip("#").strip()
        for key, target in HEADER_KEYS.items():
            prefix = f"{key}:"
            if clean.upper().startswith(prefix):
                result[target] = clean[len(prefix):].strip()
    return result

def has_protected_block(text: str) -> bool:
    return "### ULTRAMODE PROTECTED START" in text and "### ULTRAMODE PROTECTED END" in text

def has_notation_block(text: str) -> bool:
    return "ULTRAMODE NOTATION BLOCK" in text

def extract_categories(text: str) -> List[str]:
    found = CATEGORY_RE.findall(text)
    seen = []
    for item in found:
        item = item.strip()
        if item and item not in seen:
            seen.append(item)
    return seen[:20]

def first_meaningful_docline(text: str) -> str:
    for line in text.splitlines()[:BODY_SCAN_LINES]:
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            s = s.lstrip("#").strip()
        if not s:
            continue
        if s.startswith(("FILENAME:", "FOLDER PATH:", "DESTINATION:", "PATCH TYPE:", "VERSION:", "REVISION:", "SUMMARY:")):
            continue
        if "ULTRAMODE PROTECTED" in s or s == "Hi Mom." or "ULTRAMODE NOTATION BLOCK" in s:
            continue
        return s[:220]
    return ""

def guess_purpose(path: Path, text: str, header_summary: str) -> str:
    lower_name = path.name.lower()
    lower_text = text.lower()
    if header_summary:
        return header_summary
    guesses = [("theme", "shared theme / UI drawing support"), ("patcher", "patching or patch workflow tool"), ("harvester", "rule harvesting / indexing / organization tool"), ("index", "indexing / mapping / inventory tool"), ("github", "GitHub integration / backup tool"), ("discover", "discovery / scanning / inspection tool"), ("orphan", "orphan file/media finding tool"), ("gamepad", "gamepad / input helper"), ("gui", "GUI / layout helper"), ("help", "help / notes / guidance file"), ("log", "log / sidecar / notes file")]
    for needle, label in guesses:
        if needle in lower_name or needle in lower_text:
            return label
    doc = first_meaningful_docline(text)
    return doc if doc else "purpose_unknown"

def guess_status(path: Path, header: Dict[str, str], text: str) -> str:
    ext = path.suffix.lower()
    has_header = bool(header.get("header_filename") or header.get("summary"))
    notation = has_notation_block(text)
    protected = has_protected_block(text)
    if ext == ".py" and has_header and notation and protected:
        return "structured_python"
    if ext == ".py" and notation:
        return "python_with_notation"
    if ext == ".py":
        return "python_unstructured"
    if ext == ".txt" and has_header and notation:
        return "patcher_capable_txt"
    if ext == ".txt" and notation:
        return "notation_txt"
    if ext == ".txt":
        return "plain_txt"
    return "unknown"

def guess_related_files(path: Path, folder_files: List[Path]) -> str:
    stem = path.stem.lower()
    matches = []
    for other in folder_files:
        if other == path:
            continue
        other_stem = other.stem.lower()
        if stem == other_stem or stem in other_stem or other_stem in stem:
            matches.append(other.name)
    return ", ".join(sorted(matches)[:12])

def parse_file(path: Path, root: Path, folder_files: List[Path]) -> FileRecord:
    text = safe_read_text(path)
    stat = path.stat()
    header = parse_header_fields(text)
    categories = extract_categories(text)
    rel = str(path.relative_to(root)) if path.is_relative_to(root) else str(path)
    return FileRecord(
        filename=path.name, full_path=str(path), relative_path=rel, extension=path.suffix.lower(),
        size_bytes=stat.st_size, modified_time=datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %I:%M%p").lower(),
        file_hash12=file_hash12(path), header_filename=header["header_filename"], header_folder_path=header["header_folder_path"],
        header_destination=header["header_destination"], patch_type=header["patch_type"], version=header["version"],
        revision=header["revision"], summary=header["summary"], purpose_guess=guess_purpose(path, text, header["summary"]),
        categories_found=", ".join(categories), protected_block="yes" if has_protected_block(text) else "no",
        has_notation_block="yes" if has_notation_block(text) else "no", has_header="yes" if any(header.values()) else "no",
        status_guess=guess_status(path, header, text), sidecar_guess=detect_sidecar_guess(path), related_files=guess_related_files(path, folder_files)
    )

def collect_files(root: Path) -> List[Path]:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
        base = Path(dirpath)
        for name in filenames:
            path = base / name
            if not should_skip_file(path):
                files.append(path)
    return sorted(files, key=lambda p: str(p).lower())

def build_records(root: Path) -> List[FileRecord]:
    all_files = collect_files(root)
    by_folder: Dict[Path, List[Path]] = {}
    for path in all_files:
        by_folder.setdefault(path.parent, []).append(path)
    return [parse_file(path, root, by_folder.get(path.parent, [])) for path in all_files]

def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def write_full_report(output_path: Path, root: Path, records: List[FileRecord]) -> None:
    ensure_parent(output_path)
    lines = [
        "FILENAME: um_script_index_log.txt",
        "FOLDER PATH: /userdata/system/ultramode/um_master_logs/index/",
        "DESTINATION: /userdata/system/ultramode/um_master_logs/index/um_script_index_log.txt",
        "PATCH TYPE: FULL",
        "VERSION: 1",
        "REVISION: 0",
        "SUMMARY: UltraMode master script/file index generated by um_script_map_builder.py",
        "",
        "### ULTRAMODE PROTECTED START",
        "Hi Mom.",
        "### ULTRAMODE PROTECTED END",
        "",
        "# ULTRAMODE NOTATION BLOCK — DO NOT DELETE OR MODIFY EXISTING LINES — ONLY APPEND",
        "",
        "[CHANGELOG]",
        f"- {now_stamp()}: Full index report generated.",
        "",
        "[SCAN_INFO]",
        f"- root: {root}",
        f"- files_indexed: {len(records)}",
        f"- output: {output_path}",
        "",
        "[SUMMARY]",
        f"- python_files: {sum(1 for r in records if r.extension == '.py')}",
        f"- txt_files: {sum(1 for r in records if r.extension == '.txt')}",
        "",
        "[INDEX_ENTRIES]",
        "",
    ]
    for idx, rec in enumerate(records, start=1):
        lines.extend([
            f"[[ENTRY {idx:04d}]]", f"filename: {rec.filename}", f"full_path: {rec.full_path}", f"relative_path: {rec.relative_path}",
            f"extension: {rec.extension}", f"size_bytes: {rec.size_bytes}", f"modified_time: {rec.modified_time}", f"file_hash12: {rec.file_hash12}",
            f"header_filename: {rec.header_filename}", f"header_folder_path: {rec.header_folder_path}", f"header_destination: {rec.header_destination}",
            f"patch_type: {rec.patch_type}", f"version: {rec.version}", f"revision: {rec.revision}", f"summary: {rec.summary}",
            f"purpose_guess: {rec.purpose_guess}", f"categories_found: {rec.categories_found}", f"protected_block: {rec.protected_block}",
            f"has_notation_block: {rec.has_notation_block}", f"has_header: {rec.has_header}", f"status_guess: {rec.status_guess}",
            f"sidecar_guess: {rec.sidecar_guess}", f"related_files: {rec.related_files}", ""
        ])
    output_path.write_text("\n".join(lines), encoding="utf-8")

def append_scan_note(output_path: Path, root: Path, records: List[FileRecord]) -> None:
    ensure_parent(output_path)
    if not output_path.exists():
        write_full_report(output_path, root, records)
        return
    lines = ["", "[SCAN_APPEND]", f"- {now_stamp()}: scan complete", f"- root: {root}", f"- files_indexed: {len(records)}", f"- python_files: {sum(1 for r in records if r.extension == '.py')}", f"- txt_files: {sum(1 for r in records if r.extension == '.txt')}", "- note: full entry rewrite not performed in append mode", ""]
    with output_path.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))

def print_summary(records: List[FileRecord]) -> None:
    print("=" * 72)
    print("ULTRAMODE SCRIPT MAP BUILDER")
    print("=" * 72)
    print(f"Files indexed: {len(records)}")
    print(f"Python: {sum(1 for r in records if r.extension == '.py')}")
    print(f"Text:   {sum(1 for r in records if r.extension == '.txt')}")
    print("")
    print("Sample entries:")
    for rec in records[:12]:
        vr = f"v{rec.version} r{rec.revision}".strip() if rec.version or rec.revision else "no version"
        print(f"- {rec.relative_path} | {vr} | {rec.purpose_guess}")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build an UltraMode script/file index log.")
    parser.add_argument("--root", default=str(DEFAULT_ROOT), help="Root folder to scan.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output index log path.")
    parser.add_argument("--mode", choices=["full", "append"], default="full", help="full = rewrite full index, append = append scan note only.")
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser()
    output = Path(args.output).expanduser()
    if not root.exists():
        print(f"ERROR: root does not exist: {root}")
        return 1
    try:
        records = build_records(root)
        if args.mode == "full":
            write_full_report(output, root, records)
        else:
            append_scan_note(output, root, records)
        print_summary(records)
        print("")
        print(f"Wrote: {output}")
        return 0
    except KeyboardInterrupt:
        print("Aborted.")
        return 130
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
