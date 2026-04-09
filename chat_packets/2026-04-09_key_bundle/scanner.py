#!/usr/bin/env python3
# scanner.py — path scanner (key bundle)
# Hi Mom.
from __future__ import annotations
import os
from pathlib import Path
from typing import List

def scan_paths(root: Path) -> List[Path]:
    out: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {'__pycache__', '.git'}]
        for f in filenames:
            out.append(Path(dirpath) / f)
    return out
