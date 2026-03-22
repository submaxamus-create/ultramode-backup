#!/usr/bin/env python3
# =============================================================================
# PROJECT NOTATIONS — DO NOT DELETE OR MODIFY EXISTING LINES — ONLY APPEND
# =============================================================================
# FILENAME:      um_notation.py
# FOLDER PATH:   /userdata/system/ultramode/modules/mandatory/
# DESTINATION:   /userdata/system/ultramode/modules/mandatory/um_notation.py
# Version:       v1.0
# Revision:      r1
#
# PURPOSE:
#   - Sidecar helper for Ultramode notation/log handling.
#   - Keeps bulky notation utilities out of um.py and other GUI modules.
#   - Provides safe runtime note append, log tail, log summary, and status helpers.
#
# CHANGE LOG (APPEND-ONLY)
# YYYY-MM-DD HH:MM | AUTHOR | VERSION | REVISION | NOTE
# 2026-03-15 21:00 | ChatGPT | v1.0 | r1 | Created sidecar helper for notation/log structure, runtime note capture, and root menu tooling.
# =============================================================================
#
# Hi Mom.
# =============================================================================

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List

ULTRAMODE_ROOT = Path('/userdata/system/ultramode')
LOG_ROOT = ULTRAMODE_ROOT / 'logs'
MODULE_LOG_ROOT = LOG_ROOT / 'modules'
EXPORT_ROOT = LOG_ROOT / 'exports'
SIDECAR_LOG = MODULE_LOG_ROOT / 'um_notation_log.txt'
RUNTIME_NOTES_LOG = MODULE_LOG_ROOT / 'um_runtime_notes_log.txt'


def ensure_structure() -> None:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    MODULE_LOG_ROOT.mkdir(parents=True, exist_ok=True)
    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)


def _append_line(path: Path, line: str) -> bool:
    ensure_structure()
    try:
        with path.open('a', encoding='utf-8', errors='ignore') as fh:
            fh.write(line.rstrip('\n') + '\n')
        return True
    except Exception:
        return False


def append_runtime_note(message: str, category: str = 'RUNTIME') -> bool:
    stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'{stamp} | {category} | {message}'
    ok_a = _append_line(RUNTIME_NOTES_LOG, line)
    ok_b = _append_line(SIDECAR_LOG, line)
    return bool(ok_a and ok_b)


def read_log_tail(path: str, lines: int = 10) -> List[str]:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            data = fh.readlines()
        return [line.rstrip('\n') for line in data[-max(1, lines):]]
    except Exception as exc:
        return [f'log read failed: {exc}']


def summarize_log(path: str) -> str:
    target = Path(path)
    if not target.exists():
        return 'log missing'
    line_count = 0
    warning_count = 0
    error_count = 0
    try:
        with target.open('r', encoding='utf-8', errors='ignore') as fh:
            for line in fh:
                line_count += 1
                upper = line.upper()
                if 'WARNING' in upper:
                    warning_count += 1
                if 'ERROR' in upper:
                    error_count += 1
        return f'log lines={line_count} warnings={warning_count} errors={error_count}'
    except Exception as exc:
        return f'log summary failed: {exc}'


def export_digest(name: str, lines: List[str]) -> bool:
    ensure_structure()
    target = EXPORT_ROOT / name
    try:
        with target.open('w', encoding='utf-8', errors='ignore') as fh:
            for line in lines:
                fh.write(str(line).rstrip('\n') + '\n')
        return True
    except Exception:
        return False


def get_sidecar_status() -> str:
    ensure_structure()
    ready = SIDECAR_LOG.exists() or RUNTIME_NOTES_LOG.exists()
    return 'sidecar ready' if ready else 'sidecar armed'
