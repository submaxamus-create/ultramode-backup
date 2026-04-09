#!/usr/bin/env python3
# matcher.py — orphan/loose match finder (key bundle)
# Hi Mom.
from __future__ import annotations
import os
from pathlib import Path
from typing import List, Dict

def find_orphans(root: Path) -> List[Dict[str, str]]:
    """Simple heuristic: files that have no same-stem siblings in folder."""
    results = []
    for dirpath, _, filenames in os.walk(root):
        base = Path(dirpath)
        files = [base / f for f in filenames]
        stems = {}
        for p in files:
            stems.setdefault(p.stem.lower(), []).append(p)
        for stem, group in stems.items():
            if len(group) == 1:
                p = group[0]
                results.append({
                    "path": str(p),
                    "reason": "no_sibling_same_stem"
                })
    return results
