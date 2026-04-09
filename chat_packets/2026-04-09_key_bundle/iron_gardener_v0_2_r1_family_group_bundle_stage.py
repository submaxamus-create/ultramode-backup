#!/usr/bin/env python3
# =============================================================================
# FILENAME:      iron_gardener_v0_2_r1_family_group_bundle_stage.py
# PROGRAM_NAME:  Iron Gardener
# FOLDER PATH:   /userdata/system/ultramode/modules/tools/iron_gardener/
# DESTINATION:   /userdata/system/ultramode/modules/tools/iron_gardener/iron_gardener.py
# VERSION:       v0.2
# REVISION:      r1
# SUMMARY:       Family grouping + smart bundle staging pass for Ultramode tree.
# DATE:          2026-04-07 02:16
# AUTHOR:        ChatGPT + Paul
# Hi Mom.
# =============================================================================

from __future__ import annotations
import argparse
import json
import os
import re
import hashlib
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

ROOT_DEFAULT = Path("/userdata/system/ultramode")
OUT_ROOT = ROOT_DEFAULT / "modules" / "tools" / "iron_gardener"
REPORT_ROOT = OUT_ROOT / "reports"
STAGE_ROOT = OUT_ROOT / "staging"
LOG_PATH = OUT_ROOT / "iron_gardener_log.txt"

KEEP = "KEEP"
REVIEW = "REVIEW"
ARCHIVE = "ARCHIVE"
LOST_INTELLIGENCE = "LOST_INTELLIGENCE"
TROUBLE = "TROUBLE"
DUPLICATE = "DUPLICATE"

TEXTISH = {
    ".py",".txt",".log",".md",".json",".cfg",".ini",".yaml",".yml",".sh",
    ".html",".htm",".mhtml",".svg",".css",".js",".sc"
}
IGNORE_DIRS = {"__pycache__", ".git", ".venv", "node_modules"}
BUNDLE_EXTS = {".py",".txt",".log",".md",".sc",".json"}

@dataclass
class Record:
    path: str
    name: str
    ext: str
    size: int
    mtime: str
    family: str
    stage: str
    reasons: List[str] = field(default_factory=list)
    duplicate_of: Optional[str] = None
    bundle_hint: bool = False

@dataclass
class FamilyGroup:
    family: str
    branch: str
    count: int = 0
    newest: str = ""
    stages: Dict[str, int] = field(default_factory=dict)
    files: List[str] = field(default_factory=list)

def ensure_dirs() -> None:
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    STAGE_ROOT.mkdir(parents=True, exist_ok=True)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

def log(msg: str) -> None:
    ensure_dirs()
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] | [IRON_GARDENER] | {msg}"
    print(line)
    try:
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def read_text(path: Path, limit: int = 200_000) -> str:
    try:
        data = path.read_bytes()[:limit]
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""

def sha256(path: Path) -> str:
    try:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""

def infer_family(path: Path) -> str:
    n = path.name.lower()
    if n.startswith("directory_list_"):
        return "directory_list"
    if n.startswith("um.py") or n.startswith("um_") or n == "um_fixed.py":
        return "um"
    if "umpatcher" in n:
        return "umpatcher"
    if "thinktank" in n or "master_dump" in n or "rules" in n or "notation" in n:
        return "rules_thinktank"
    if "idea_extractor" in n:
        return "idea_extractor"
    if "game" in str(path).lower():
        return "game_assets"
    stem = path.stem.lower()
    stem = re.sub(r"_v\d+[\w\.-]*", "", stem)
    stem = re.sub(r"_r\d+[\w\.-]*", "", stem)
    stem = re.sub(r"\d{4}[-_]?\d{2}[-_]?\d{2}.*$", "", stem)
    return stem.strip("_- ") or "misc"

def infer_branch(path: Path) -> str:
    low = str(path).lower()
    if "! ai lost modules" in low:
        return "lost_modules"
    if "rules and good ideas" in low:
        return "rules_and_good_ideas"
    if "/game/" in low:
        return "game"
    if path.parent == ROOT_DEFAULT:
        return "root"
    if "/modules/" in low:
        return "modules"
    if "/backups/" in low:
        return "backups"
    if "/logs/" in low:
        return "logs"
    return "other"

def classify(path: Path, text: str):
    name = path.name.lower()
    ext = path.suffix.lower()
    if name in {"your", "unknown.py"} or ext == "":
        return TROUBLE, ["stray_or_no_extension"], False
    if name.startswith("directory_list_") and ext == ".txt":
        return ARCHIVE, ["directory_scan_spam"], False
    if ".bak" in name:
        return ARCHIVE, ["backup_variant"], False
    if "! ai lost modules" in str(path).lower():
        if ext == ".py":
            return LOST_INTELLIGENCE, ["lost_module_python"], True
        return REVIEW, ["lost_module_support"], False
    if any(k in name for k in ["thinktank", "master_dump", "master_rules", "master_help", "knowledge_transfer"]):
        return LOST_INTELLIGENCE, ["intelligence_candidate"], True
    if ext == ".py":
        if any(tok in text for tok in ["def ", "class ", "import ", "if __name__"]):
            return REVIEW, ["python_needs_family_review"], True
        return REVIEW, ["python_review"], True
    if ext in {".txt",".log",".md",".json",".sc"}:
        return REVIEW, ["support_review"], False
    return KEEP, ["asset_or_other"], False

def find_bundle(path: Path):
    base = path.stem.lower()
    out = []
    try:
        for c in sorted(path.parent.iterdir()):
            if c == path:
                continue
            if c.suffix.lower() in BUNDLE_EXTS:
                cn = c.name.lower()
                if base in cn or path.stem.lower().split("_")[0] in cn:
                    out.append(str(c))
    except Exception:
        pass
    return out[:20]

def scan(root: Path):
    records = []
    hashes = {}
    bundles = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for fname in filenames:
            p = Path(dirpath) / fname
            try:
                stat = p.stat()
                size = stat.st_size
                mtime = datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds")
            except Exception:
                continue
            text = read_text(p) if (p.suffix.lower() in TEXTISH or ".bak" in p.name.lower() or p.suffix == "") else ""
            family = infer_family(p)
            stage, reasons, bundle_hint = classify(p, text)
            digest = sha256(p) if size <= 5_000_000 else ""
            dup_of = None
            if digest:
                if digest in hashes:
                    dup_of = hashes[digest]
                    stage = DUPLICATE
                    reasons = reasons + ["exact_hash_duplicate"]
                else:
                    hashes[digest] = str(p)
            records.append(Record(
                path=str(p), name=p.name, ext=p.suffix or "[no_ext]", size=size,
                mtime=mtime, family=family, stage=stage, reasons=reasons,
                duplicate_of=dup_of, bundle_hint=bundle_hint
            ))
            if bundle_hint:
                companions = find_bundle(p)
                if companions:
                    bundles[str(p)] = companions
    return records, bundles

def group_families(records):
    grouped = {}
    for rec in records:
        key = (infer_family(Path(rec.path)), infer_branch(Path(rec.path)))
        grp = grouped.setdefault(key, FamilyGroup(family=key[0], branch=key[1]))
        grp.count += 1
        grp.files.append(rec.path)
        grp.stages[rec.stage] = grp.stages.get(rec.stage, 0) + 1
        if not grp.newest or rec.mtime > grp.newest:
            grp.newest = rec.mtime
    return sorted(grouped.values(), key=lambda g: (g.branch, g.family))

def build_outputs(records, bundles, groups):
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "root": str(ROOT_DEFAULT),
        "totals": {
            "records": len(records),
            "keep": sum(1 for r in records if r.stage == KEEP),
            "review": sum(1 for r in records if r.stage == REVIEW),
            "archive": sum(1 for r in records if r.stage == ARCHIVE),
            "lost_intelligence": sum(1 for r in records if r.stage == LOST_INTELLIGENCE),
            "trouble": sum(1 for r in records if r.stage == TROUBLE),
            "duplicate": sum(1 for r in records if r.stage == DUPLICATE),
            "bundle_candidates": len(bundles),
        },
        "first_priority_branches": [
            "lost_modules",
            "root:directory_list",
            "root:um",
            "rules_and_good_ideas",
        ],
        "bundles": bundles,
        "groups": [asdict(g) for g in groups],
    }

def write_outputs(records, report):
    ensure_dirs()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    rec_path = REPORT_ROOT / f"iron_gardener_v2_records_{stamp}.json"
    rep_path = REPORT_ROOT / f"iron_gardener_v2_grouped_report_{stamp}.json"
    rec_path.write_text(json.dumps([asdict(r) for r in records], indent=2), encoding="utf-8")
    rep_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return rec_path, rep_path

def write_stage_lists(report):
    ensure_dirs()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stage_dir = STAGE_ROOT / f"v2_stage_{stamp}"
    stage_dir.mkdir(parents=True, exist_ok=True)
    by_branch = {}
    for g in report["groups"]:
        by_branch[f"{g['branch']}::{g['family']}"] = g["files"]
    (stage_dir / "bundle_manifest.json").write_text(json.dumps(report["bundles"], indent=2), encoding="utf-8")
    (stage_dir / "group_stage_manifest.json").write_text(json.dumps(by_branch, indent=2), encoding="utf-8")
    return stage_dir

def console(report, rec_path, rep_path, stage_dir):
    print("\n" + "=" * 79)
    print("IRON GARDENER V2 — FAMILY GROUP + BUNDLE STAGE PASS")
    print("=" * 79)
    for k, v in report["totals"].items():
        print(f"{k.upper():22} {v}")
    print("-" * 79)
    print(f"RECORDS: {rec_path}")
    print(f"GROUPED REPORT: {rep_path}")
    print(f"STAGE DIR: {stage_dir}")
    print("-" * 79)
    print("FIRST PRIORITY BRANCHES:")
    for item in report["first_priority_branches"]:
        print(f"  - {item}")
    print("-" * 79)
    print("TOP FAMILY GROUPS:")
    for g in report["groups"][:12]:
        print(f"  - {g['branch']} | {g['family']} | count={g['count']} | stages={g['stages']}")
    print("=" * 79)

def main():
    parser = argparse.ArgumentParser(description="Iron Gardener v2 family group + bundle stage pass.")
    parser.add_argument("--root", default=str(ROOT_DEFAULT))
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.exists():
        log(f"ERROR | missing root={root}")
        return 2
    log(f"START_V2 | root={root}")
    records, bundles = scan(root)
    groups = group_families(records)
    report = build_outputs(records, bundles, groups)
    rec_path, rep_path = write_outputs(records, report)
    stage_dir = write_stage_lists(report)
    console(report, rec_path, rep_path, stage_dir)
    log(f"COMPLETE_V2 | records={len(records)} | groups={len(groups)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
