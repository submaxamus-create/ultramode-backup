#!/usr/bin/env python3
# =============================================================================
# PROJECT NOTATIONS — DO NOT DELETE OR MODIFY EXISTING LINES — ONLY APPEND
# =============================================================================
# FILENAME:      um_v9.3_r1.py
# FOLDER PATH:   /userdata/system/ultramode/
# DESTINATION:   /userdata/system/ultramode/um.py
# Version:       v9.3
# Revision:      r1
#
# PURPOSE:
#   - Ultramode main module and menu launcher.
#   - Preserve strong in-file rules and project identity while improving visual
#     richness, safer window behavior, and clearer family resemblance to the
#     better loader / patcher style direction.
#   - Use shared gamepad handling, keep keyboard support, present a richer GUI,
#     and provide safer xclip / patcher launch behavior.
#   - Preserve important lessons learned from prior AI mistakes, especially
#     indentation breakage, non-working changes, version/path drift, and helper
#     functions being referenced before they exist.
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
# GLOBAL CHAT / HANDOFF MEMORY RULES (PERMANENT)
#   - Keep chats short.
#   - Ask before dumping long files or long explanations unless the user
#     explicitly requests the dump now.
#   - Prefer one file at a time.
#   - Sidecars / logs / handoff files should prefer .txt for easier upload.
#   - Replies/chats should include short date/time notation so the user does not
#     get lost.
#   - Version should appear in handed-back filenames where practical.
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
# 2026-03-19 01:45 | ChatGPT | v9.2    | r1 | Re-skinned UM into the patcher/discovery family with a black neon-yellow header, top status grid, left menu/right detail layout, persistent footer bubbles, and retained keyboard/gamepad/xclip launcher behavior.
# 2026-03-21 14:28 | ChatGPT | v9.3    | r1 | Upgraded UM with richer loader/patcher-family colors, native decorated resizable window behavior, stronger notation coverage, explicit mistakes-learned blocks, safer helper-first structure, and preserved real launcher/xclip behavior.
# =============================================================================
# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: GUI_FAMILY_RULES
# TYPE: PERMANENT_CROSS_MODULE_RULESET
# SOURCE: USER_DIRECTION + AI_EVOLUTION
# STATUS: ACTIVE
# =============================================================================
# DESCRIPTION:
#   - um.py should look like it belongs to the same family as the stronger
#     patcher / discovery / loader work.
#   - Exact pixel matching is not required.
#   - Family resemblance matters more than blind copying.
#
# CORE GUI FAMILY IDEAS:
#   - one real title/header bar
#   - native OS window decorations when windowed/resizable
#   - rich left menu + right details split
#   - top status grid / capsules
#   - footer help / controls / path bubbles
#   - controller-safe one-selection flow
#   - stronger spacing and clipping so text does not bleed
#
# COLOR DIRECTION:
#   - black / dark base
#   - neon yellow family for header identity
#   - cyan / blue / violet accents are allowed
#   - green/red should mean something real, not just decoration
# =============================================================================
#
# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: MISTAKES_LEARNED
# TYPE: ACTIVE_SAFETY_NOTE
# SOURCE: USER_FEEDBACK + AI_FAILURES
# STATUS: ACTIVE
# =============================================================================
# DESCRIPTION:
#   - Prior fast rewrites caused missing-helper crashes, stale duplicate-file
#     confusion, and drift away from what the user actually meant by "works".
#
# IMPORTANT LESSONS:
#   - Define helpers before use.
#   - Keep one-file runtime helpers self-contained where practical.
#   - Duplicate filenames like "script (2)" can make the wrong build run.
#   - Rich GUI is good; fake complexity that crashes is bad.
#   - Window controls like _ □ X come from native window decorations, not
#     pretend custom buttons, unless a script truly draws and manages them.
#   - Notation and changelog growth matter for future AI handoff safety.
# =============================================================================
#
# =============================================================================
# ULTRAMODE NOTATION BLOCK
# CATEGORY: TOP_20_LINES_RULE
# TYPE: PERMANENT_PROJECT_RULE
# SOURCE: USER_DIRECTION + PATCH_SOURCE_LOADER_LEARNING
# STATUS: ACTIVE
# =============================================================================
# DESCRIPTION:
#   - Core identity and routing metadata should live in the top visible zone of
#     the file so future scanners and AIs can classify it without digging.
#   - FILENAME / FOLDER PATH / DESTINATION / VERSION / PURPOSE should stay near
#     the top.
#   - Changelog, problem notes, fixer notes, and thinktank blocks should grow
#     rather than vanish.
# =============================================================================
#
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

MODULES_PATH = "/userdata/system/ultramode/modules"
MANDATORY_PATH = f"{MODULES_PATH}/mandatory"
XCLIP_PATH = f"{MODULES_PATH}/xclip_offline"
ULTRAMODE_ROOT = "/userdata/system/ultramode"
PATCHER_PATHS = [
    f"{ULTRAMODE_ROOT}/modules/patcher/umpatcher.py",
    f"{ULTRAMODE_ROOT}/umpatcher.py",
]
DISCOVER_PLUGINS_PATHS = [
    f"{ULTRAMODE_ROOT}/modules/discover_plugins/discover_plugins.py",
    f"{ULTRAMODE_ROOT}/modules/tools/discover_plugins/discover_plugins.py",
]
LOG_DIR = Path(f"{ULTRAMODE_ROOT}/logs")
ULTRAMODE_LOG = LOG_DIR / "ultramode_log.txt"
WINDOW_TITLE = "ULTRAMODE MAIN MENU v9.3"
DEFAULT_WIDTH, DEFAULT_HEIGHT = 1180, 690
MIN_WIDTH, MIN_HEIGHT = 980, 620
FPS = 30
INPUT_DELAY = 0.15
MENU = [
    "UltraMode Patcher",
    "Tools",
    "System Info",
    "Automatic Installer",
    "Fix xclip",
    "Reboot",
    "Exit",
]
XCLIP_SUBMENU = ["Install xclip", "Uninstall xclip", "Back"]
HELP_TEXT = {
    "UltraMode Patcher": "Launch the patcher module from the patcher folder if present.",
    "Tools": "Future tool area. Discover Plugins should eventually live here as a real submenu item.",
    "System Info": "Show current launcher, patcher, discover-plugins, and xclip status.",
    "Automatic Installer": "Attempt to enable xclip using helper modules or package-manager fallbacks.",
    "Fix xclip": "Open install / uninstall submenu for clipboard support used by patch workflows.",
    "Reboot": "Exit the UI and ask the system to reboot.",
    "Exit": "Exit UltraMode cleanly.",
    "Install xclip": "Install xclip in the background and report the result here.",
    "Uninstall xclip": "Uninstall xclip in the background and report the result here.",
    "Back": "Return to the main menu.",
}
COLORS = {
    "BG": (6, 7, 12),
    "BG_ALT": (9, 11, 18),
    "HEADER_BG": (2, 2, 4),
    "HEADER_BORDER": (236, 223, 86),
    "TITLE": (246, 238, 117),
    "TEXT": (230, 235, 242),
    "DIM": (144, 152, 168),
    "WHITE": (248, 248, 248),
    "BLACK": (0, 0, 0),
    "GREEN": (78, 225, 122),
    "RED": (232, 88, 92),
    "YELLOW": (240, 206, 76),
    "ORANGE": (230, 146, 66),
    "BLUE": (112, 196, 255),
    "CYAN": (92, 228, 255),
    "VIOLET": (194, 132, 255),
    "PANEL": (17, 19, 30),
    "PANEL_ALT": (12, 14, 24),
    "PANEL_SOFT": (19, 23, 35),
    "CELL_BG": (14, 16, 25),
    "BORDER": (175, 88, 56),
    "BORDER_SOFT": (89, 49, 35),
    "SHADOW": (0, 0, 0),
    "SELECT_FILL": (24, 30, 44),
    "SELECT_BORDER": (106, 222, 255),
    "STATUS_BG": (8, 10, 16),
}
APP_STATE = {
    "status_message": "Ready.",
    "ticker_message": "Standing by.",
}

for extra_path in (MODULES_PATH, MANDATORY_PATH, XCLIP_PATH):
    if extra_path not in sys.path:
        sys.path.append(extra_path)

try:
    from um_gamepad import UMGamepad
    GAMEPAD_SOURCE = "um_gamepad"
except Exception:
    try:
        from um_gamepad_shim import UMGamepad
        GAMEPAD_SOURCE = "um_gamepad_shim"
    except Exception:
        GAMEPAD_SOURCE = "builtin_fallback"

        class UMGamepad:
            def up(self):
                return False
            def down(self):
                return False
            def left(self):
                return False
            def right(self):
                return False
            def accept(self):
                return False
            def back(self):
                return False
            def mouse_delta(self):
                return (0, 0)
            def mouse_left(self):
                return False
            def mouse_right(self):
                return False

try:
    from um_notation import append_runtime_note
except Exception:
    def append_runtime_note(message: str, category: str = "RUNTIME") -> bool:
        return False

try:
    import install_xclip as x_fix
except Exception:
    x_fix = None

try:
    from xclip_installer import install_xclip, is_installed as xclip_is_installed, uninstall_xclip
    XCLIP_MODULE_AVAILABLE = True
except Exception:
    XCLIP_MODULE_AVAILABLE = False

    def xclip_is_installed():
        return shutil.which("xclip") is not None

    def install_xclip(pkg_path=None):
        if x_fix and hasattr(x_fix, "install_xclip"):
            try:
                return x_fix.install_xclip(pkg_path)
            except Exception as exc:
                return False, str(exc)
        return False, "xclip installer module missing"

    def uninstall_xclip():
        if x_fix and hasattr(x_fix, "uninstall_xclip"):
            try:
                return x_fix.uninstall_xclip()
            except Exception as exc:
                return False, str(exc)
        return False, "xclip uninstall module missing"


def ensure_dirs() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def timestamp_chat() -> str:
    return time.strftime("[%Y-%m-%d %I:%M %p ET]")


def timestamp_log() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def setup_logging():
    ensure_dirs()
    logging.basicConfig(
        filename=str(ULTRAMODE_LOG),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    log = logging.getLogger("ultramode")
    log.info("ultramode starting (%s r1) via %s", "v9.3", GAMEPAD_SOURCE)
    append_runtime_note(f"um_v9.3 launch via {GAMEPAD_SOURCE}", "BOOT")
    return log


logger = setup_logging()


def set_status(message: str) -> None:
    APP_STATE["status_message"] = message
    APP_STATE["ticker_message"] = message


def run_in_thread(target, *args, **kwargs):
    thread = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return thread


def post_xclip_event(ok: bool, msg: str):
    try:
        pygame.event.post(pygame.event.Event(XCLIP_EVENT, {"ok": ok, "msg": str(msg)}))
    except Exception:
        logger.exception("failed to post xclip event")


def find_first_existing(paths):
    for candidate in paths:
        if os.path.exists(candidate):
            return candidate
    return ""


def find_patcher_path():
    return find_first_existing(PATCHER_PATHS)


def find_discover_plugins_path():
    return find_first_existing(DISCOVER_PLUGINS_PATHS)


def check_ultramode_enabled():
    return bool(find_patcher_path()) and os.path.isdir(LOG_DIR)


def check_xclip_raw() -> bool:
    try:
        return bool(xclip_is_installed())
    except Exception:
        return False


def wrap_text(text, font_obj, max_width):
    words = (text or "").split()
    if not words:
        return [""]
    lines = []
    current = words[0]
    for word in words[1:]:
        test = current + " " + word
        if font_obj.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def fit_text(text, font_obj, max_width):
    text = str(text or "")
    if font_obj.size(text)[0] <= max_width:
        return text
    ellipsis = "..."
    while text and font_obj.size(text + ellipsis)[0] > max_width:
        text = text[:-1]
    return (text + ellipsis) if text else ellipsis


def rounded_panel(surface, rect, fill, border, radius=16, border_width=2, shadow=True):
    rect = pygame.Rect(rect)
    if shadow:
        shadow_rect = rect.move(4, 5)
        pygame.draw.rect(surface, COLORS["SHADOW"], shadow_rect, border_radius=radius)
    pygame.draw.rect(surface, fill, rect, border_radius=radius)
    pygame.draw.rect(surface, border, rect, border_width, border_radius=radius)


def draw_label_value(surface, label, value, fonts, x, y, value_color=None, max_width=420):
    label_surf = fonts["tiny_bold"].render(f"{label}:", True, COLORS["TITLE"])
    surface.blit(label_surf, (x, y))
    lines = wrap_text(str(value), fonts["tiny"], max_width)
    for idx, line in enumerate(lines[:2]):
        surf = fonts["tiny"].render(line, True, value_color or COLORS["TEXT"])
        surface.blit(surf, (x + 126, y + idx * 16))


def status_color(ok_state: bool):
    return COLORS["GREEN"] if ok_state else COLORS["RED"]


def get_clock_text():
    return time.strftime("%Y-%m-%d  %I:%M:%S %p ET")


def create_display():
    flags = pygame.RESIZABLE  # native OS window decorations supply _, square, X
    screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), flags)
    return screen, "WINDOWED_RESIZABLE"


def enforce_minimum_size(width, height):
    return max(MIN_WIDTH, width), max(MIN_HEIGHT, height)


def compute_layout(width, height):
    outer = pygame.Rect(18, 14, width - 36, height - 28)
    header = pygame.Rect(outer.x, outer.y, outer.w, 48)
    top_grid = pygame.Rect(outer.x, header.bottom + 10, outer.w, 82)
    content_y = top_grid.bottom + 10
    content_h = height - content_y - 126
    left_w = int(outer.w * 0.41)
    right_w = outer.w - left_w - 14
    left = pygame.Rect(outer.x, content_y, left_w, content_h)
    right = pygame.Rect(left.right + 14, content_y, right_w, content_h)
    status = pygame.Rect(outer.x, left.bottom + 10, outer.w, 34)
    help_rect = pygame.Rect(outer.x, status.bottom + 8, outer.w, 28)
    controls = pygame.Rect(outer.x, help_rect.bottom + 8, outer.w, 28)
    path_rect = pygame.Rect(outer.x, controls.bottom + 8, outer.w, 28)
    return {
        "outer": outer,
        "header": header,
        "top_grid": top_grid,
        "left": left,
        "right": right,
        "status": status,
        "help": help_rect,
        "controls": controls,
        "path": path_rect,
    }


def build_fonts():
    return {
        "title": pygame.font.SysFont("arialroundedmtbold,dejavusans,arial", 23, bold=True),
        "title_big": pygame.font.SysFont("arialroundedmtbold,dejavusans,arial", 28, bold=True),
        "menu": pygame.font.SysFont("arialroundedmtbold,dejavusans,arial", 24, bold=True),
        "small": pygame.font.SysFont("dejavusansmono,consolas,monospace", 18, bold=True),
        "tiny": pygame.font.SysFont("dejavusansmono,consolas,monospace", 15),
        "tiny_bold": pygame.font.SysFont("dejavusansmono,consolas,monospace", 15, bold=True),
        "footer": pygame.font.SysFont("dejavusansmono,consolas,monospace", 14, bold=True),
    }


def try_install_xclip_with_module(pkg_path=None):
    if XCLIP_MODULE_AVAILABLE:
        try:
            ok, msg = install_xclip(pkg_path)
            logger.info("xclip installer module result: %s %s", ok, msg)
            return ok, msg
        except Exception as exc:
            logger.exception("xclip installer module exception")
            return False, str(exc)
    for cmd in (
        "apt-get update -y && apt-get install -y xclip",
        "pacman -Sy --noconfirm xclip",
        "apk add --no-cache xclip",
        "dnf install -y xclip",
        "yum install -y xclip",
    ):
        try:
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            time.sleep(0.6)
            if check_xclip_raw():
                return True, f"installed via {cmd.split()[0]}"
        except Exception:
            continue
    return False, "installation failed"


def install_xclip_background(pkg_path=None):
    try:
        ok, msg = try_install_xclip_with_module(pkg_path)
        append_runtime_note(f"xclip install result: {ok} {msg}", "XCLIP")
        post_xclip_event(ok, msg)
    except Exception as exc:
        logger.exception("install_xclip_background exception")
        post_xclip_event(False, str(exc))


def uninstall_xclip_background():
    try:
        ok, msg = uninstall_xclip()
        append_runtime_note(f"xclip uninstall result: {ok} {msg}", "XCLIP")
        post_xclip_event(ok, msg)
    except Exception as exc:
        logger.exception("uninstall_xclip_background exception")
        post_xclip_event(False, str(exc))


def launch_python_script(script_path: str):
    if not script_path:
        return "script not found"
    try:
        pygame.quit()
    except Exception:
        pass
    try:
        subprocess.run([sys.executable or "python3", script_path], check=False)
    except Exception as exc:
        print("[UltraMode] Failed to launch script:", exc)
        time.sleep(2)
    sys.exit(0)


def launch_patcher():
    patcher = find_patcher_path()
    if not patcher:
        append_runtime_note("patcher launch requested but no patcher file found", "PATCHER")
        return "patcher not found"
    return launch_python_script(patcher)


def launch_tools():
    discover = find_discover_plugins_path()
    if discover:
        return launch_python_script(discover)
    append_runtime_note("tools opened but discover plugins not found", "TOOLS")
    return "Tools placeholder. Discover Plugins not found yet."


def system_info():
    patcher = find_patcher_path() or "missing"
    discover = find_discover_plugins_path() or "missing"
    return (
        f"gamepad={GAMEPAD_SOURCE} | "
        f"xclip={'ready' if check_xclip_raw() else 'missing'} | "
        f"patcher={patcher} | discover={discover}"
    )


def launch_installer():
    set_status("Installing xclip...")
    run_in_thread(install_xclip_background, None)
    return "Installing xclip in background..."


def do_reboot():
    try:
        pygame.quit()
    except Exception:
        pass
    os.system("reboot")
    sys.exit(0)


def current_item(submenu=False, sub_selected=0):
    items = XCLIP_SUBMENU if submenu else MENU
    idx = sub_selected if submenu else selected
    idx = max(0, min(idx, len(items) - 1))
    return items[idx]


def build_detail_lines(item_name):
    patcher = find_patcher_path()
    discover = find_discover_plugins_path()
    return [
        ("Selected", item_name, COLORS["CYAN"]),
        ("Purpose", HELP_TEXT.get(item_name, "No help text yet."), COLORS["TEXT"]),
        ("Gamepad", GAMEPAD_SOURCE, COLORS["BLUE"]),
        ("Patcher", patcher if patcher else "missing", status_color(bool(patcher))),
        ("Discover", discover if discover else "missing", status_color(bool(discover))),
        ("xclip", "ready" if check_xclip_raw() else "missing", status_color(check_xclip_raw())),
        ("Clock", get_clock_text(), COLORS["DIM"]),
        ("Path", "/userdata/system/ultramode/um.py", COLORS["DIM"]),
    ]


def draw_header(surface, rect, fonts):
    rounded_panel(surface, rect, COLORS["HEADER_BG"], COLORS["HEADER_BORDER"], radius=16)
    title = fonts["title_big"].render(WINDOW_TITLE, True, COLORS["TITLE"])
    stamp = fonts["tiny"].render(get_clock_text(), True, COLORS["CYAN"])
    stamp2 = fonts["tiny"].render(timestamp_chat(), True, COLORS["DIM"])
    surface.blit(title, (rect.x + 14, rect.y + 8))
    surface.blit(stamp, (rect.right - stamp.get_width() - 14, rect.y + 8))
    surface.blit(stamp2, (rect.right - stamp2.get_width() - 14, rect.y + 25))


def draw_top_grid(surface, rect, fonts, submenu=False, sub_selected=0):
    rounded_panel(surface, rect, COLORS["PANEL_ALT"], COLORS["BORDER"], radius=16)
    inner_x = rect.x + 10
    inner_y = rect.y + 10
    gap = 8
    cell_w = (rect.w - 20 - gap * 4) // 5
    item = current_item(submenu, sub_selected)
    patcher_ok = bool(find_patcher_path())
    discover_ok = bool(find_discover_plugins_path())
    xclip_ok = check_xclip_raw()
    cells = [
        ("MODE", "XCLIP SUBMENU" if submenu else "MAIN MENU", COLORS["WHITE"]),
        ("SELECTED", item, COLORS["CYAN"]),
        ("PATCHER", "READY" if patcher_ok else "MISSING", status_color(patcher_ok)),
        ("DISCOVER", "READY" if discover_ok else "MISSING", status_color(discover_ok)),
        ("XCLIP", "READY" if xclip_ok else "MISSING", status_color(xclip_ok)),
    ]
    for idx, (label, value, color) in enumerate(cells):
        cell = pygame.Rect(inner_x + idx * (cell_w + gap), inner_y, cell_w, 62)
        rounded_panel(surface, cell, COLORS["CELL_BG"], COLORS["HEADER_BORDER"], radius=12, border_width=2, shadow=False)
        label_surf = fonts["tiny_bold"].render(label, True, COLORS["TITLE"])
        value_surf = fonts["tiny"].render(fit_text(value, fonts["tiny"], cell.w - 16), True, color)
        surface.blit(label_surf, (cell.x + 8, cell.y + 8))
        surface.blit(value_surf, (cell.x + 8, cell.y + 31))


def draw_menu_panel(surface, rect, fonts, submenu=False, sub_selected=0):
    rounded_panel(surface, rect, COLORS["PANEL"], COLORS["BORDER"], radius=18)
    title = fonts["small"].render("MAIN ACTIONS", True, COLORS["TITLE"])
    surface.blit(title, (rect.x + 14, rect.y + 10))
    items = XCLIP_SUBMENU if submenu else MENU
    current_index = sub_selected if submenu else selected
    list_top = rect.y + 48
    line_h = 42
    box_h = 34
    for idx, item in enumerate(items):
        row_y = list_top + idx * line_h
        row_rect = pygame.Rect(rect.x + 12, row_y, rect.w - 24, box_h)
        active = idx == current_index
        if active:
            rounded_panel(surface, row_rect, COLORS["SELECT_FILL"], COLORS["SELECT_BORDER"], radius=12, border_width=2, shadow=False)
        text = item
        color = COLORS["CYAN"] if active else COLORS["TEXT"]
        prefix = "► " if active else "  "
        surf = fonts["menu"].render(prefix + fit_text(text, fonts["menu"], row_rect.w - 24), True, color)
        surface.blit(surf, (row_rect.x + 10, row_rect.y + 3))
    bubble = pygame.Rect(rect.x + 12, rect.bottom - 48, rect.w - 24, 30)
    rounded_panel(surface, bubble, COLORS["PANEL_ALT"], COLORS["HEADER_BORDER"], radius=12, border_width=2, shadow=False)
    state = "READY" if check_ultramode_enabled() else "PARTIAL"
    state_color = COLORS["GREEN"] if state == "READY" else COLORS["YELLOW"]
    left = fonts["tiny_bold"].render("ULTRAMODE STATUS", True, COLORS["TITLE"])
    right = fonts["tiny"].render(state, True, state_color)
    surface.blit(left, (bubble.x + 10, bubble.y + 7))
    surface.blit(right, (bubble.right - right.get_width() - 12, bubble.y + 7))


def draw_detail_panel(surface, rect, fonts, submenu=False, sub_selected=0):
    rounded_panel(surface, rect, COLORS["PANEL_SOFT"], COLORS["BORDER"], radius=18)
    title = fonts["small"].render("DETAILS / LEARNED CONTEXT", True, COLORS["TITLE"])
    surface.blit(title, (rect.x + 14, rect.y + 10))
    lines = build_detail_lines(current_item(submenu, sub_selected))
    y = rect.y + 48
    for label, value, color in lines:
        draw_label_value(surface, label, value, fonts, rect.x + 12, y, value_color=color, max_width=rect.w - 154)
        y += 38
    note_rect = pygame.Rect(rect.x + 12, rect.bottom - 88, rect.w - 24, 72)
    rounded_panel(surface, note_rect, COLORS["PANEL_ALT"], COLORS["VIOLET"], radius=12, border_width=2, shadow=False)
    note_title = fonts["tiny_bold"].render("MISTAKES LEARNED", True, COLORS["TITLE"])
    note_text = [
        "Keep helpers defined before use. Native window frame gives _, square, X.",
        "Ask before dumps. Keep sidecars/logs as .txt. Preserve changelog/notation.",
    ]
    surface.blit(note_title, (note_rect.x + 10, note_rect.y + 8))
    for idx, line in enumerate(note_text):
        surface.blit(fonts["tiny"].render(fit_text(line, fonts["tiny"], note_rect.w - 20), True, COLORS["TEXT"]),
                     (note_rect.x + 10, note_rect.y + 30 + idx * 16))


def draw_footer_bubble(surface, rect, label, text, fonts, label_color=None, text_color=None, border=None):
    rounded_panel(surface, rect, COLORS["PANEL_ALT"], border or COLORS["BORDER"], radius=12, border_width=2, shadow=False)
    label_surf = fonts["tiny_bold"].render(label, True, label_color or COLORS["TITLE"])
    value = fit_text(text, fonts["footer"], rect.w - 116)
    text_surf = fonts["footer"].render(value, True, text_color or COLORS["TEXT"])
    surface.blit(label_surf, (rect.x + 10, rect.y + 7))
    surface.blit(text_surf, (rect.x + 98, rect.y + 7))


def draw_status_bubble(surface, rect, fonts):
    message = APP_STATE["status_message"]
    color = COLORS["GREEN"] if "success" in message.lower() or "ready" in message.lower() else COLORS["TEXT"]
    if any(token in message.lower() for token in ("failed", "missing", "not found", "error")):
        color = COLORS["RED"]
    draw_footer_bubble(surface, rect, "STATUS", message, fonts, text_color=color, border=COLORS["HEADER_BORDER"])


def draw_help_bubble(surface, rect, fonts, submenu=False, sub_selected=0):
    draw_footer_bubble(surface, rect, "HELP", HELP_TEXT.get(current_item(submenu, sub_selected), "No help text yet."), fonts, text_color=COLORS["TEXT"], border=COLORS["BLUE"])


def draw_controls_bubble(surface, rect, fonts):
    draw_footer_bubble(surface, rect, "CTRL", "UP/DOWN move   ENTER/A select   ESC/B back   window uses native _ □ X", fonts, text_color=COLORS["VIOLET"], border=COLORS["VIOLET"])


def draw_path_bubble(surface, rect, fonts):
    draw_footer_bubble(surface, rect, "PATH", "/userdata/system/ultramode/um.py", fonts, text_color=COLORS["DIM"], border=COLORS["BORDER_SOFT"])


def draw_ui(surface, fonts, layout, submenu=False, sub_selected=0):
    surface.fill(COLORS["BG"])
    draw_header(surface, layout["header"], fonts)
    draw_top_grid(surface, layout["top_grid"], fonts, submenu, sub_selected)
    draw_menu_panel(surface, layout["left"], fonts, submenu, sub_selected)
    draw_detail_panel(surface, layout["right"], fonts, submenu, sub_selected)
    draw_status_bubble(surface, layout["status"], fonts)
    draw_help_bubble(surface, layout["help"], fonts, submenu, sub_selected)
    draw_controls_bubble(surface, layout["controls"], fonts)
    draw_path_bubble(surface, layout["path"], fonts)


def handle_select(index):
    if index == 0:
        return launch_patcher()
    if index == 1:
        return launch_tools()
    if index == 2:
        return system_info()
    if index == 3:
        return launch_installer()
    if index == 4:
        return fix_xclip_menu_action()
    if index == 5:
        do_reboot()
    if index == 6:
        pygame.quit()
        sys.exit(0)
    return ""


def fix_xclip_menu_action():
    global last_nav_time
    sub_selected = 0
    in_submenu = True
    local_last_accept = False
    local_last_back = False
    while in_submenu:
        draw_ui(screen, fonts, compute_layout(*screen.get_size()), submenu=True, sub_selected=sub_selected)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == XCLIP_EVENT:
                ok = getattr(event, "ok", False)
                msg = getattr(event, "msg", "")
                set_status("xclip action finished." if ok else f"xclip action failed: {msg}")
            elif event.type == pygame.VIDEORESIZE:
                resize_to(event.w, event.h)
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    sub_selected = (sub_selected - 1) % len(XCLIP_SUBMENU)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    sub_selected = (sub_selected + 1) % len(XCLIP_SUBMENU)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    choice = XCLIP_SUBMENU[sub_selected]
                    if choice == "Install xclip":
                        set_status("Installing xclip...")
                        run_in_thread(install_xclip_background, None)
                    elif choice == "Uninstall xclip":
                        set_status("Uninstalling xclip...")
                        run_in_thread(uninstall_xclip_background)
                    else:
                        in_submenu = False
                elif event.key == pygame.K_ESCAPE:
                    in_submenu = False
        now = time.time()
        if pad.up() and now - last_nav_time > INPUT_DELAY:
            sub_selected = (sub_selected - 1) % len(XCLIP_SUBMENU)
            last_nav_time = now
        elif pad.down() and now - last_nav_time > INPUT_DELAY:
            sub_selected = (sub_selected + 1) % len(XCLIP_SUBMENU)
            last_nav_time = now
        accept = pad.accept()
        back = pad.back()
        if accept and not local_last_accept:
            choice = XCLIP_SUBMENU[sub_selected]
            if choice == "Install xclip":
                set_status("Installing xclip...")
                run_in_thread(install_xclip_background, None)
            elif choice == "Uninstall xclip":
                set_status("Uninstalling xclip...")
                run_in_thread(uninstall_xclip_background)
            else:
                in_submenu = False
        if back and not local_last_back:
            in_submenu = False
        local_last_accept = accept
        local_last_back = back
        clock.tick(FPS)
    return "Back from xclip submenu."


pygame.init()
pygame.joystick.init()
screen, display_mode_label = create_display()
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()
fonts = build_fonts()
pad = UMGamepad()
selected = 0
running = True
last_nav_time = 0.0
last_accept = False
last_back = False
XCLIP_EVENT = pygame.USEREVENT + 1


def resize_to(width, height):
    global screen
    width, height = enforce_minimum_size(width, height)
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen


draw_ui(screen, fonts, compute_layout(*screen.get_size()))
pygame.display.flip()

while running:
    redraw = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            resize_to(event.w, event.h)
            redraw = True
        elif event.type == XCLIP_EVENT:
            ok = getattr(event, "ok", False)
            msg = getattr(event, "msg", "")
            set_status("xclip action finished." if ok else f"xclip action failed: {msg}")
            redraw = True
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                selected = (selected - 1) % len(MENU)
                redraw = True
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                selected = (selected + 1) % len(MENU)
                redraw = True
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                message = handle_select(selected)
                if message is not None:
                    set_status(message)
                redraw = True
            elif event.key == pygame.K_ESCAPE:
                running = False

    now = time.time()
    if pad.up() and now - last_nav_time > INPUT_DELAY:
        selected = (selected - 1) % len(MENU)
        last_nav_time = now
        redraw = True
    elif pad.down() and now - last_nav_time > INPUT_DELAY:
        selected = (selected + 1) % len(MENU)
        last_nav_time = now
        redraw = True

    accept = pad.accept()
    back = pad.back()
    if accept and not last_accept:
        message = handle_select(selected)
        if message is not None:
            set_status(message)
        redraw = True
    if back and not last_back:
        running = False

    last_accept = accept
    last_back = back

    if redraw:
        draw_ui(screen, fonts, compute_layout(*screen.get_size()))
        pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit(0)

# =============================================================================
# ### ULTRAMODE PROTECTED END
# =============================================================================
# ###EOL###
