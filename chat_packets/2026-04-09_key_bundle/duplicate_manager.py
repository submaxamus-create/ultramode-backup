#!/usr/bin/env python3
# duplicate_manager.py — simple hash duplicate finder (key bundle)
# Hi Mom.
from __future__ import annotations
import hashlib
from pathlib import Path
from typing import Dict, List

def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def build_duplicate_report(paths: List[Path]) -> Dict[str, List[str]]:
    by_hash: Dict[str, List[str]] = {}
    for p in paths:
        try:
            h = file_hash(p)
        except Exception:
            continue
        by_hash.setdefault(h, []).append(str(p))
    return {h: ps for h, ps in by_hash.items() if len(ps) > 1}
