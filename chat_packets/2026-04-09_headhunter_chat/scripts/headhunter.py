#!/usr/bin/env python3
# =============================================================================
# ULTRAMODE HEADER — RECOGNITION ZONE (KEEP NEAR TOP)
# FILENAME: headhunter_v1_0_r1_2026-04-09.py
# FOLDER PATH: /userdata/system/ultramode/modules/tools/headhunter/
# DESTINATION: /userdata/system/ultramode/modules/tools/headhunter/headhunter.py
# PATCH TYPE: FULL
# VERSION: 1.0
# REVISION: 1
# DATE: 2026-04-09
# TIME: 01:31 PM
# AUTHOR: OpenAI ChatGPT
# SOURCE FILE: UNKNOWN
# STATUS_STAGING: [SEED_BUILD]
# SCRIPT_ROLE: HEADER_TRUTH_REPAIR_ROUTING_ENGINE
# TRUST_CLASS: REVIEW_INTENT
# HEADER_HEALTH: ORANGE
# SIDECAR_PATH: UNKNOWN
# THINKTANK_PATH: UNKNOWN
# LOG_PATH: UNKNOWN
# SUMMARY: Scans UltraMode files for header truth, drift, markers, notation backup
#   identity, trust class, header health, sidecar links, and repair suggestions.
# Hi Mom.
# =============================================================================
# ### ULTRAMODE PROTECTED START
# HeadHunter is report-first. Do not auto-rewrite files unless explicitly called.
# ### ULTRAMODE PROTECTED END
# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: PURPOSE
# TYPE: ACTIVE_TOOL_SEED
# SOURCE: Paul + ChatGPT
# STATUS: ACTIVE
# PURPOSE: Header truth engine for UMPatcher / Hammer / Shredder / Code Bank.
# =============================================================================

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Sequence

REQUIRED_FIELDS = [
    "FILENAME", "FOLDER PATH", "DESTINATION", "PATCH TYPE", "VERSION", "REVISION",
    "DATE", "TIME", "SUMMARY", "SOURCE FILE",
]

EXTENDED_FIELDS = [
    "PROGRAM_NAME", "AUTHOR", "PURPOSE", "STATUS_STAGING", "SCRIPT_ROLE", "TRUST_CLASS",
    "HEADER_HEALTH", "CONFIDENCE", "TARGET_LINE", "TARGET_SECTION", "MODULE_BUCKET",
    "MODULE_PATH", "MENU_PATH", "MENU_BUCKET", "UMP_REGISTER", "UMP_MANIFEST_ARG",
    "UMP_RETURN_TARGET", "SIDECAR_PATH", "THINKTANK_PATH", "LOG_PATH", "DIGEST_ROLE",
    "DIGEST_ACTION", "PRE_DIGEST_SOURCE", "POST_DIGEST_TARGET", "BANK_TARGET",
    "PACKET_TARGET", "ROOT_PATH", "PRE_STATE", "POST_STATE", "CREATED_AT", "UPDATED_AT",
    "LIVE_TARGET_EXISTS", "DIGEST_STAGE", "EOL_MARKER",
]

VALID_PATCH_TYPES = {
    "CREATE", "APPEND", "FULL", "REPLACE", "INSERT_BEFORE", "INSERT_AFTER",
    "DELETE", "REPLACE_SECTION", "CODE_HANDOFF", "APPEND_REFERENCE",
}

PROTECTED_MARKERS = ["### ULTRAMODE PROTECTED START", "### ULTRAMODE PROTECTED END"]
EOL_MARKER = "### EOL ###"

NOTATION_SIGNALS = [
    "ULTRAMODE NOTATION BLOCK", "CATEGORY:", "TYPE:", "SOURCE:", "STATUS:",
    "PURPOSE:", "B.O.D:", "EVOLUTION:", "IDEAS:", "GOALS:", "LESSONS:",
    "AI_THINKTANK:", "RELATIONSHIPS:", "NEXT_STEPS:", "YOUTUBE_STORY:", "USER_VISION:",
]

DANGER_PATTERNS = [
    r"\bos\.system\s*\(", r"\bsubprocess\.", r"\bshutil\.rmtree\s*\(",
    r"\bos\.remove\s*\(", r"\bos\.unlink\s*\(", r"\beval\s*\(", r"\bexec\s*\(",
]

TEXT_EXTENSIONS = {
    ".py", ".txt", ".md", ".rst", ".log", ".json", ".yaml", ".yml",
    ".ini", ".cfg", ".toml", ".sh", ".bat", ".ps1", ".csv",
}

@dataclass
class SyntaxResult:
    valid: bool
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    lineno: Optional[int] = None

@dataclass
class HeaderFieldResult:
    name: str
    present: bool
    value: Optional[str]
    truthful: Optional[bool]
    notes: list[str] = field(default_factory=list)

@dataclass
class MarkerResult:
    hi_mom_present: bool
    protected_start_present: bool
    protected_end_present: bool
    protected_balanced: bool
    eol_present: bool
    content_below_eol: bool

@dataclass
class NotationResult:
    notation_hits: list[str]
    notation_count: int
    backup_identity_strength: str

@dataclass
class RoleResult:
    likely_python: bool
    likely_fragment: bool
    likely_runtime_script: bool
    likely_sidecar_text: bool
    likely_chat_dump: bool
    likely_patch_packet: bool
    likely_gui_module: bool
    likely_digest_source: bool
    role_label: str

@dataclass
class PathTruthResult:
    actual_filename: str
    actual_folder: str
    extension: str
    destination_exists: Optional[bool]
    sidecar_exists: Optional[bool]
    thinktank_exists: Optional[bool]
    log_exists: Optional[bool]
    family_guess: str

@dataclass
class HeadHunterResult:
    source_path: str
    scan_stamp: str
    label: str
    route: str
    header_health: str
    trust_class: str
    confidence: int
    reasons: list[str]
    warnings: list[str]
    syntax: SyntaxResult
    required_fields: list[HeaderFieldResult]
    extended_fields_found: list[str]
    marker_result: MarkerResult
    notation_result: NotationResult
    role_result: RoleResult
    path_truth: PathTruthResult
    lamp_pack: dict
    suggested_repairs: list[str]
    tiny_packet: dict

def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")

def read_text_file(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return None

def extract_top_lines(text: str, count: int = 50) -> list[str]:
    return normalize_newlines(text).split("\n")[:count]

def infer_family(path: Path) -> str:
    normalized = str(path).replace("\\", "/")
    if "/modules/mandatory/" in normalized:
        return "mandatory_module"
    if "/modules/tools/" in normalized:
        return "tool_module"
    if "/modules/patcher/incoming/" in normalized:
        return "incoming_patch_candidate"
    if "/modules/patcher/" in normalized:
        return "patcher_module"
    if "/um_master_logs/" in normalized:
        return "master_log"
    return "unknown_family"

def safe_value_match(a: str | None, b: str | None) -> bool:
    if a is None or b is None:
        return False
    return a.strip() == b.strip()

def find_header_start_line(lines: list[str]) -> Optional[int]:
    for idx, line in enumerate(lines):
        if re.search(r"^\s*#\s*(FILENAME|PROGRAM_NAME|FOLDER PATH|DESTINATION|PATCH TYPE)\s*:", line):
            return idx + 1
    return None

def analyze_syntax(text: str, ext: str) -> SyntaxResult:
    if ext != ".py":
        return SyntaxResult(valid=True)
    try:
        ast.parse(text)
        return SyntaxResult(valid=True)
    except SyntaxError as exc:
        return SyntaxResult(valid=False, error_type=exc.__class__.__name__, error_message=str(exc), lineno=getattr(exc, "lineno", None))

def parse_header_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in extract_top_lines(text, 80):
        m = re.match(r"^\s*#\s*([A-Z0-9_ /.-]+?)\s*:\s*(.*?)\s*$", line)
        if m:
            fields[m.group(1).strip()] = m.group(2).strip()
    return fields

def analyze_markers(text: str) -> MarkerResult:
    hi_mom_present = "Hi Mom." in text
    protected_start_present = PROTECTED_MARKERS[0] in text
    protected_end_present = PROTECTED_MARKERS[1] in text
    protected_balanced = protected_start_present == protected_end_present
    eol_present = EOL_MARKER in text
    content_below_eol = False
    if eol_present:
        parts = text.split(EOL_MARKER, 1)
        if len(parts) == 2 and parts[1].strip():
            content_below_eol = True
    return MarkerResult(hi_mom_present=hi_mom_present, protected_start_present=protected_start_present, protected_end_present=protected_end_present, protected_balanced=protected_balanced, eol_present=eol_present, content_below_eol=content_below_eol)

def analyze_notation(text: str) -> NotationResult:
    hits = [sig for sig in NOTATION_SIGNALS if sig in text]
    count = len(hits)
    strength = "STRONG" if count >= 5 else ("MEDIUM" if count >= 2 else ("WEAK" if count >= 1 else "NONE"))
    return NotationResult(notation_hits=hits, notation_count=count, backup_identity_strength=strength)

def analyze_role(text: str, ext: str, path: Path) -> RoleResult:
    likely_python = False
    likely_fragment = False
    likely_runtime_script = False
    likely_sidecar_text = False
    likely_chat_dump = False
    likely_patch_packet = False
    likely_gui_module = False
    likely_digest_source = False
    role_label = "unknown"
    python_score = 8 if ext == ".py" else 0
    for token in ["#!/usr/bin/env python3", "import ", "from ", "def ", "class ", "if __name__ =="]:
        if token in text:
            python_score += 3
    likely_python = python_score >= 8
    if likely_python and "def " in text and "if __name__ ==" not in text and len(text.splitlines()) < 80:
        likely_fragment = True
    if likely_python and ("pygame" in text or "pygame." in text or "display.set_mode" in text):
        likely_gui_module = True
    lower = text.lower()
    if ext in {".txt", ".log", ".md"} and "ULTRAMODE NOTATION BLOCK" in text:
        likely_sidecar_text = True
    if "DIGEST_ROLE:" in text or "DIGEST_ACTION:" in text:
        likely_digest_source = True
    if "MATCH_ANCHOR_START:" in text or "PATCH_INTENT:" in text:
        likely_patch_packet = True
    if any(token in lower for token in ["chat dump", "conversation", "claude handoff", "packet", "ramblings"]):
        likely_chat_dump = True
    if likely_python and not likely_fragment and not likely_sidecar_text:
        likely_runtime_script = True
    if likely_sidecar_text:
        role_label = "sidecar_or_log"
    elif likely_patch_packet:
        role_label = "patch_packet"
    elif likely_chat_dump or likely_digest_source:
        role_label = "digest_source"
    elif likely_gui_module:
        role_label = "gui_module"
    elif likely_fragment:
        role_label = "python_fragment"
    elif likely_runtime_script:
        role_label = "runtime_script"
    elif ext == ".txt":
        role_label = "text_doc"
    return RoleResult(likely_python=likely_python, likely_fragment=likely_fragment, likely_runtime_script=likely_runtime_script, likely_sidecar_text=likely_sidecar_text, likely_chat_dump=likely_chat_dump, likely_patch_packet=likely_patch_packet, likely_gui_module=likely_gui_module, likely_digest_source=likely_digest_source, role_label=role_label)

def build_required_field_results(path: Path, header_fields: dict[str, str]) -> list[HeaderFieldResult]:
    actual_filename = path.name
    actual_folder = str(path.parent)
    results: list[HeaderFieldResult] = []
    for name in REQUIRED_FIELDS:
        value = header_fields.get(name)
        present = value is not None and value != ""
        truthful: Optional[bool] = None
        notes: list[str] = []
        if name == "FILENAME" and present:
            truthful = safe_value_match(value, actual_filename)
            if not truthful:
                notes.append(f"actual filename is {actual_filename}")
        elif name == "FOLDER PATH" and present:
            truthful = safe_value_match(value, actual_folder)
            if not truthful:
                notes.append(f"actual folder is {actual_folder}")
        elif name == "PATCH TYPE" and present:
            truthful = value in VALID_PATCH_TYPES
            if not truthful:
                notes.append("patch type not in approved list")
        elif name in {"DATE", "TIME", "SUMMARY", "SOURCE FILE", "DESTINATION", "VERSION", "REVISION"} and present:
            truthful = True
        elif not present:
            truthful = False
            notes.append("missing required field")
        results.append(HeaderFieldResult(name=name, present=present, value=value, truthful=truthful, notes=notes))
    return results

def build_path_truth(path: Path, header_fields: dict[str, str]) -> PathTruthResult:
    dest = header_fields.get("DESTINATION")
    sidecar = header_fields.get("SIDECAR_PATH")
    thinktank = header_fields.get("THINKTANK_PATH")
    log_path = header_fields.get("LOG_PATH")
    def exists_or_none(value: Optional[str]) -> Optional[bool]:
        if not value or value == "UNKNOWN":
            return None
        return Path(value).exists()
    return PathTruthResult(actual_filename=path.name, actual_folder=str(path.parent), extension=path.suffix.lower(), destination_exists=exists_or_none(dest), sidecar_exists=exists_or_none(sidecar), thinktank_exists=exists_or_none(thinktank), log_exists=exists_or_none(log_path), family_guess=infer_family(path))

def analyze_header_drift(text: str, ext: str, reasons: list[str], warnings: list[str]) -> None:
    lines = normalize_newlines(text).split("\n")
    shebang_ok = bool(lines and lines[0].strip() == "#!/usr/bin/env python3")
    header_start = find_header_start_line(lines)
    if ext == ".py" and not shebang_ok:
        reasons.append("Missing Python shebang on line 1.")
        warnings.append("SHEBANG_MISSING")
    if header_start is None:
        reasons.append("No recognizable header fields found in scan range.")
        warnings.append("NO_HEADER_FOUND")
        return
    if header_start > 50:
        reasons.append("Header drifted below top 50 lines.")
        warnings.append("HEADER_DRIFT_HARD_FAIL")
    elif header_start > 20:
        reasons.append("Header drifted below preferred top recognition zone.")
        warnings.append("HEADER_DRIFT")

def detect_danger(text: str) -> list[str]:
    hits = []
    for pattern in DANGER_PATTERNS:
        if re.search(pattern, text):
            hits.append(pattern)
    return hits

def assign_health_and_trust(ext: str, required_results: list[HeaderFieldResult], markers: MarkerResult, notation: NotationResult, role: RoleResult, syntax: SyntaxResult, warnings: list[str]) -> tuple[str, str, str, str, int]:
    missing_required = sum(1 for r in required_results if not r.present)
    bad_required = sum(1 for r in required_results if r.present and r.truthful is False)
    header_health, trust_class, label, route, confidence = "ORANGE", "REVIEW_INTENT", "REVIEW_REQUIRED", "review_queue", 70
    if ext == ".py" and not syntax.valid:
        return "RED", "UNTRUSTED_PYTHON", "BROKEN_SYNTAX", "syntax_repair", 90
    if role.likely_sidecar_text:
        return "BLUE", ("PATCHER_CAPABLE_TXT" if notation.notation_count >= 2 else "NON_CODE"), "SIDECAR_TEXT", "save_or_review", 80
    if "HEADER_DRIFT_HARD_FAIL" in warnings:
        return "RED", "REVIEW_INTENT", "HEADER_DRIFT", "header_repair", 92
    if missing_required == 0 and bad_required == 0 and markers.hi_mom_present and markers.protected_balanced and markers.eol_present:
        return "GREEN", ("VALID_PATCH" if role.likely_python else "PYTHON_WITH_NOTATION"), "HEADER_OK", "allow_review", 91
    if missing_required >= 3 or not markers.eol_present or not markers.protected_balanced:
        return "RED", ("REVIEW_INTENT" if role.likely_python else "NON_CODE"), "HEADER_BROKEN", "header_repair", 88
    if role.likely_fragment:
        return "ORANGE", "UNTRUSTED_PYTHON", "PYTHON_FRAGMENT", "wrap_or_review", 84
    return header_health, trust_class, label, route, confidence

def build_lamp_pack(header_health: str, markers: MarkerResult, required_results: list[HeaderFieldResult], path_truth: PathTruthResult, syntax: SyntaxResult) -> dict:
    required_missing = sum(1 for r in required_results if not r.present)
    syntax_lamp = "GREEN" if syntax.valid else "RED"
    marker_lamp = "GREEN" if markers.hi_mom_present and markers.protected_balanced and markers.eol_present else "RED"
    destination_lamp = "BLUE"
    if path_truth.destination_exists is True:
        destination_lamp = "GREEN"
    elif path_truth.destination_exists is False:
        destination_lamp = "ORANGE"
    required_lamp = "GREEN" if required_missing == 0 else ("ORANGE" if required_missing <= 2 else "RED")
    return {
        "primary": header_health,
        "syntax": syntax_lamp,
        "markers": marker_lamp,
        "required": required_lamp,
        "destination": destination_lamp,
        "sidecar": "GREEN" if path_truth.sidecar_exists else ("BLUE" if path_truth.sidecar_exists is None else "ORANGE"),
        "thinktank": "GREEN" if path_truth.thinktank_exists else ("BLUE" if path_truth.thinktank_exists is None else "ORANGE"),
        "log": "GREEN" if path_truth.log_exists else ("BLUE" if path_truth.log_exists is None else "ORANGE"),
    }

def build_suggested_repairs(path: Path, ext: str, required_results: list[HeaderFieldResult], markers: MarkerResult, warnings: list[str], path_truth: PathTruthResult) -> list[str]:
    repairs: list[str] = []
    if ext == ".py":
        repairs.append("Ensure line 1 is exactly '#!/usr/bin/env python3'.")
    if "NO_HEADER_FOUND" in warnings:
        repairs.append("Insert a scan-safe header near the top recognition zone.")
    if "HEADER_DRIFT" in warnings or "HEADER_DRIFT_HARD_FAIL" in warnings:
        repairs.append("Move the header back into the top recognition zone.")
    for result in required_results:
        if not result.present:
            repairs.append(f"Add missing required field: {result.name}: UNKNOWN")
        elif result.truthful is False:
            repairs.append(f"Correct field '{result.name}' to match actual file facts.")
    if not markers.hi_mom_present:
        repairs.append("Preserve or restore 'Hi Mom.' near the protected/header area.")
    if not markers.protected_start_present:
        repairs.append("Restore '### ULTRAMODE PROTECTED START'.")
    if not markers.protected_end_present:
        repairs.append("Restore '### ULTRAMODE PROTECTED END'.")
    if not markers.eol_present:
        repairs.append("Add '### EOL ###' at end of file.")
    if markers.content_below_eol:
        repairs.append("Review content below EOL marker; keep only if clearly intended.")
    if path_truth.destination_exists is False:
        repairs.append("Review DESTINATION path because target does not currently exist.")
    return list(dict.fromkeys(repairs))

def emit_repair_template(path: Path, header_fields: dict[str, str]) -> str:
    now = datetime.now()
    filename = path.name
    folder = str(path.parent)
    destination = header_fields.get("DESTINATION", str(path))
    summary = header_fields.get("SUMMARY", "UNKNOWN")
    source_file = header_fields.get("SOURCE FILE", "UNKNOWN")
    lines = [
        "#!/usr/bin/env python3" if path.suffix.lower() == ".py" else "",
        "# =============================================================================",
        f"# FILENAME: {filename}",
        f"# FOLDER PATH: {folder}",
        f"# DESTINATION: {destination}",
        f"# PATCH TYPE: {header_fields.get('PATCH TYPE', 'UNKNOWN')}",
        f"# VERSION: {header_fields.get('VERSION', 'UNKNOWN')}",
        f"# REVISION: {header_fields.get('REVISION', 'UNKNOWN')}",
        f"# DATE: {now.strftime('%Y-%m-%d')}",
        f"# TIME: {now.strftime('%I:%M %p')}",
        f"# SOURCE FILE: {source_file}",
        f"# SUMMARY: {summary}",
        "# Hi Mom.",
        "# =============================================================================",
    ]
    return "\n".join(line for line in lines if line != "") + "\n"

def analyze_file(path: Path) -> HeadHunterResult | None:
    text = read_text_file(path)
    if text is None:
        return None
    text = normalize_newlines(text)
    ext = path.suffix.lower()
    header_fields = parse_header_fields(text)
    syntax = analyze_syntax(text, ext)
    markers = analyze_markers(text)
    notation = analyze_notation(text)
    role = analyze_role(text, ext, path)
    path_truth = build_path_truth(path, header_fields)
    required_results = build_required_field_results(path, header_fields)
    reasons: list[str] = []
    warnings: list[str] = []
    analyze_header_drift(text, ext, reasons, warnings)
    if not markers.hi_mom_present:
        warnings.append("HI_MOM_MISSING")
        reasons.append("Hi Mom. marker missing.")
    if not markers.protected_balanced:
        warnings.append("PROTECTED_MARKERS_BROKEN")
        reasons.append("Protected markers are missing or unbalanced.")
    if not markers.eol_present:
        warnings.append("EOL_MISSING")
        reasons.append("EOL marker missing.")
    if markers.content_below_eol:
        warnings.append("CONTENT_BELOW_EOL")
        reasons.append("Content exists below EOL marker.")
    if syntax.error_message:
        reasons.append(f"Syntax error: {syntax.error_message}")
    danger_hits = detect_danger(text)
    if danger_hits:
        warnings.append("DANGER_PATTERNS_PRESENT")
        reasons.append("Potentially dangerous operations detected.")
    missing_required = [r.name for r in required_results if not r.present]
    if missing_required:
        reasons.append("Missing required fields: " + ", ".join(missing_required))
    bad_required = [r.name for r in required_results if r.present and r.truthful is False]
    if bad_required:
        reasons.append("Field truth mismatch: " + ", ".join(bad_required))
    header_health, trust_class, label, route, confidence = assign_health_and_trust(ext=ext, required_results=required_results, markers=markers, notation=notation, role=role, syntax=syntax, warnings=warnings)
    extended_found = [k for k in EXTENDED_FIELDS if k in header_fields]
    suggested_repairs = build_suggested_repairs(path=path, ext=ext, required_results=required_results, markers=markers, warnings=warnings, path_truth=path_truth)
    lamp_pack = build_lamp_pack(header_health=header_health, markers=markers, required_results=required_results, path_truth=path_truth, syntax=syntax)
    tiny_packet = {
        "source_path": str(path),
        "label": label,
        "route": route,
        "header_health": header_health,
        "trust_class": trust_class,
        "confidence": confidence,
        "role": role.role_label,
        "primary_lamp": lamp_pack["primary"],
        "warnings": warnings[:5],
        "first_reason": reasons[0] if reasons else "No major issue detected.",
    }
    return HeadHunterResult(source_path=str(path), scan_stamp=now_stamp(), label=label, route=route, header_health=header_health, trust_class=trust_class, confidence=confidence, reasons=reasons, warnings=warnings, syntax=syntax, required_fields=required_results, extended_fields_found=extended_found, marker_result=markers, notation_result=notation, role_result=role, path_truth=path_truth, lamp_pack=lamp_pack, suggested_repairs=suggested_repairs, tiny_packet=tiny_packet)

def format_human_report(result: HeadHunterResult) -> str:
    lines: list[str] = []
    lines.append("=" * 79)
    lines.append("ULTRAMODE HEADHUNTER REPORT")
    lines.append("=" * 79)
    lines.append(f"SOURCE:         {result.source_path}")
    lines.append(f"STAMP:          {result.scan_stamp}")
    lines.append(f"LABEL:          {result.label}")
    lines.append(f"ROUTE:          {result.route}")
    lines.append(f"HEADER_HEALTH:  {result.header_health}")
    lines.append(f"TRUST_CLASS:    {result.trust_class}")
    lines.append(f"CONFIDENCE:     {result.confidence}")
    lines.append(f"ROLE:           {result.role_result.role_label}")
    lines.append(f"FAMILY_GUESS:   {result.path_truth.family_guess}")
    lines.append("")
    lines.append("[LAMPS]")
    for key, value in result.lamp_pack.items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("[REASONS]")
    for item in result.reasons or ["none"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("[WARNINGS]")
    for item in result.warnings or ["none"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("[REQUIRED_FIELDS]")
    for item in result.required_fields:
        lines.append(f"- {item.name}: present={item.present} truthful={item.truthful} value={item.value}")
        for note in item.notes:
            lines.append(f"  note: {note}")
    lines.append("")
    lines.append("[MARKERS]")
    m = result.marker_result
    lines.append(f"- hi_mom_present: {m.hi_mom_present}")
    lines.append(f"- protected_start_present: {m.protected_start_present}")
    lines.append(f"- protected_end_present: {m.protected_end_present}")
    lines.append(f"- protected_balanced: {m.protected_balanced}")
    lines.append(f"- eol_present: {m.eol_present}")
    lines.append(f"- content_below_eol: {m.content_below_eol}")
    lines.append("")
    lines.append("[NOTATION]")
    n = result.notation_result
    lines.append(f"- notation_count: {n.notation_count}")
    lines.append(f"- backup_identity_strength: {n.backup_identity_strength}")
    lines.append(f"- notation_hits: {', '.join(n.notation_hits) if n.notation_hits else 'none'}")
    lines.append("")
    lines.append("[PATH_TRUTH]")
    p = result.path_truth
    lines.append(f"- actual_filename: {p.actual_filename}")
    lines.append(f"- actual_folder: {p.actual_folder}")
    lines.append(f"- extension: {p.extension}")
    lines.append(f"- destination_exists: {p.destination_exists}")
    lines.append(f"- sidecar_exists: {p.sidecar_exists}")
    lines.append(f"- thinktank_exists: {p.thinktank_exists}")
    lines.append(f"- log_exists: {p.log_exists}")
    lines.append("")
    lines.append("[SUGGESTED_REPAIRS]")
    for item in result.suggested_repairs or ["none"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("### EOL ###")
    return "\n".join(lines)

def iter_candidate_files(root: Path):
    for current_root, _, filenames in os.walk(root):
        for filename in filenames:
            path = Path(current_root) / filename
            if path.suffix.lower() in TEXT_EXTENSIONS or path.suffix == "":
                yield path

def scan_tree(root: Path) -> list[HeadHunterResult]:
    results: list[HeadHunterResult] = []
    for path in iter_candidate_files(root):
        result = analyze_file(path)
        if result is not None:
            results.append(result)
    return results

def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="UltraMode header truth / repair / routing scanner.")
    parser.add_argument("target", help="File or folder to analyze.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of human report.")
    parser.add_argument("--tiny", action="store_true", help="Print tiny packet only.")
    parser.add_argument("--emit-repair-template", action="store_true", help="Print suggested repair header template.")
    return parser.parse_args(argv)

def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        print(f"ERROR: target not found: {target}", file=sys.stderr)
        return 2
    if target.is_file():
        result = analyze_file(target)
        if result is None:
            print(f"ERROR: unable to read file: {target}", file=sys.stderr)
            return 3
        if args.emit_repair_template:
            text = read_text_file(target)
            header_fields = parse_header_fields(text or "")
            print(emit_repair_template(target, header_fields))
            return 0
        if args.tiny:
            print(json.dumps(result.tiny_packet, indent=2))
            return 0
        if args.json:
            print(json.dumps(asdict(result), indent=2))
            return 0
        print(format_human_report(result))
        return 0
    results = scan_tree(target)
    payload = [asdict(r) for r in results]
    if args.tiny:
        print(json.dumps([r["tiny_packet"] for r in payload], indent=2))
    elif args.json:
        print(json.dumps(payload, indent=2))
    else:
        for idx, result in enumerate(results):
            if idx:
                print()
            print(format_human_report(result))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: CHANGELOG
# TYPE: APPEND_ONLY
# SOURCE: ChatGPT
# STATUS: ACTIVE
# =============================================================================
# 2026-04-09 13:31 | ChatGPT | v1.0 r1 | Initial seed build for HeadHunter.
# Added top-zone header scan, required field checks, drift detection, marker
# checks, notation backup identity scan, role guess, lamp packet, and repair
# suggestion output.
# =============================================================================
# ### EOL ###
