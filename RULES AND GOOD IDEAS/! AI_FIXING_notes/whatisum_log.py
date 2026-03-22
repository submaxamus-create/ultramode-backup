#!/usr/bin/env python3
"""
whatisum_log.py
Author: Paul
Created: 2026-03-12
Purpose: Create a single WHATISUM.LOG file and provide utilities to collect scripts,
         extract notation tokens from saved pages, normalize headers, build a manifest,
         and prepare a GitHub-ready repository skeleton for modular-scripts-consolidation.
Inputs: None required to generate WHATISUM.LOG; optional paths/URLs for evidence and scripts.
Outputs: WHATISUM.LOG (text), helper scripts in tools/, and optional repo skeleton.
Dependencies: Python 3.8+; requests (optional for web archiving); pathlib, json, csv, re, shutil, datetime
Notation tags: notate, archive, normalize, manifest, evidence, header
Notes: This single-file tool encapsulates the full project summary and provides functions
       to perform the actions described in WHATISUM.LOG. Run with --write-log to create WHATISUM.LOG.
"""

import os
import re
import json
import csv
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# Optional import for web fetching; only used if user explicitly calls web archive functions.
try:
    import requests
except Exception:
    requests = None

# ---------------------------------------------------------------------------
# CONSTANTS: core content that will be written into WHATISUM.LOG verbatim
# ---------------------------------------------------------------------------

_WHATISUM_CONTENT = f"""WHATISUM.LOG

Project name: modular-scripts-consolidation
Main file: um
Owner: Paul
Date: {datetime.utcnow().date().isoformat()}

---

Current inventory snapshot
- Many small Python tools named like filename.py scattered across machines and chats.
- Multiple notation styles used across scripts and chat logs (examples: # NOTE:, @notate, /* notate that */, inline prose like "notate that" in web chats).
- Web pages and chat threads contain actionable notes and decisions that must be preserved (phrases to capture include "notate that", "put that in notation", "add to notation").
- Main problems: inconsistent headers, missing docstrings, duplicated or out-of-sync notations across scripts, and forgotten tools with no metadata.
- Desired end state: a GitHub repository containing a clean folder-of-folders structure, every script with standardized headers/metadata, extracted web/chat evidence saved as files, and an automated pipeline for AI to fix headers and plug scripts into module menus.

---

Problems and risks (what to fix first)
- Fragmented notations — different scripts use different annotation formats; updates in one place are not propagated elsewhere.
- Missing metadata — many scripts lack a header with purpose, author, inputs, outputs, and dependencies.
- Lost tools — utilities created over time are undocumented and effectively orphaned.
- Uncaptured conversations — web pages and chat threads with "notate that" are ephemeral and must be archived before they are closed or unpinned.
- Integration gaps — scripts are not registered in module menus or a central manifest, so functionality is hidden.
- Merge conflicts and duplication — without consolidation, automated merges will create conflicts and duplicate logic.

---

High level plan of action
1. Archive evidence — crawl and save every web page and chat thread that contains notation phrases into a local folder evidence/ as raw HTML plus a plain-text extraction.
2. Inventory scripts — collect all *.py and related files into src/ while preserving original paths in src/original_paths.txt.
3. Normalize headers — add a standardized header template to every script (author, date, description, inputs, outputs, tags, notation-format).
4. Extract notations — parse each script and saved chat/page for notation tokens and produce a single canonical NOTATIONS.md.
5. Create manifest and menus — generate modules/manifest.json listing each script, its entry points, and the menu path where it should appear.
6. Automate fixes with AI — feed each file to an AI worker that: (a) rewrites/standardizes the header, (b) consolidates duplicated notations into NOTATIONS.md, (c) suggests where to plug the script into menus.
7. Review and merge — human review of AI changes, then commit to GitHub with meaningful commits and PRs.
8. Maintain — add CI checks that enforce header presence and notation consistency on future commits.

---

Standard header template to apply to every script
\"\"\"python
\"\"\"
Filename: filename.py
Author: Paul
Created: {datetime.utcnow().date().isoformat()}
Purpose: Short one-line description of what this script does.
Inputs: list of inputs or None
Outputs: list of outputs or None
Dependencies: list of external libs or None
Notation tags: comma-separated tags like notate, config, ui, menu
Notes: Any special instructions or links to evidence files in evidence/
\"\"\"
\"\"\"

---

Evidence capture strategy
- Search tokens: scan saved pages and chat exports for exact phrases: notate that, put that in notation, add to notation, notation:, @notate.
- Save format: for each matched page create two files: evidence/<slug>.html and evidence/<slug>.txt (plain text with matched lines highlighted).
- Index: evidence/index.csv with columns slug;source_url;date_saved;matched_tokens.
- Retention: mark threads that must be closed/unpinned after archiving in evidence/close_list.txt.

---

Suggested GitHub repository layout
Path | Purpose | Notes
README.md | Project overview and quick start | Include consolidation goals
src/ | All scripts collected | Preserve originals in src/originals/
modules/ | Module wrappers and menus | manifest.json lives here
evidence/ | Saved web pages and chat exports | HTML and text pairs
tools/ | Extraction and normalization scripts | Scripts to run the pipeline
docs/ | NOTATIONS.md and developer guides | Single source of truth for notations
.github/workflows/ | CI checks for headers and notation rules | Enforce standards on PRs

---

Concrete commands and a starter extraction script
Shell commands to collect files:
mkdir -p repo/{{src,evidence,modules,tools,docs}}
rsync -av --include='*/' --include='*.py' --exclude='*' /path/to/search/ repo/src/

Python starter to crawl saved URLs list and extract notation lines (example provided in tools/extract_notations.py)

Note: run web-archiving only against pages you control or have permission to archive.

---

Automation and AI workflow outline
- Step A: Run tools/scan_evidence.py to build evidence/index.csv.
- Step B: Run tools/collect_scripts.py to copy all scripts into src/ and produce src/original_paths.txt.
- Step C: For each file in src/, run tools/ai_fix_header.py which:
  - reads the file,
  - inserts or updates the standardized header,
  - extracts inline notation tokens and appends them to docs/NOTATIONS.md with a source pointer.
- Step D: Generate modules/manifest.json from docs/NOTATIONS.md and script metadata.
- Step E: Create a PR per module group with clear commit messages like docs: add standardized header to <filename.py> and chore: register <filename.py> in manifest.

Best practices: use .gitignore to exclude logs and env files, write meaningful commit messages, and keep commits small and focused.

---

Notation consolidation rules
- Canonicalize tokens: map all variants to a single canonical token NOTATE.
- Single source of truth: docs/NOTATIONS.md must list each notation with id, text, source, and recommended action.
- No inline-only decisions: any decision captured in a chat must have a corresponding entry in NOTATIONS.md and a linked script or issue.
- Enforce via CI: PRs that add or modify notation tokens must update NOTATIONS.md or be rejected.

---

Quick governance checklist for the first commit
- [ ] Create repository skeleton and push to GitHub.
- [ ] Add .gitignore and CODE_OF_CONDUCT or CONTRIBUTING.md.
- [ ] Run script collection and evidence capture.
- [ ] Apply header template to all scripts.
- [ ] Produce docs/NOTATIONS.md and modules/manifest.json.
- [ ] Open PRs grouped by module for human review.

---

Immediate next-step artifacts described
- README.md skeleton (project overview and quick start).
- tools/extract_notations.py (starter extraction script).
- tools/ai_fix_header.py (starter that applies the header template and extracts notation tokens).
- docs/NOTATIONS.md skeleton and a sample modules/manifest.json for the first 10 scripts.

---

Operational notes
- Many small scripts lack headers and metadata; the header template above must be applied consistently.
- Evidence capture must be prioritized for any web pages or chat threads that contain the tokens listed in the Evidence capture strategy. Those threads should be archived before being closed or unpinned.
- The manifest should be authoritative for menus and module registration; scripts not listed in the manifest are considered unregistered and must be reviewed.
- CI checks should fail builds that remove or alter notation tokens without updating docs/NOTATIONS.md.
- Human review is required for AI-suggested header changes before merging.

End of WHATISUM.LOG
"""

# ---------------------------------------------------------------------------
# HEADER TEMPLATE: used to normalize script headers
# ---------------------------------------------------------------------------

HEADER_TEMPLATE = '''"""
Filename: {filename}
Author: Paul
Created: {created}
Purpose: {purpose}
Inputs: {inputs}
Outputs: {outputs}
Dependencies: {dependencies}
Notation tags: {tags}
Notes: {notes}
"""
'''

# ---------------------------------------------------------------------------
# UTILITIES: file system helpers and safe write
# ---------------------------------------------------------------------------

def safe_write_text(path: Path, text: str, overwrite: bool = True):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return False
    path.write_text(text, encoding='utf-8')
    return True

# ---------------------------------------------------------------------------
# CORE ACTIONS: create WHATISUM.LOG, repo skeleton, starter tools, and helpers
# ---------------------------------------------------------------------------

def write_whatisum_log(out_path: Path = Path('WHATISUM.LOG')):
    """Write the consolidated WHATISUM.LOG file to disk."""
    safe_write_text(out_path, _WHATISUM_CONTENT)
    return out_path

def create_repo_skeleton(base: Path = Path('repo')):
    """Create the suggested GitHub repository layout skeleton."""
    dirs = [
        base / 'src',
        base / 'src' / 'originals',
        base / 'modules',
        base / 'evidence',
        base / 'tools',
        base / 'docs',
        base / '.github' / 'workflows'
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    # Create placeholder files
    safe_write_text(base / 'README.md', '# modular-scripts-consolidation\n\nSee WHATISUM.LOG for details.\n')
    safe_write_text(base / '.gitignore', 'venv/\n__pycache__/\n*.log\n.env\n')
    safe_write_text(base / 'docs' / 'NOTATIONS.md', '# NOTATIONS\n\nCanonical notation registry.\n')
    safe_write_text(base / 'modules' / 'manifest.json', json.dumps({"modules": []}, indent=2))
    return base

# ---------------------------------------------------------------------------
# EVIDENCE EXTRACTION: functions to archive web pages and extract notation lines
# ---------------------------------------------------------------------------

TOKENS = [r'notate that', r'put that in notation', r'add to notation', r'notation:', r'@notate']

def extract_text_from_html(html: str) -> str:
    """Very simple HTML to text extraction (strip tags)."""
    # Remove scripts/styles
    html = re.sub(r'(?is)<(script|style).*?>.*?</\\1>', '', html)
    # Remove tags
    text = re.sub(r'<[^>]+>', '', html)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def find_token_lines(text: str):
    """Return lines (segments) that contain any of the tokens."""
    lower = text.lower()
    matches = []
    for token in TOKENS:
        if token in lower:
            # find surrounding context
            for m in re.finditer(re.escape(token), lower):
                start = max(0, m.start() - 120)
                end = min(len(text), m.end() + 120)
                snippet = text[start:end].strip()
                matches.append(snippet)
    return matches

def save_evidence_from_url(url: str, outdir: Path = Path('evidence')):
    """Fetch a URL and save HTML and extracted text; returns slug and matches.
       Requires requests to be available. Use only for pages you control or have permission to archive."""
    if requests is None:
        raise RuntimeError("requests library not available; install requests to enable web archiving.")
    r = requests.get(url, timeout=30)
    html = r.text
    text = extract_text_from_html(html)
    slug = re.sub(r'[^0-9A-Za-z_-]', '_', url)[:120]
    outdir.mkdir(parents=True, exist_ok=True)
    html_path = outdir / f'{slug}.html'
    txt_path = outdir / f'{slug}.txt'
    safe_write_text(html_path, html)
    safe_write_text(txt_path, text)
    matches = find_token_lines(text)
    # Append to index.csv
    index_path = outdir / 'index.csv'
    exists = index_path.exists()
    with index_path.open('a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        if not exists:
            writer.writerow(['slug', 'source_url', 'date_saved', 'matched_tokens'])
        writer.writerow([slug, url, datetime.utcnow().isoformat(), '|'.join(matches)])
    return slug, matches

# ---------------------------------------------------------------------------
# SCRIPT COLLECTION: copy scripts into src/ and record original paths
# ---------------------------------------------------------------------------

def collect_scripts(source_paths, dest_dir: Path = Path('src')):
    """Copy provided script paths into dest_dir preserving filenames; record original paths."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    original_paths = []
    for p in source_paths:
        src = Path(p)
        if not src.exists():
            continue
        dest = dest_dir / src.name
        shutil.copy2(src, dest)
        original_paths.append(f'{src.resolve()} -> {dest.resolve()}')
    safe_write_text(dest_dir / 'original_paths.txt', '\n'.join(original_paths))
    return dest_dir / 'original_paths.txt'

# ---------------------------------------------------------------------------
# HEADER NORMALIZATION: insert or update standardized header in a script
# ---------------------------------------------------------------------------

def normalize_header_in_file(file_path: Path, author='Paul', default_purpose='TBD', tags='notate'):
    """Ensure the file has the standard header; if missing, insert one at top."""
    text = file_path.read_text(encoding='utf-8')
    created = datetime.utcnow().date().isoformat()
    filename = file_path.name
    # Detect existing triple-quote header at top
    header_match = re.match(r'^\s*(?P<header>"""[\s\S]*?""")', text)
    if header_match:
        # Replace existing header with standardized template while preserving Purpose if found
        existing = header_match.group('header')
        # Try to extract Purpose line
        purpose_match = re.search(r'Purpose:\s*(.*)', existing)
        purpose = purpose_match.group(1).strip() if purpose_match else default_purpose
        new_header = HEADER_TEMPLATE.format(
            filename=filename,
            created=created,
            purpose=purpose,
            inputs='None',
            outputs='None',
            dependencies='None',
            tags=tags,
            notes='See docs/NOTATIONS.md and evidence/ for related notes.'
        )
        new_text = re.sub(r'^\s*"""[\s\S]*?"""', new_header, text, count=1)
    else:
        new_header = HEADER_TEMPLATE.format(
            filename=filename,
            created=created,
            purpose=default_purpose,
            inputs='None',
            outputs='None',
            dependencies='None',
            tags=tags,
            notes='See docs/NOTATIONS.md and evidence/ for related notes.'
        )
        new_text = new_header + '\n' + text
    file_path.write_text(new_text, encoding='utf-8')
    return file_path

# ---------------------------------------------------------------------------
# NOTATION EXTRACTION: scan scripts and evidence for tokens and build NOTATIONS.md
# ---------------------------------------------------------------------------

def build_notations_registry(src_dir: Path = Path('src'), evidence_dir: Path = Path('evidence'), out_path: Path = Path('docs/NOTATIONS.md')):
    """Scan src/ and evidence/ for notation tokens and produce a canonical NOTATIONS.md."""
    entries = []
    # Scan scripts
    for py in src_dir.glob('*.py'):
        text = py.read_text(encoding='utf-8')
        lower = text.lower()
        if any(tok in lower for tok in TOKENS):
            matches = []
            for tok in TOKENS:
                for m in re.finditer(re.escape(tok), lower):
                    start = max(0, m.start() - 80)
                    end = min(len(text), m.end() + 80)
                    snippet = text[start:end].replace('\n', ' ')
                    matches.append(snippet.strip())
            entries.append({
                'id': f'src:{py.name}',
                'source': str(py),
                'matches': matches
            })
    # Scan evidence text files
    if evidence_dir.exists():
        for txt in evidence_dir.glob('*.txt'):
            text = txt.read_text(encoding='utf-8')
            lower = text.lower()
            if any(tok in lower for tok in TOKENS):
                matches = find_token_lines(text)
                entries.append({
                    'id': f'evidence:{txt.name}',
                    'source': str(txt),
                    'matches': matches
                })
    # Write NOTATIONS.md
    out_lines = ['# NOTATIONS\n', f'Generated: {datetime.utcnow().isoformat()}\n', 'Canonicalized token: NOTATE\n']
    for e in entries:
        out_lines.append(f'## {e["id"]}\n')
        out_lines.append(f'- **source**: {e["source"]}\n')
        for i, m in enumerate(e['matches'], 1):
            out_lines.append(f'- **match_{i}**: {m}\n')
        out_lines.append('\n')
    safe_write_text(out_path, '\n'.join(out_lines))
    return out_path

# ---------------------------------------------------------------------------
# MANIFEST GENERATION: create modules/manifest.json from scripts metadata
# ---------------------------------------------------------------------------

def generate_manifest(src_dir: Path = Path('src'), manifest_path: Path = Path('modules/manifest.json')):
    """Generate a simple manifest.json listing scripts and placeholder menu paths."""
    modules = []
    for py in sorted(src_dir.glob('*.py')):
        # Attempt to extract Purpose from header
        text = py.read_text(encoding='utf-8')
        purpose = 'TBD'
        m = re.search(r'Purpose:\s*(.*)', text)
        if m:
            purpose = m.group(1).strip()
        modules.append({
            'filename': py.name,
            'path': str(py),
            'purpose': purpose,
            'menu_path': f'Modules/{py.stem}'
        })
    manifest = {'generated': datetime.utcnow().isoformat(), 'modules': modules}
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    safe_write_text(manifest_path, json.dumps(manifest, indent=2))
    return manifest_path

# ---------------------------------------------------------------------------
# AI FIXER STUB: placeholder to show how AI could be invoked per-file (no external calls)
# ---------------------------------------------------------------------------

def ai_fix_header_stub(file_path: Path):
    """Stub function representing an AI worker that would rewrite headers and suggest menu placement.
       This function performs deterministic, local normalization only."""
    # Normalize header
    normalize_header_in_file(file_path)
    # Suggest menu placement by reading top-level docstring purpose
    text = file_path.read_text(encoding='utf-8')
    purpose = 'TBD'
    m = re.search(r'Purpose:\s*(.*)', text)
    if m:
        purpose = m.group(1).strip()
    suggestion = {'filename': file_path.name, 'suggested_menu': f'Modules/{file_path.stem}', 'purpose': purpose}
    return suggestion

# ---------------------------------------------------------------------------
# COMMAND-LINE INTERFACE
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='whatisum_log utility: create WHATISUM.LOG and helper actions.')
    parser.add_argument('--write-log', action='store_true', help='Write WHATISUM.LOG to current directory.')
    parser.add_argument('--create-skeleton', action='store_true', help='Create repository skeleton at ./repo.')
    parser.add_argument('--collect-scripts', nargs='+', help='Copy listed script paths into repo/src/.')
    parser.add_argument('--normalize-headers', action='store_true', help='Normalize headers for all scripts in src/.')
    parser.add_argument('--build-notations', action='store_true', help='Build docs/NOTATIONS.md from src/ and evidence/.')
    parser.add_argument('--generate-manifest', action='store_true', help='Generate modules/manifest.json from src/.')
    parser.add_argument('--archive-url', nargs=1, help='Fetch a URL and save evidence (requires requests).')
    parser.add_argument('--ai-fix-one', nargs=1, help='Run local AI-fixer stub on a single script path.')
    args = parser.parse_args()

    if args.write_log:
        p = write_whatisum_log(Path('WHATISUM.LOG'))
        print(f'Wrote WHATISUM.LOG -> {p.resolve()}')

    if args.create_skeleton:
        base = create_repo_skeleton(Path('repo'))
        print(f'Created repo skeleton at {base.resolve()}')

    if args.collect_scripts:
        p = collect_scripts(args.collect_scripts, dest_dir=Path('repo/src'))
        print(f'Collected scripts; original paths recorded in {p.resolve()}')

    if args.normalize_headers:
        src = Path('repo/src')
        if not src.exists():
            print('repo/src does not exist; run --create-skeleton or provide scripts first.')
        else:
            for py in src.glob('*.py'):
                normalize_header_in_file(py)
            print('Normalized headers for scripts in repo/src/')

    if args.build_notations:
        out = build_notations_registry(src_dir=Path('repo/src'), evidence_dir=Path('repo/evidence'), out_path=Path('repo/docs/NOTATIONS.md'))
        print(f'Built NOTATIONS.md -> {out.resolve()}')

    if args.generate_manifest:
        manifest = generate_manifest(src_dir=Path('repo/src'), manifest_path=Path('repo/modules/manifest.json'))
        print(f'Generated manifest -> {manifest.resolve()}')

    if args.archive_url:
        url = args.archive_url[0]
        try:
            slug, matches = save_evidence_from_url(url, outdir=Path('repo/evidence'))
            print(f'Archived {url} as {slug}; matches: {len(matches)}')
        except Exception as e:
            print(f'Error archiving URL: {e}')

    if args.ai_fix_one:
        path = Path(args.ai_fix_one[0])
        if not path.exists():
            print(f'File not found: {path}')
        else:
            suggestion = ai_fix_header_stub(path)
            print(json.dumps(suggestion, indent=2))

if __name__ == '__main__':
    main()
