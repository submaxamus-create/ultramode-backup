#!/usr/bin/env python3
"""
===============================================================================
ULTRAMODE MASTER LOGS BOOTSTRAP
===============================================================================
FILENAME:      um_master_logs_bootstrap_v1.py
VERSION:       v1
INTENDED PATH: /userdata/system/ultramode/um_master_logs_bootstrap_v1.py
PURPOSE:
  Create the UltraMode master log root and starter structure safely.
  This script is CREATE-ONLY by default for folders/files it manages.
  It will NOT move, delete, overwrite, or clean existing logs.

USER RULES CARRIED FORWARD:
  - Preserve worthwhile ideas/rules/lessons across chats.
  - Prefer concise operational output.
  - Richer notation is mandatory.
  - Do not lose history; use append-only text structures.
  - Future architecture should reduce repeated user explanation.

SAFETY RULES:
  - Existing files are never overwritten.
  - Existing folders are never removed or renamed.
  - No old logs are migrated automatically.
  - Re-running is safe and idempotent.

USAGE:
  python3 um_master_logs_bootstrap_v1.py
  python3 um_master_logs_bootstrap_v1.py --dry-run
  python3 um_master_logs_bootstrap_v1.py --root /userdata/system/ultramode/um_master_logs
===============================================================================
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable


# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: CHANGELOG
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# [v1]
# - Initial bootstrap script created for UltraMode master log architecture.
# - Creates the preferred root and required subfolders.
# - Seeds starter .txt files with strong headers and append-only sections.
# - Supports dry-run mode.
# - Uses create-only behavior; never overwrites existing files.
# - Prints path verification and concise end summary.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: ANALYSIS
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - The master log structure is meant to centralize project-wide rules, help,
#   notation, runtime evidence, generated reports, and future module summaries.
# - The bootstrap script must stay conservative: create missing only.
# - The bootstrap should be useful both for first setup and repeated safe runs.
# - The bootstrap is a foundational script, so clarity matters more than clever
#   compression.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: GOALS
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Reduce repeated manual setup of master log structure.
# - Establish canonical starter files future AI can read quickly.
# - Preserve rich notation culture from the start.
# - Provide a stable path for future gatherers, harvesters, and indexers.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: IDEAS
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Future version could offer optional seeding of module-local summary files.
# - Future version could emit a bootstrap report into reports/.
# - Future version could validate writable permissions more deeply.
# - Future version could add optional canonical template refresh previews
#   without touching existing files.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: AI_THINKTANK
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - This bootstrap should remain boring-safe rather than magically invasive.
# - It is better to create slightly more starter context than too little,
#   because future AI collaboration benefits from visible anchors.
# - Sidecar .txt transport is important because upload workflows prefer .txt.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: ARCHITECTURE_INTENT
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Root design:
#     /userdata/system/ultramode/um_master_logs/
# - Subfolder intent:
#     index/    -> where things are
#     rules/    -> global laws and AI rules
#     help/     -> usage/help authority
#     notation/ -> thinktank / ideas / architecture
#     runtime/  -> live/runtime logs and evidence
#     reports/  -> generated summaries and analysis reports
#     archive/  -> snapshots and old exported states
#     modules/  -> future per-module summaries or mirrors
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: CROSS_MODULE_RELATIONSHIPS
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Master logs are meant to support many modules, not just one script.
# - Gatherers can later promote repeated local rules into global rule files.
# - Module-local logs remain near modules; master logs become shared authority.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: SHARED_UI_RULES
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Not directly implemented here, but bootstrap files should make room for
#   future shared GUI standards, title bar rules, bubble help, date/clock, and
#   cross-module visual consistency notes.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: INPUT_MODEL_PLAN
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Not directly implemented here, but master logs should later capture shared
#   keyboard/gamepad conventions and module input contracts.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: DISCOVERY_TO_ACTION_PIPELINE
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Shared pipeline target:
#     discover -> classify -> compare -> decide -> present -> log -> learn -> improve
# - Bootstrap exists so future tools have known destinations for each phase.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: RULE_CONFIDENCE_MODEL
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Future rule gatherers should distinguish:
#     probable rule
#     repeated rule
#     canonical/global rule
# - Bootstrap does not infer rules; it only prepares the storage locations.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: NOISE_PATTERNS_AND_COUNTERMEASURES
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Common failure mode: too much scattered notation without known authority.
# - Countermeasure: seed dedicated files for rules/help/notation/index early.
# - Common failure mode: accidental destructive cleanup.
# - Countermeasure: create-only behavior and explicit summary output.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: FUTURE_SIDECAR_SPLIT_PLAN
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Heavy notation should increasingly live in .txt sidecars rather than only
#   inside executable scripts.
# - Bootstrap seeds that sidecar-first direction at the master level.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: AI_COLLABORATION_PROTOCOL
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Future AI should read master logs before proposing repeated architecture.
# - Future AI should append, not erase, when adding worthwhile context.
# - Future AI should treat starter files as authoritative anchors, not rigid
#   prisons; they may be expanded carefully.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: SAFE_EVOLUTION_RULES
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Prefer additive changes.
# - Avoid automatic migration unless explicitly approved.
# - Avoid hidden filesystem edits outside declared root.
# - Surface what was created versus what already existed.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: MODULE_ORCHESTRATION_GOALS
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Future orchestration tools may use master logs as shared memory between
#   modules, gatherers, patchers, scanners, and helpers.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: LESSONS_FROM_REAL_RUNS
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Re-running setup scripts happens often in iterative projects.
# - Safe idempotence is more valuable than aggressive automation.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: KNOWN_WEAK_ASSUMPTIONS
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Assumes filesystem permissions allow creation under the chosen root.
# - Assumes text files are acceptable initial authority containers.
# - Assumes user still prefers the declared master log root.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: UPGRADE_CANDIDATES
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Add optional report file emission.
# - Add starter canonical rule registry.
# - Add optional module summary template generation.
# - Add optional readme for each subfolder with richer examples.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: THEME_SYSTEM_PLAN
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Not directly implemented here.
# - Master notation should later preserve shared theme definitions and color
#   conventions that affect multiple tools.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: GLOBAL_RULE_CANONICALIZATION_PLAN
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Future gatherers should compare repeated statements across module logs and
#   promote true global rules into rules/ when confidence is high.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: MASTER_LOG_ARCHITECTURE
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - This script bootstraps the architecture, but does not populate it with all
#   project knowledge. It creates the minimum stable skeleton.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: NOTATION_HARVEST_PLAN
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Future tools may scan modules/subfolders and extract notation candidates
#   into master summaries without modifying source modules.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: CANONICAL_RULE_SOURCES
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Likely future sources:
#     master rules files
#     important sidecars
#     repeated user directives
#     module-local logs with repeated cross-module patterns
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: RULE_SCOPE_MODEL
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Rule scopes expected later:
#     global project rule
#     family/module-type rule
#     single-module rule
#     temporary run/session note
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: MODULE_DEPENDENCY_MAP
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Not directly implemented here.
# - Master logs should later document which modules rely on shared GUI,
#   gamepad, theme, windowing, and logging conventions.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: SHARED_SERVICE_CANDIDATES
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Potential shared services:
#     rule gatherer
#     notation harvester
#     theme helper
#     clock/date helper
#     gamepad integration helper
#     path/index helper
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: GUI_STANDARDIZATION_PLAN
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Master notation should later store shared menu/window appearance rules so
#   modules converge visually instead of drifting.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: WINDOW_CHROME_PLAN
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Reserved for future shared notes on close/minimize/maximize style,
#   title-bar layout, and desktop-mode behavior.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: CLOCK_DATE_INTEGRATION_PLAN
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Reserved for future shared notes on clock/date bars and timing displays.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: GAMEPAD_INTEGRATION_CONTRACT
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Reserved for future shared rules on gamepad navigation, focus behavior,
#   emergency exit handling, and module consistency.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: THEME_ENGINE_CONTRACT
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Reserved for future shared rules on theme identifiers, palette authority,
#   and cross-module theme compatibility.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: LOG_TXT_TRANSPORT_RULES
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Prefer .txt sidecars for transport and upload friendliness.
# - Avoid plain .log as the primary collaboration transport format.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: AI_HANDOFF_MINIMUMS
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Important handoffs should include path, purpose, version line, current
#   goals, known decisions, and rule reminders.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: NOTATION_EXTRACTION_CRITERIA
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Worth extracting when it is repeated, project-wide, architectural,
#   safety-related, or useful to future AI across chats.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: PROMOTE_TO_MASTER_LOG_RULES
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Promote when a note becomes clearly cross-module, stable, and repeated.
# - Keep local if it remains module-specific or experimental.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: FUTURE_TOOLCHAIN_IDEAS
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Rule gatherer -> canonicalizer -> harvester -> reporter pipeline.
# - Future dashboard for master log health.
# - Future diff/compare tools for rule drift across modules.
# =============================================================================

# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: CROSS_MODULE_AUTONOMY_PLAN
# STATUS: ACTIVE
# APPEND_ONLY: YES
# -----------------------------------------------------------------------------
# - Goal is for modules to keep local autonomy while sharing stable global
#   standards through master logs.
# =============================================================================


DEFAULT_ROOT = Path("/userdata/system/ultramode/um_master_logs")
SUBDIRS = (
    "index",
    "rules",
    "help",
    "notation",
    "runtime",
    "reports",
    "archive",
    "modules",
)


@dataclass
class ResultTracker:
    created_dirs: list[Path] = field(default_factory=list)
    existing_dirs: list[Path] = field(default_factory=list)
    created_files: list[Path] = field(default_factory=list)
    existing_files: list[Path] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")


def banner_line() -> str:
    return "=" * 79


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bootstrap UltraMode master log folders and starter files safely."
    )
    parser.add_argument(
        "--root",
        default=str(DEFAULT_ROOT),
        help=f"Master log root path (default: {DEFAULT_ROOT})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without writing anything.",
    )
    return parser


def header_block(title: str, path_text: str, purpose_lines: Iterable[str]) -> str:
    purpose = "\n".join(f"  - {line}" for line in purpose_lines)
    return (
        f"===============================================================================\n"
        f"ULTRAMODE MASTER LOG FILE\n"
        f"===============================================================================\n"
        f"TITLE:         {title}\n"
        f"PATH:          {path_text}\n"
        f"STATUS:        ACTIVE STARTER FILE\n"
        f"RULE:          APPEND-ONLY. NEVER DELETE HISTORY. ONLY APPEND.\n"
        f"CREATED_BY:    um_master_logs_bootstrap_v1.py\n"
        f"CREATED_AT:    {now_stamp()}\n"
        f"===============================================================================\n"
        f"PURPOSE:\n{purpose}\n"
        f"===============================================================================\n\n"
    )


def section_block(category: str, lines: Iterable[str]) -> str:
    body = "\n".join(f"- {line}" for line in lines)
    return (
        f"[{category}]\n"
        f"{body}\n\n"
    )


def starter_file_contents(root: Path) -> dict[Path, str]:
    return {
        root / "rules" / "global_ai_rules.txt": (
            header_block(
                "Global AI Rules",
                str(root / "rules" / "global_ai_rules.txt"),
                [
                    "Project-wide AI collaboration rules.",
                    "Canonical place for repeated stable user preferences and workflow law.",
                    "Should collect only truly global rules, not one-off local notes.",
                ],
            )
            + section_block(
                "RULES", [
                    "Keep worthwhile rules concise, clear, and stable.",
                    "Prefer append-only additions over destructive rewrites.",
                    "When promoting a rule here, note why it is global.",
                ])
            + section_block(
                "PROMOTION_NOTES", [
                    "Promote repeated cross-module rules from local logs when confidence is high.",
                    "Keep uncertain or module-specific rules in local/module notation until proven global.",
                ])
            + section_block(
                "FUTURE_APPENDS", [
                    "Append future global rules below this line.",
                ])
        ),
        root / "help" / "master_logs_help.txt": (
            header_block(
                "Master Logs Help",
                str(root / "help" / "master_logs_help.txt"),
                [
                    "Explain what each master log folder is for.",
                    "Help future AI and humans navigate the architecture quickly.",
                ],
            )
            + section_block(
                "FOLDER_MAP", [
                    "index/ = where things are",
                    "rules/ = project-wide law / AI rules / script rules",
                    "help/ = usage/help authority",
                    "notation/ = ideas / architecture / thinktank",
                    "runtime/ = runtime/live evidence",
                    "reports/ = generated outputs",
                    "archive/ = snapshots and old exports",
                    "modules/ = future module summaries or mirrored summaries",
                ])
            + section_block(
                "USAGE_NOTES", [
                    "Prefer .txt for sidecar transport and uploads.",
                    "Preserve append-only history where practical.",
                ])
        ),
        root / "notation" / "master_notation.txt": (
            header_block(
                "Master Notation",
                str(root / "notation" / "master_notation.txt"),
                [
                    "Central thinktank file for project-wide ideas, goals, and architecture intent.",
                    "Should preserve evolving cross-module concepts.",
                ],
            )
            + section_block(
                "DISCOVERY_TO_ACTION_PIPELINE", [
                    "discover -> classify -> compare -> decide -> present -> log -> learn -> improve",
                ])
            + section_block(
                "SEED_CATEGORIES", [
                    "CHANGELOG",
                    "ANALYSIS",
                    "GOALS",
                    "IDEAS",
                    "AI_THINKTANK",
                    "ARCHITECTURE_INTENT",
                    "CROSS_MODULE_RELATIONSHIPS",
                    "SHARED_UI_RULES",
                    "INPUT_MODEL_PLAN",
                    "RULE_CONFIDENCE_MODEL",
                    "NOISE_PATTERNS_AND_COUNTERMEASURES",
                    "SAFE_EVOLUTION_RULES",
                    "MODULE_ORCHESTRATION_GOALS",
                ])
            + section_block(
                "FUTURE_APPENDS", [
                    "Append new architecture notes and project-wide ideas below this line.",
                ])
        ),
        root / "index" / "master_log_index.txt": (
            header_block(
                "Master Log Index",
                str(root / "index" / "master_log_index.txt"),
                [
                    "Directory map for master log authorities.",
                    "Quick index for where major project knowledge lives.",
                ],
            )
            + section_block(
                "INDEX", [
                    "rules/global_ai_rules.txt -> canonical global AI rules",
                    "help/master_logs_help.txt -> architecture usage help",
                    "notation/master_notation.txt -> project-wide thinktank",
                    "runtime/runtime_readme.txt -> runtime log guidance",
                    "reports/reports_readme.txt -> report storage guidance",
                    "archive/archive_readme.txt -> archive guidance",
                    "modules/modules_index.txt -> future module summary map",
                ])
        ),
        root / "runtime" / "runtime_readme.txt": (
            header_block(
                "Runtime Folder Guidance",
                str(root / "runtime" / "runtime_readme.txt"),
                [
                    "Explain what belongs in runtime/.",
                    "Keep runtime evidence distinct from long-term rules and notation.",
                ],
            )
            + section_block(
                "RUNTIME_NOTES", [
                    "Use for live logs, temporary evidence, and run outputs.",
                    "Do not treat runtime noise as canonical rule truth by default.",
                ])
        ),
        root / "reports" / "reports_readme.txt": (
            header_block(
                "Reports Folder Guidance",
                str(root / "reports" / "reports_readme.txt"),
                [
                    "Explain what belongs in reports/.",
                    "Store generated summaries, audit outputs, and extraction reports here.",
                ],
            )
            + section_block(
                "REPORT_NOTES", [
                    "Use for generated reports and summaries.",
                    "Prefer timestamped filenames for future generated report outputs.",
                ])
        ),
        root / "archive" / "archive_readme.txt": (
            header_block(
                "Archive Folder Guidance",
                str(root / "archive" / "archive_readme.txt"),
                [
                    "Explain what belongs in archive/.",
                    "Preserve historical snapshots without mixing them into current authority files.",
                ],
            )
            + section_block(
                "ARCHIVE_NOTES", [
                    "Use for old snapshots, exports, and archived states.",
                    "Do not automatically delete older items without explicit approval.",
                ])
        ),
        root / "modules" / "modules_index.txt": (
            header_block(
                "Modules Index",
                str(root / "modules" / "modules_index.txt"),
                [
                    "Future map of module summaries, mirrored rules, and cross-module notes.",
                    "Acts as a placeholder anchor for later module-level harvesting.",
                ],
            )
            + section_block(
                "MODULE_SUMMARY_PLAN", [
                    "Future module summaries may live in subfolders under modules/.",
                    "Use this file to map which modules have been harvested or summarized.",
                ])
        ),
    }


def ensure_dir(path: Path, dry_run: bool, tracker: ResultTracker) -> None:
    try:
        if path.exists():
            tracker.existing_dirs.append(path)
            return
        if dry_run:
            tracker.created_dirs.append(path)
            return
        path.mkdir(parents=True, exist_ok=True)
        tracker.created_dirs.append(path)
    except Exception as exc:  # pragma: no cover - defensive path
        tracker.errors.append(f"DIR ERROR: {path} -> {exc}")


def ensure_file(path: Path, content: str, dry_run: bool, tracker: ResultTracker) -> None:
    try:
        if path.exists():
            tracker.existing_files.append(path)
            return
        if dry_run:
            tracker.created_files.append(path)
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        tracker.created_files.append(path)
    except Exception as exc:  # pragma: no cover - defensive path
        tracker.errors.append(f"FILE ERROR: {path} -> {exc}")


def print_verification(root: Path, dry_run: bool) -> None:
    print(banner_line())
    print("ULTRAMODE MASTER LOGS BOOTSTRAP")
    print(banner_line())
    print(f"Timestamp : {now_stamp()}")
    print(f"Mode      : {'DRY RUN' if dry_run else 'LIVE CREATE'}")
    print(f"Root Path : {root}")
    print("Policy    : create missing only; never overwrite/delete existing logs")
    print(banner_line())


def print_list(label: str, items: list[Path]) -> None:
    print(f"{label}: {len(items)}")
    for item in items:
        print(f"  - {item}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    root = Path(args.root).expanduser()
    dry_run = bool(args.dry_run)
    tracker = ResultTracker()

    print_verification(root, dry_run)

    ensure_dir(root, dry_run, tracker)
    for subdir in SUBDIRS:
        ensure_dir(root / subdir, dry_run, tracker)

    for path, content in starter_file_contents(root).items():
        ensure_file(path, content, dry_run, tracker)

    print_list("Created directories", tracker.created_dirs)
    print_list("Existing directories", tracker.existing_dirs)
    print_list("Created files", tracker.created_files)
    print_list("Existing files", tracker.existing_files)

    print(banner_line())
    if tracker.errors:
        print(f"Errors: {len(tracker.errors)}")
        for err in tracker.errors:
            print(f"  - {err}")
        print("RESULT: COMPLETED WITH ERRORS")
        print(banner_line())
        return 1

    print("Errors: 0")
    print("RESULT: SUCCESS")
    if dry_run:
        print("NOTE: No filesystem changes were made because --dry-run was used.")
    print(banner_line())
    return 0


if __name__ == "__main__":
    sys.exit(main())
