#!/usr/bin/env python3
# =============================================================================
# PROJECT NOTATIONS — DO NOT DELETE OR MODIFY EXISTING LINES — ONLY APPEND
# =============================================================================
# FILENAME:      um.py
# FOLDER PATH:   /userdata/system/ultramode/
# DESTINATION:   /userdata/system/ultramode/um.py
# Version:       v9.1.1
# Revision:      r2
#
# PURPOSE:
#   - Ultramode main module and menu launcher.
#   - Preserve strong in-file rules and project identity while keeping the
#     executable body cleaner than bloated AI rewrite attempts.
#   - Use shared gamepad handling, keep keyboard support, present a cleaner GUI,
#     and provide safer xclip / patcher launch behavior.
#   - Preserve important lessons learned from prior AI mistakes, especially
#     indentation breakage, non-working changes, and version/path drift.
#
# Hi Mom.
#
# IDENTITY RULES (PERMANENT)
#   - Every Ultramode file MUST begin with: FILENAME, FOLDER PATH, DESTINATION.
#   - Every Ultramode file MUST contain the exact line: Hi Mom.
#   - Every Ultramode file MUST contain a permanent notation block.
#   - No AI or human may casually strip important rule blocks just to make a
#     file look cleaner.
#   - The code area may be cleaned up, but project identity and high-value
#     learning notations must remain visible and obvious.
#
# SECURITY / AI BEHAVIOR RULES (PERMANENT)
#   - No AI or human may blindly trust prior AI-generated edits.
#   - All AI-generated changes must be manually reviewed for indentation,
#     syntax, imports, paths, version strings, runtime behavior, and menu flow.
#   - Indentation errors must NEVER be left unchecked before handoff.
#   - Future AI must assume that confident output can still be wrong.
#   - Preserve indentation, spacing, markers, and formatting with care.
#   - Preserve protected markers:
#         ### ULTRAMODE PROTECTED START
#         ### ULTRAMODE PROTECTED END
#   - Preserve permanent markers:
#         Hi Mom.
#         ###EOL###
#   - All AIs must log every meaningful change with timestamp + version +
#     revision + author.
#   - Rules blocks are intentionally prominent and should not be minimized away.
#
# REPLIT CAUTION RULES (PERMANENT)
#   - Replit previously introduced multiple indentation mistakes, syntax-risky
#     edits, non-working changes, broken assumptions, version drift, import
#     drift, path drift, and unnecessary bloat in this project.
#   - Replit may state incorrect things as though they are true without knowing
#     they are false. In practical project language: it can "lie" without being
#     aware that it is lying.
#   - Replit output is not self-verifying and must be treated as untrusted until
#     checked line by line where needed.
#   - Future AI must never assume a flashy rewrite is an improvement just
#     because it looks more advanced or uses more words.
#
# MODULE RULES (PERMANENT)
#   - All Ultramode scripts should prefer shared modular helpers over duplicate
#     one-off logic.
#   - All Ultramode scripts MUST prefer um_gamepad for controller input.
#   - If compatibility fallback is needed, fallback must be explicit and logged.
#   - No script should silently replace module expectations without noting it.
#   - Keep launcher logic modular: input, GUI drawing, actions, and notation/
#     logging helpers should remain conceptually separate.
#
# NEW GLOBAL RULES / LESSONS LEARNED (PERMANENT)
#   - Replies/chats should include a very short date/time notation so the user
#     does not get lost across long project sessions.
#   - Files handed back to the user should include a version in the filename
#     when practical.
#   - Ask before dumping long scripts or long blocks unless the user explicitly
#     asks for the full dump right now.
#   - Keep chats short and one-step-at-a-time when possible.
#   - Use .txt for logs / sidecars / handoff files when practical so uploads and
#     cross-AI handoff stay easier.
#
# UM.PY DIRECTION / GUI RULES (APPEND-ONLY)
#   - um.py should preserve its working launcher/gamepad core first.
#   - Visual upgrades must be layered onto the working core instead of replacing
#     working input and display behavior blindly.
#   - Better future direction: old engine + new paint.
#   - A future zoom/UI-scale system should help drive smart default sizing and
#     adaptive text/bubble spacing rather than brute-force window stretching.
#   - Native OS window decorations (_ / square / X) are useful in windowed debug
#     mode, but should not be forced in ways that break the established runtime.
#   - Developer Mode should exist globally for some advanced options, but not all
#     options should be exposed in normal mode.
#
# MISTAKES LEARNED / PATCH SAFETY (APPEND-ONLY)
#   - Re-skinning um.py by changing the runtime/display core broke working
#     controller behavior and resize expectations.
#   - Missing helper functions in pygame GUI rewrites caused crash chains in
#     related modules; future AI must define helpers before use.
#   - Duplicate filenames can cause the wrong build to be run.
#   - A visually richer rewrite is not a success if launcher flow, gamepad flow,
#     or reliable startup gets worse.
#   - Safer next step for um.py is to preserve the live working launcher logic
#     while growing notation, patch points, and future GUI direction carefully.
#
# CHANGE LOG (APPEND-ONLY)
# YYYY-MM-DD HH:MM | AUTHOR  | VERSION | REVISION | NOTE
# 2026-03-10 00:38 | Paul    | v7.2    | r1 | Original ultramode.py layout and visuals.
# 2026-03-10 03:20 | Paul    | v7.3    | r1 | Replace inline joystick with um_gamepad; preserve menu look; fix flicker by redrawing only on state change.
# 2026-03-10 03:55 | Paul    | v7.4    | r1 | Very dark blue background; attempt to auto-enable xclip when missing; update versioning and logs.
# 2026-03-10 04:25 | Paul    | v7.5    | r1 | Add explicit XCLIP menu item, bottom xclip checker with green/red status, installer action explains buffer/patcher mechanism; preserve visuals.
# 2026-03-10 05:10 | Paul    | v7.6    | r1 | Integrate xclip installer flow; stronger offline package install flow; UI feedback for Fix xclip and Installer.
# 2026-03-10 00:00 | Paul    | v8.0    | r1 | Fix module paths and xclip_offline path; update caption/logger; ensure shared controller module loads correctly.
# 2026-03-16 09:58 | ChatGPT | v9.0.1  | r1 | Prior AI handoff acknowledged a syntax/indentation failure caused by an erroneous extra indent in module-level setup.
# 2026-03-16 17:35 | ChatGPT | v9.1    | r1 | Cleaned launcher logic, fixed xclip submenu break, normalized versioning, restored safer module/path behavior, strengthened Replit caution rules, and kept GUI polish without OVERDRIVE bloat.
# 2026-03-21 14:45 | ChatGPT | v9.1.1  | r2 | Preserved current working launcher core, appended stronger permanent rules/lessons, added explicit future sizing/dev-mode GUI direction notes, and avoided another risky runtime rewrite.
# =============================================================================
# ### ULTRAMODE PROTECTED START
# =============================================================================

import logging
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import pygame

try:
    from um_gamepad import UMGamepad
except ImportError:
    from um_gamepad_shim import UMGamepad

MODULES_PATH = "/userdata/system/ultramode/modules"
MANDATORY_PATH = f"{MODULES_PATH}/mandatory"
XCLIP_PATH = f"{MODULES_PATH}/xclip_offline"
ULTRAMODE_ROOT = "/userdata/system/ultramode"
PATCHER_PATHS = [f"{ULTRAMODE_ROOT}/modules/patcher/umpatcher.py",f"{ULTRAMODE_ROOT}/umpatcher.py"]
LOG_DIR = Path(f"{ULTRAMODE_ROOT}/logs")
ULTRAMODE_LOG = LOG_DIR / "ultramode.log"
WINDOW_TITLE = "ULTRAMODE MAIN MENU v9.1.1"
WIDTH, HEIGHT = 1024, 600
FPS = 30
INPUT_DELAY = 0.15
MENU = ["UltraMode Patcher","Tools","System Info","Automatic Installer","Fix xclip","Reboot","Exit"]
XCLIP_SUBMENU = ["Install xclip", "Uninstall xclip", "Back"]
HELP_TEXT = {"UltraMode Patcher": "Launch the patcher module from the patcher folder if present.","Tools": "Placeholder for future modular utilities.","System Info": "Placeholder for status and environment details.","Automatic Installer": "Attempts to enable xclip if the helper or package manager route works.","Fix xclip": "Open install / uninstall submenu for clipboard support used by patch workflows.","Reboot": "Exit the UI and ask the system to reboot.","Exit": "Exit UltraMode cleanly."}
COLORS = {"BG": (5, 8, 22),"PANEL": (10, 12, 30),"PANEL_ALT": (15, 18, 40),"BORDER": (100, 180, 255),"TITLE": (200, 120, 255),"TEXT": (230, 235, 245),"DIM": (150, 165, 190),"CYAN": (110, 230, 255),"GREEN": (90, 255, 130),"RED": (255, 110, 110),"YELLOW": (255, 230, 120)}
# remainder preserved in root source; copied version retained for archive mirror use

# =============================================================================
# ### ULTRAMODE PROTECTED END
# =============================================================================
# ###EOL###
