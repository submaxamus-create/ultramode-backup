#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
####################################################################################################
# ULTRAMODE / UMPATCHER PRE-FLIGHT CODE RECOGNIZER + LABELER
####################################################################################################
# FILENAME: umpatcher_code_labeler_v1_0_r1_2026-04-08.py
# DESTINATION: /userdata/system/ultramode/modules/patcher/umpatcher_code_labeler.py
# PATCH TYPE: NEW_FILE
# VERSION: 1.0
# REVISION: r1
# SUMMARY: Detects likely Python/code/text content, checks header/notation quality, labels trust/state,
#          and returns routing suggestions for UMPatcher before apply/write.
####################################################################################################
"""

from __future__ import annotations

import ast
import json
import os
import re
import sys
from dataclasses import dataclass, asdict, field

HEADER_FIELDS_REQUIRED = [
    "FILENAME",
    "DESTINATION",
    "PATCH TYPE",
    "VERSION",
    "REVISION",
    "SUMMARY",
]

HEADER_FIELDS_OPTIONAL = ["FOLDER PATH", "TARGET_LINE"]

NOTATION_HINTS = [
    "CHANGELOG", "THINKTANK", "AI THINK TANK", "GOALS", "IDEAS",
    "LESSONS", "RULES", "USAGE", "NOTES", "ANALYSIS",
]

PROTECTED_MARKERS = [
    "### ULTRAMODE PROTECTED START",
    "### ULTRAMODE PROTECTED END",
    "Hi Mom.",
]

PYTHON_STRONG_HINTS = [
    "#!/usr/bin/env python3", "import ", "from ", "def ", "class ",
    "if __name__ ==", "try:", "except ", "return ",
]

PYTHON_MEDIUM_HINTS = [
    "lambda ", "with ", "for ", "while ", "elif ", "self.",
    "__init__", "raise ", "pass", "yield ",
]

DANGER_PATTERNS = [
    r"\bos\.system\s*\(",
    r"\bsubprocess\.",
    r"\bshutil\.rmtree\s*\(",
    r"\bos\.remove\s*\(",
    r"\bos\.unlink\s*\(",
    r"\bos\.rename\s*\(",
    r"\bos\.replace\s*\(",
    r"\bPath\s*\(.*\)\.unlink\s*\(",
    r"\beval\s*\(",
    r"\bexec\s*\(",
]

TEXT_SIDEcar_HINTS = [
    "ticket", "changelog", "thinktank", "notes", "summary", "todo",
    "rule", "idea", "analysis", "report", "log",
]

@dataclass
class SyntaxResult:
    valid: bool
    error_type: str | None = None
    error_message: str | None = None
    lineno: int | None = None
    offset: int | None = None

@dataclass
class HeaderResult:
    found_any_header: bool
    required_found: list[str] = field(default_factory=list)
    required_missing: list[str] = field(default_factory=list)
    optional_found: list[str] = field(default_factory=list)
    recognition_zone_ok: bool = False
    protected_markers_found: list[str] = field(default_factory=list)
    protected_markers_missing: list[str] = field(default_factory=list)
    has_destination_value: bool = False
    destination_value: str | None = None

@dataclass
class NotationResult:
    notation_hits: list[str] = field(default_factory=list)
    notation_count: int = 0
    likely_sidecar_or_doc: bool = False

@dataclass
class CodeShapeResult:
    line_count: int
    nonempty_line_count: int
    comment_line_count: int
    import_count: int
    def_count: int
    class_count: int
    indented_line_count: int
    assignment_count: int
    likely_fragment: bool = False
    likely_full_script: bool = False
    likely_python: bool = False
    python_score: int = 0

@dataclass
class SafetyResult:
    danger_hits: list[str] = field(default_factory=list)
    warning_hits: list[str] = field(default_factory=list)
    danger_score: int = 0

@dataclass
class ClassificationResult:
    label: str
    color: str
    confidence: int
    route: str
    suggested_action: str
    summary: str
    reasons: list[str]
    warnings: list[str]
    source_name: str
    extension: str | None
    syntax: SyntaxResult
    header: HeaderResult
    notation: NotationResult
    code_shape: CodeShapeResult
    safety: SafetyResult

def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")

def safe_split_lines(text: str) -> list[str]:
    return normalize_newlines(text).split("\n")

def extract_top_zone(text: str, max_lines: int = 40) -> str:
    lines = safe_split_lines(text)
    return "\n".join(lines[:max_lines])

def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))

def count_regex(pattern: str, text: str, flags: int = 0) -> int:
    return len(re.findall(pattern, text, flags))

def analyze_syntax(text: str) -> SyntaxResult:
    try:
        ast.parse(text)
        return SyntaxResult(valid=True)
    except SyntaxError as exc:
        return SyntaxResult(valid=False, error_type=exc.__class__.__name__, error_message=str(exc), lineno=getattr(exc, "lineno", None), offset=getattr(exc, "offset", None))
    except Exception as exc:
        return SyntaxResult(valid=False, error_type=exc.__class__.__name__, error_message=str(exc))

def analyze_header(text: str) -> HeaderResult:
    top_zone = extract_top_zone(text, max_lines=50)
    lines = safe_split_lines(top_zone)
    required_found, required_missing, optional_found = [], [], []
    protected_found, protected_missing = [], []
    destination_value = None
    found_any_header = False
    for field_name in HEADER_FIELDS_REQUIRED:
        pattern = rf"^\s*#\s*{re.escape(field_name)}\s*:\s*(.+?)\s*$"
        m = re.search(pattern, top_zone, re.MULTILINE)
        if m:
            required_found.append(field_name)
            found_any_header = True
            if field_name == "DESTINATION":
                destination_value = m.group(1).strip()
        else:
            required_missing.append(field_name)
    for field_name in HEADER_FIELDS_OPTIONAL:
        pattern = rf"^\s*#\s*{re.escape(field_name)}\s*:\s*(.+?)\s*$"
        if re.search(pattern, top_zone, re.MULTILINE):
            optional_found.append(field_name)
            found_any_header = True
    for marker in PROTECTED_MARKERS:
        if marker in top_zone or marker in text:
            protected_found.append(marker)
        else:
            protected_missing.append(marker)
    recognition_zone_ok = False
    if found_any_header:
        hit_lines = 0
        for line in lines[:20]:
            if re.search(r"#\s*(FILENAME|DESTINATION|PATCH TYPE|VERSION|REVISION|SUMMARY)\s*:", line):
                hit_lines += 1
        recognition_zone_ok = hit_lines >= 3
    has_destination_value = bool(destination_value and destination_value.strip() and destination_value.strip() != "?")
    return HeaderResult(found_any_header=found_any_header, required_found=required_found, required_missing=required_missing, optional_found=optional_found, recognition_zone_ok=recognition_zone_ok, protected_markers_found=protected_found, protected_markers_missing=protected_missing, has_destination_value=has_destination_value, destination_value=destination_value)

def analyze_notation(text: str) -> NotationResult:
    upper_text = text.upper()
    notation_hits = [hint for hint in NOTATION_HINTS if hint in upper_text]
    lower_text = text.lower()
    likely_sidecar_or_doc = False
    if len(notation_hits) >= 2 and ("def " not in text and "class " not in text and "import " not in text):
        likely_sidecar_or_doc = True
    elif sum(1 for w in TEXT_SIDEcar_HINTS if w in lower_text) >= 4 and "def " not in text:
        likely_sidecar_or_doc = True
    return NotationResult(notation_hits=notation_hits, notation_count=len(notation_hits), likely_sidecar_or_doc=likely_sidecar_or_doc)

def analyze_code_shape(text: str) -> CodeShapeResult:
    lines = safe_split_lines(text)
    nonempty_lines = [ln for ln in lines if ln.strip()]
    comment_line_count = sum(1 for ln in lines if ln.strip().startswith("#"))
    import_count = count_regex(r"^\s*(import\s+\w+|from\s+\w+)", text, re.MULTILINE)
    def_count = count_regex(r"^\s*def\s+\w+\s*\(", text, re.MULTILINE)
    class_count = count_regex(r"^\s*class\s+\w+", text, re.MULTILINE)
    indented_line_count = sum(1 for ln in lines if ln.startswith((" ", "\t")) and ln.strip())
    assignment_count = count_regex(r"^\s*[A-Za-z_]\w*\s*=\s*.+", text, re.MULTILINE)
    python_score = 0
    for hint in PYTHON_STRONG_HINTS:
        if hint in text:
            python_score += 10
    for hint in PYTHON_MEDIUM_HINTS:
        if hint in text:
            python_score += 4
    if import_count:
        python_score += min(import_count * 2, 10)
    if def_count:
        python_score += min(def_count * 4, 16)
    if class_count:
        python_score += min(class_count * 6, 12)
    if indented_line_count >= 3:
        python_score += 8
    if assignment_count >= 2:
        python_score += 4
    if re.search(r":\s*$", text, re.MULTILINE):
        python_score += 4
    if re.search(r"^\s*#\!\/usr\/bin\/env python3", text, re.MULTILINE):
        python_score += 15
    likely_python = python_score >= 18
    likely_fragment = False
    likely_full_script = False
    if likely_python:
        has_full_script_signals = import_count > 0 or "if __name__ ==" in text or def_count >= 2 or class_count >= 1
        if has_full_script_signals and len(nonempty_lines) >= 12:
            likely_full_script = True
        if not likely_full_script:
            if def_count == 1 and import_count == 0 and len(nonempty_lines) < 20:
                likely_fragment = True
            elif re.search(r"^\s*(def|class)\s+\w+", text, re.MULTILINE) and not re.search(r"if __name__ ==", text):
                likely_fragment = True
    return CodeShapeResult(line_count=len(lines), nonempty_line_count=len(nonempty_lines), comment_line_count=comment_line_count, import_count=import_count, def_count=def_count, class_count=class_count, indented_line_count=indented_line_count, assignment_count=assignment_count, likely_fragment=likely_fragment, likely_full_script=likely_full_script, likely_python=likely_python, python_score=python_score)

def analyze_safety(text: str) -> SafetyResult:
    danger_hits, warning_hits = [], []
    danger_score = 0
    for pattern in DANGER_PATTERNS:
        if re.search(pattern, text):
            danger_hits.append(pattern)
            danger_score += 10
    if "chmod" in text or "chown" in text:
        warning_hits.append("filesystem_permission_change")
        danger_score += 4
    if "/userdata/" in text:
        warning_hits.append("writes_or_targets_userdata_path")
    if re.search(r"\b(open|Path)\s*\(", text) and re.search(r"\b(w|a|wb|ab)\b", text):
        warning_hits.append("possible_file_write_behavior")
    return SafetyResult(danger_hits=danger_hits, warning_hits=warning_hits, danger_score=danger_score)

def infer_extension(source_name: str) -> str | None:
    _, ext = os.path.splitext(source_name)
    return ext.lower() if ext else None

def build_summary(label: str, reasons: list[str]) -> str:
    return f"{label}: {reasons[0]}" if reasons else label

def classify_content(text: str, source_name: str = "buffer.txt") -> dict:
    text = normalize_newlines(text)
    extension = infer_extension(source_name)
    syntax = analyze_syntax(text)
    header = analyze_header(text)
    notation = analyze_notation(text)
    code_shape = analyze_code_shape(text)
    safety = analyze_safety(text)
    reasons, warnings = [], []
    label, color, route, suggested_action, confidence = "REVIEW_REQUIRED", "ORANGE", "review_queue", "Review content manually before any write/apply.", 50
    is_mostly_blank = code_shape.nonempty_line_count == 0
    has_py_ext = extension == ".py"
    has_txt_ext = extension == ".txt"
    if is_mostly_blank:
        label, color, route, suggested_action, confidence = "EMPTY_CONTENT", "RED", "block", "Block apply. Content is empty.", 98
        reasons.append("Content is empty.")
    else:
        if notation.likely_sidecar_or_doc and not code_shape.likely_python:
            label, color, route, suggested_action, confidence = "SIDECAR_OR_TEXT_DOC", "BLUE", "save_as_text_or_sidecar", "Treat as sidecar/log/notation text, not runnable script.", 88
            reasons.append("Looks like notation/log/document text rather than runnable code.")
        if code_shape.likely_python and syntax.valid and header.found_any_header and len(header.required_missing) == 0 and header.has_destination_value and header.recognition_zone_ok:
            label, color, route, suggested_action, confidence = "VALID_PATCH_PY", "GREEN", "patch_review_ready", "Show review screen, then allow controlled patch/apply.", 92
            reasons.append("Python syntax is valid and required patch header fields are present.")
            if header.protected_markers_missing:
                warnings.append("Protected markers are missing or incomplete.")
                confidence -= 6
        elif code_shape.likely_python and syntax.valid:
            if not header.found_any_header:
                if code_shape.likely_fragment:
                    label, color, route, suggested_action, confidence = "PYTHON_FRAGMENT", "ORANGE", "fragment_repair_or_wrap", "Offer wrap-template or route to manual review as partial code.", 84
                    reasons.append("Valid Python detected, but content looks like a fragment/snippet.")
                else:
                    label, color, route, suggested_action, confidence = "UNTRUSTED_PYTHON", "ORANGE", "python_review_no_header", "Treat as Python, but do not apply as patch until header is repaired.", 85
                    reasons.append("Valid Python detected, but required UltraMode patch header is missing.")
            else:
                if header.required_missing:
                    label, color, route, suggested_action, confidence = "BROKEN_HEADER", "ORANGE", "header_repair", "Repair required header fields before patch/apply.", 82
                    reasons.append("Valid Python detected, but required header fields are missing: " + ", ".join(header.required_missing))
                elif not header.has_destination_value:
                    label, color, route, suggested_action, confidence = "MISSING_DESTINATION", "RED", "block_until_destination", "Block apply until DESTINATION is valid.", 93
                    reasons.append("Python is valid, but DESTINATION is missing or unusable.")
                else:
                    label, color, route, suggested_action, confidence = "REVIEW_REQUIRED", "ORANGE", "manual_review", "Python detected. Review header placement, markers, and route manually.", 70
                    reasons.append("Python is valid, but patch readiness is incomplete.")
        elif code_shape.likely_python and not syntax.valid:
            label, color, route, suggested_action, confidence = "BROKEN_SYNTAX", "RED", "syntax_repair", "Do not apply. Route to syntax repair / review.", 90
            reasons.append("Content strongly resembles Python, but syntax parsing failed.")
            if syntax.lineno:
                reasons.append(f"Syntax error near line {syntax.lineno}.")
        else:
            label, color, route, suggested_action, confidence = "TEXT_NOT_CODE", "RED", "save_as_text_or_block", "Treat as text or log. Do not apply as Python patch.", 86
            reasons.append("Content does not strongly resemble runnable Python.")
    if has_py_ext and label in {"TEXT_NOT_CODE", "SIDECAR_OR_TEXT_DOC"}:
        warnings.append("Filename says .py but content does not look like runnable Python.")
        confidence = min(99, confidence + 2)
    if has_txt_ext and label in {"VALID_PATCH_PY", "UNTRUSTED_PYTHON", "PYTHON_FRAGMENT", "BROKEN_SYNTAX"}:
        warnings.append("Filename says .txt but content appears to be Python or Python-like.")
    if header.found_any_header and header.protected_markers_missing:
        warnings.append("Protected markers incomplete: " + ", ".join(header.protected_markers_missing))
    if safety.danger_hits:
        warnings.append("Potentially dangerous operations detected.")
        if label == "VALID_PATCH_PY":
            label, color, route, suggested_action = "VALID_PATCH_PY_WITH_RISK", "ORANGE", "high_attention_review", "Require explicit high-risk confirmation before apply."
            reasons.append("Patch appears valid, but includes potentially dangerous operations.")
            confidence = max(70, confidence - 10)
        elif label not in {"TEXT_NOT_CODE", "SIDECAR_OR_TEXT_DOC", "EMPTY_CONTENT"}:
            reasons.append("Potentially dangerous operations detected in content.")
    if safety.warning_hits:
        warnings.extend(safety.warning_hits)
    confidence = clamp(confidence, 1, 99)
    summary = build_summary(label, reasons)
    result = ClassificationResult(label=label, color=color, confidence=confidence, route=route, suggested_action=suggested_action, summary=summary, reasons=reasons, warnings=warnings, source_name=source_name, extension=extension, syntax=syntax, header=header, notation=notation, code_shape=code_shape, safety=safety)
    return asdict(result)

def format_human_report(result: dict) -> str:
    lines = []
    lines.append("=" * 80)
    lines.append("UMPATCHER PRE-FLIGHT CLASSIFIER REPORT")
    lines.append("=" * 80)
    lines.append(f"Source:              {result['source_name']}")
    lines.append(f"Extension:           {result['extension']}")
    lines.append(f"Label:               {result['label']}")
    lines.append(f"Color:               {result['color']}")
    lines.append(f"Confidence:          {result['confidence']}")
    lines.append(f"Route:               {result['route']}")
    lines.append(f"Suggested Action:    {result['suggested_action']}")
    lines.append(f"Summary:             {result['summary']}")
    lines.append("")
    lines.append("REASONS:")
    for item in result["reasons"] or ["none"]:
        lines.append(f"  - {item}")
    lines.append("")
    lines.append("WARNINGS:")
    for item in result["warnings"] or ["none"]:
        lines.append(f"  - {item}")
    lines.append("")
    return "\n".join(lines)

def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()

def parse_args(argv: list[str]) -> dict[str, object]:
    args = {"path": None, "stdin": False, "json": False, "compact": False}
    for arg in argv[1:]:
        if arg == "--stdin":
            args["stdin"] = True
        elif arg == "--json":
            args["json"] = True
        elif arg == "--compact":
            args["compact"] = True
        elif not arg.startswith("--") and args["path"] is None:
            args["path"] = arg
    return args

def main() -> int:
    args = parse_args(sys.argv)
    if args["stdin"]:
        source_name = "stdin_buffer.txt"
        raw_text = sys.stdin.read()
    elif args["path"]:
        source_name = str(args["path"])
        raw_text = read_text_file(source_name)
    else:
        print("Usage:")
        print("  python3 umpatcher_code_labeler.py /path/to/file.py")
        print("  cat somefile.txt | python3 umpatcher_code_labeler.py --stdin")
        print("Options:")
        print("  --json     Output JSON")
        print("  --compact  Compact JSON")
        return 1
    result = classify_content(raw_text, source_name=source_name)
    if args["json"]:
        print(json.dumps(result, separators=(",", ":")) if args["compact"] else json.dumps(result, indent=2))
    else:
        print(format_human_report(result))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
