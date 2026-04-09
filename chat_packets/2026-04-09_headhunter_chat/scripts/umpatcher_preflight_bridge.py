#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
####################################################################################################
# FILENAME: umpatcher_preflight_bridge_v1_0_r1_2026-04-08.py
# FOLDER PATH: /userdata/system/ultramode/modules/patcher/
# DESTINATION: /userdata/system/ultramode/modules/patcher/umpatcher_preflight_bridge.py
# PATCH TYPE: NEW_FILE
# VERSION: 1.0
# REVISION: r1
# SUMMARY: Bridge/helper for UMPatcher to run the code labeler against buffer/file content and return
#          lamp-ready status, route decisions, and compact UI fields.
####################################################################################################
"""

from __future__ import annotations

import json
import os
from typing import Any

try:
    from umpatcher_code_labeler import classify_content
except ImportError:
    import sys
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    if CURRENT_DIR not in sys.path:
        sys.path.insert(0, CURRENT_DIR)
    from umpatcher_code_labeler import classify_content

LABEL_TO_PRIMARY_LAMP = {
    "VALID_PATCH_PY": "GREEN",
    "VALID_PATCH_PY_WITH_RISK": "ORANGE",
    "UNTRUSTED_PYTHON": "ORANGE",
    "PYTHON_FRAGMENT": "ORANGE",
    "BROKEN_HEADER": "ORANGE",
    "REVIEW_REQUIRED": "ORANGE",
    "SIDECAR_OR_TEXT_DOC": "BLUE",
    "BROKEN_SYNTAX": "RED",
    "MISSING_DESTINATION": "RED",
    "TEXT_NOT_CODE": "RED",
    "EMPTY_CONTENT": "RED",
}

ROUTE_TO_DECISION = {
    "patch_review_ready": "ALLOW_REVIEW",
    "high_attention_review": "ALLOW_REVIEW_HIGH_RISK",
    "python_review_no_header": "SEND_TO_REVIEW",
    "fragment_repair_or_wrap": "SEND_TO_WRAP_REPAIR",
    "header_repair": "SEND_TO_HEADER_REPAIR",
    "syntax_repair": "BLOCK_AND_REPAIR",
    "block_until_destination": "BLOCK",
    "save_as_text_or_sidecar": "SAVE_AS_TEXT",
    "save_as_text_or_block": "BLOCK_OR_SAVE_TEXT",
    "manual_review": "SEND_TO_REVIEW",
    "review_queue": "SEND_TO_REVIEW",
    "block": "BLOCK",
}

def _bool_to_lamp(ok: bool, bad_color: str = "RED") -> str:
    return "GREEN" if ok else bad_color

def _first_reason(result: dict[str, Any]) -> str:
    reasons = result.get("reasons", []) or []
    return reasons[0] if reasons else "No reason available."

def _top_warnings(result: dict[str, Any], limit: int = 3) -> list[str]:
    warnings = result.get("warnings", []) or []
    return warnings[:limit]

def _build_lamps(result: dict[str, Any]) -> dict[str, str]:
    syntax = result.get("syntax", {})
    header = result.get("header", {})
    notation = result.get("notation", {})
    safety = result.get("safety", {})
    code_shape = result.get("code_shape", {})
    syntax_lamp = _bool_to_lamp(bool(syntax.get("valid")), "RED")
    header_ok = header.get("found_any_header") and not header.get("required_missing") and header.get("recognition_zone_ok")
    header_lamp = _bool_to_lamp(bool(header_ok), "ORANGE")
    destination_lamp = _bool_to_lamp(bool(header.get("has_destination_value")), "RED")
    notation_count = int(notation.get("notation_count", 0) or 0)
    notation_lamp = "GREEN" if notation_count >= 2 else ("ORANGE" if notation_count >= 1 else "BLUE")
    danger_score = int(safety.get("danger_score", 0) or 0)
    if danger_score <= 0:
        danger_lamp = "GREEN"
    elif danger_score < 10:
        danger_lamp = "ORANGE"
    else:
        danger_lamp = "RED"
    likely_python = bool(code_shape.get("likely_python"))
    trust_lamp = "GREEN" if result.get("label") == "VALID_PATCH_PY" else ("ORANGE" if likely_python else ("BLUE" if result.get("label") == "SIDECAR_OR_TEXT_DOC" else "RED"))
    primary_lamp = LABEL_TO_PRIMARY_LAMP.get(result.get("label", ""), "ORANGE")
    return {
        "primary": primary_lamp,
        "syntax": syntax_lamp,
        "header": header_lamp,
        "destination": destination_lamp,
        "notation": notation_lamp,
        "danger": danger_lamp,
        "trust": trust_lamp,
    }

def _build_compact_ui_block(result: dict[str, Any], lamps: dict[str, str]) -> dict[str, Any]:
    header = result.get("header", {})
    code_shape = result.get("code_shape", {})
    syntax = result.get("syntax", {})
    return {
        "title": "UMPatcher Preflight",
        "primary_lamp": lamps["primary"],
        "label": result.get("label"),
        "confidence": result.get("confidence"),
        "decision": ROUTE_TO_DECISION.get(result.get("route", ""), "SEND_TO_REVIEW"),
        "summary": result.get("summary"),
        "first_reason": _first_reason(result),
        "top_warnings": _top_warnings(result),
        "source_name": result.get("source_name"),
        "extension": result.get("extension"),
        "line_count": code_shape.get("line_count"),
        "python_score": code_shape.get("python_score"),
        "likely_python": code_shape.get("likely_python"),
        "likely_fragment": code_shape.get("likely_fragment"),
        "likely_full_script": code_shape.get("likely_full_script"),
        "syntax_valid": syntax.get("valid"),
        "syntax_error_line": syntax.get("lineno"),
        "destination_value": header.get("destination_value"),
        "required_missing": header.get("required_missing", []),
        "protected_missing": header.get("protected_markers_missing", []),
        "lamps": lamps,
    }

def preflight_from_text(raw_text: str, source_name: str = "buffer.txt") -> dict[str, Any]:
    classifier_result = classify_content(raw_text, source_name=source_name)
    lamps = _build_lamps(classifier_result)
    ui = _build_compact_ui_block(classifier_result, lamps)
    return {"ok": True, "source_type": "text", "classifier_result": classifier_result, "ui": ui}

def preflight_from_file(path: str) -> dict[str, Any]:
    if not path:
        return {"ok": False, "error": "No path provided.", "ui": {"title": "UMPatcher Preflight", "primary_lamp": "RED", "label": "ERROR", "decision": "BLOCK", "summary": "No file path provided."}}
    if not os.path.isfile(path):
        return {"ok": False, "error": f"File not found: {path}", "ui": {"title": "UMPatcher Preflight", "primary_lamp": "RED", "label": "ERROR", "decision": "BLOCK", "summary": f"File not found: {path}"}}
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        raw_text = handle.read()
    return preflight_from_text(raw_text, source_name=path)

def get_preflight_status_for_um(raw_text: str | None = None, path: str | None = None) -> dict[str, Any]:
    if raw_text is not None:
        return preflight_from_text(raw_text, source_name=path or "buffer.txt")
    if path:
        return preflight_from_file(path)
    return {"ok": False, "error": "Neither raw_text nor path was provided.", "ui": {"title": "UMPatcher Preflight", "primary_lamp": "RED", "label": "ERROR", "decision": "BLOCK", "summary": "No input provided to preflight bridge."}}

def _print_pretty(data: dict[str, Any]) -> None:
    print(json.dumps(data, indent=2))

def main() -> int:
    import sys
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 umpatcher_preflight_bridge.py /path/to/file")
        return 1
    path = sys.argv[1]
    result = preflight_from_file(path)
    _print_pretty(result["ui"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
