#!/usr/bin/env python3
# ============================================================
# FILENAME:      github_sync_agent_v0_3_full_tree.py
# FOLDER PATH:   /master_logs/runtime/
# DESTINATION:   /master_logs/runtime/github_sync_agent_v0_3_full_tree.py
# PATCH TYPE:    CREATE
# VERSION:       0.3
# REVISION:      1
# SUMMARY:       Push a wider UltraMode tree to GitHub with allow and skip rules
# ============================================================
# Hi Mom.
#
# Safe default:
# - dry run unless --live is passed
# - skips big/binary/noisy folders by default
# - intended to expand beyond master logs without blindly syncing everything

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LOCAL_ROOT = Path('/userdata/system/ultramode')
DEFAULT_REPO = 'submaxamus-create/ultramode-backup'
DEFAULT_BRANCH = 'main'
DEFAULT_REMOTE_PREFIX = 'synced_ultramode_tree'
DEFAULT_ALLOWED_EXTS = {'.txt', '.py', '.md', '.json', '.yaml', '.yml', '.csv', '.log', '.ini', '.cfg', '.sh'}
DEFAULT_SKIP_DIRS = {
    '.git', '__pycache__', '.mypy_cache', '.pytest_cache', '.venv', 'node_modules',
    'GAME', 'Ultramode github_files', 'Ultramode github2_files', 'Taskbar Monitoring in UltraMode_files',
    'Ultra Mode Recovery_files', 'SPRUCE TREE_files'
}
DEFAULT_SKIP_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.pdf', '.zip', '.htm', '.html', '.css', '.js'}
DEFAULT_MAX_BYTES = 2_000_000
API_BASE = 'https://api.github.com'


@dataclass
class SyncResult:
    created: list[str]
    updated: list[str]
    skipped: list[str]
    errors: list[str]


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')


def should_skip_dir(name: str, skip_dirs: set[str]) -> bool:
    return name in skip_dirs


def is_allowed_file(path: Path, allowed_exts: set[str], skip_exts: set[str], max_bytes: int) -> tuple[bool, str]:
    if path.suffix.lower() in skip_exts:
        return False, 'skip_ext'
    try:
        size = path.stat().st_size
    except Exception:
        return False, 'stat_error'
    if size > max_bytes:
        return False, 'too_large'
    if path.suffix.lower() in allowed_exts:
        return True, 'allowed_ext'
    guessed, _ = mimetypes.guess_type(str(path))
    if guessed and guessed.startswith('text/'):
        return True, 'text_guess'
    return False, 'not_allowed'


def iter_local_files(root: Path, allowed_exts: set[str], skip_exts: set[str], skip_dirs: set[str], max_bytes: int):
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not should_skip_dir(d, skip_dirs)]
        current_path = Path(current_root)
        for name in sorted(files):
            path = current_path / name
            allowed, reason = is_allowed_file(path, allowed_exts, skip_exts, max_bytes)
            yield path, allowed, reason


def get_remote_sha(repo: str, branch: str, remote_path: str, token: str) -> str | None:
    encoded_path = urllib.parse.quote(remote_path)
    url = f"{API_BASE}/repos/{repo}/contents/{encoded_path}?ref={urllib.parse.quote(branch)}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'UltraMode-GitHub-Sync-Agent/0.3',
    }
    req = urllib.request.Request(url=url, headers=headers, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('sha')
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        body = exc.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'GET remote sha failed for {remote_path}: HTTP {exc.code}: {body}') from exc


def put_file(repo: str, branch: str, remote_path: str, local_path: Path, token: str, commit_message: str, dry_run: bool) -> str:
    content_b64 = base64.b64encode(local_path.read_bytes()).decode('ascii')
    existing_sha = get_remote_sha(repo, branch, remote_path, token)
    if dry_run:
        return 'update' if existing_sha else 'create'

    payload = {
        'message': commit_message,
        'content': content_b64,
        'branch': branch,
    }
    if existing_sha:
        payload['sha'] = existing_sha

    encoded_path = urllib.parse.quote(remote_path)
    url = f"{API_BASE}/repos/{repo}/contents/{encoded_path}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'UltraMode-GitHub-Sync-Agent/0.3',
        'Content-Type': 'application/json',
    }
    req = urllib.request.Request(url=url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='PUT')
    try:
        with urllib.request.urlopen(req, timeout=30):
            pass
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'PUT failed for {remote_path}: HTTP {exc.code}: {body}') from exc
    return 'update' if existing_sha else 'create'


def sync_tree(local_root: Path, repo: str, branch: str, remote_prefix: str, token: str, dry_run: bool,
              allowed_exts: set[str], skip_exts: set[str], skip_dirs: set[str], max_bytes: int) -> SyncResult:
    result = SyncResult(created=[], updated=[], skipped=[], errors=[])
    if not local_root.exists():
        result.errors.append(f'local root missing: {local_root}')
        return result

    for local_file, allowed, reason in iter_local_files(local_root, allowed_exts, skip_exts, skip_dirs, max_bytes):
        rel = local_file.relative_to(local_root).as_posix()
        if not allowed:
            result.skipped.append(f'{rel} | {reason}')
            continue
        remote_path = f"{remote_prefix}/{rel}"
        commit_message = f"sync ultramode tree: {rel} @ {now_stamp()}"
        try:
            action = put_file(repo, branch, remote_path, local_file, token, commit_message, dry_run)
            if action == 'create':
                result.created.append(rel)
            else:
                result.updated.append(rel)
        except Exception as exc:
            result.errors.append(f'{rel} -> {exc}')
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Push a wider UltraMode tree to GitHub using allow/skip rules.')
    parser.add_argument('--root', default=str(DEFAULT_LOCAL_ROOT))
    parser.add_argument('--repo', default=DEFAULT_REPO)
    parser.add_argument('--branch', default=DEFAULT_BRANCH)
    parser.add_argument('--remote-prefix', default=DEFAULT_REMOTE_PREFIX)
    parser.add_argument('--token-env', default='GITHUB_TOKEN')
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--ext', action='append', default=[])
    parser.add_argument('--skip-ext', action='append', default=[])
    parser.add_argument('--skip-dir', action='append', default=[])
    parser.add_argument('--max-bytes', type=int, default=DEFAULT_MAX_BYTES)
    return parser


def print_summary(result: SyncResult, dry_run: bool) -> None:
    print('=' * 72)
    print(f"ULTRAMODE GITHUB SYNC AGENT v0.3 | {'DRY RUN' if dry_run else 'LIVE PUSH'}")
    print('=' * 72)
    print(f'created: {len(result.created)}')
    print(f'updated: {len(result.updated)}')
    print(f'skipped: {len(result.skipped)}')
    for item in result.skipped[:20]:
        print(f'  - {item}')
    if len(result.skipped) > 20:
        print(f'  ... {len(result.skipped) - 20} more skipped')
    print(f'errors: {len(result.errors)}')
    for item in result.errors[:20]:
        print(f'  ! {item}')
    print('=' * 72)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    token = os.environ.get(args.token_env, '').strip()
    if not token:
        print(f'ERROR: missing token in env var {args.token_env}')
        print(f'export {args.token_env}="YOUR_TOKEN_HERE"')
        return 1

    allowed_exts = set(DEFAULT_ALLOWED_EXTS)
    skip_exts = set(DEFAULT_SKIP_EXTS)
    skip_dirs = set(DEFAULT_SKIP_DIRS)
    for item in args.ext:
        ext = item if item.startswith('.') else f'.{item}'
        allowed_exts.add(ext.lower())
    for item in args.skip_ext:
        ext = item if item.startswith('.') else f'.{item}'
        skip_exts.add(ext.lower())
    for item in args.skip_dir:
        skip_dirs.add(item)

    dry_run = not args.live
    result = sync_tree(
        local_root=Path(args.root),
        repo=args.repo,
        branch=args.branch,
        remote_prefix=args.remote_prefix.strip('/'),
        token=token,
        dry_run=dry_run,
        allowed_exts=allowed_exts,
        skip_exts=skip_exts,
        skip_dirs=skip_dirs,
        max_bytes=args.max_bytes,
    )
    print_summary(result, dry_run)
    return 1 if result.errors else 0


if __name__ == '__main__':
    sys.exit(main())
