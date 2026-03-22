#!/usr/bin/env python3
# =============================================================================
# PROJECT NOTATIONS — DO NOT DELETE OR MODIFY EXISTING LINES — ONLY APPEND
# =============================================================================
# FILENAME:      um.py
# FOLDER PATH:   /userdata/system/ultramode/
# DESTINATION:   /userdata/system/ultramode/um.py
# Version:       v9.4
# Revision:      r1
#
# PURPOSE:
#   - Ultramode main module and menu launcher.
#   - Preserve strong in-file rules and project identity while keeping the
#     executable body cleaner than bloated AI rewrite attempts.
#   - Use shared gamepad handling, keep keyboard support, present a cleaner GUI,
#     and provide safer xclip / patcher launch behavior.
#   - Preserve important lessons learned from prior AI mistakes, especially
#     indentation breakage, non-working changes, and version/path drift.
#   - Add desktop environment scanning + restore logic so UltraMode can detect
#     a broken Batocera Desktop Mode taskbar state and attempt a safe recovery.
#   - Present desktop recovery and buffer diagnostics inside a separate
#     developer-tools box so advanced checks stay organized and controller-safe.
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
# 2026-03-22 00:00 | ChatGPT | v9.3    | r1 | Added Batocera desktop scan/fix action, red/green desktop status, /tmp/restore_taskbar.log logging, and safe taskbar restore flow based on the working shell logic.
# 2026-03-22 00:00 | ChatGPT | v9.4    | r1 | Reworked UM layout toward a fuller umpatcher-style look: fixed 1280x720 size, rounded bubbles, separate DEV MODE TOOLS box, desktop scan/fix moved into that box, and added a non-destructive buffer checker.
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
LOG_DIR = Path(f"{ULTRAMODE_ROOT}/logs")
ULTRAMODE_LOG = LOG_DIR / "ultramode.log"
RESTORE_LOG = Path("/tmp/restore_taskbar.log")
BUFFER_LOG = Path("/tmp/ultramode_buffer_check.log")
WINDOW_TITLE = "ULTRAMODE MAIN MENU v9.4"
WIDTH, HEIGHT = 1280, 720
FPS = 30
INPUT_DELAY = 0.15

MAIN_MENU = [
    "UltraMode Patcher",
    "Tools",
    "System Info",
    "Automatic Installer",
    "Reboot",
    "Exit",
]
DEV_MENU = [
    "Desktop Scan / Fix",
    "Buffer Checker",
    "Fix xclip",
]
XCLIP_SUBMENU = ["Install xclip", "Uninstall xclip", "Back"]

HELP_TEXT = {
    "UltraMode Patcher": "Launch the patcher module from the patcher folder if present.",
    "Tools": "Placeholder for future modular utilities.",
    "System Info": "Show launcher, patcher, xclip, desktop, and buffer readiness.",
    "Automatic Installer": "Attempt to enable xclip using helper modules or package-manager fallbacks.",
    "Reboot": "Exit the UI and ask the system to reboot.",
    "Exit": "Exit UltraMode cleanly.",
    "Desktop Scan / Fix": "Scan Batocera desktop state, show red/green panel status, and attempt a safe taskbar restore if needed.",
    "Buffer Checker": "Run a non-destructive diagnostic for clipboard / display / patcher / log path readiness used by patch and buffer-style workflows.",
    "Fix xclip": "Open install / uninstall submenu for clipboard support used by patch workflows.",
    "Install xclip": "Install xclip in the background and report the result here.",
    "Uninstall xclip": "Uninstall xclip in the background and report the result here.",
    "Back": "Return to the previous menu.",
}

COLORS = {
    "BG": (7, 7, 12),
    "HEADER": (5, 5, 5),
    "PANEL": (15, 15, 22),
    "PANEL_ALT": (10, 10, 16),
    "PANEL_SOFT": (18, 18, 26),
    "CELL_BG": (11, 11, 15),
    "BORDER": (195, 78, 52),
    "BORDER_SOFT": (110, 48, 30),
    "TITLE": (245, 239, 95),
    "NEON": (240, 230, 78),
    "TEXT": (230, 230, 232),
    "DIM": (155, 155, 165),
    "WHITE": (245, 245, 245),
    "GREEN": (76, 230, 126),
    "RED": (235, 92, 92),
    "YELLOW": (240, 208, 90),
    "ORANGE": (228, 145, 70),
    "BLUE": (122, 180, 255),
    "SELECT": (250, 245, 120),
    "SHADOW": (0, 0, 0),
}

DESKTOP_PANEL_ORDER = ["lxpanel", "xfce4-panel", "tint2"]
DESKTOP_SCAN_ORDER = ["lxpanel", "xfce4-panel", "tint2", "pcmanfm", "openbox", "xfwm4", "lxsession"]
DESKTOP_START_COMMANDS = {
    "lxpanel": ["lxpanel", "--profile", "LXDE"],
    "xfce4-panel": ["xfce4-panel"],
    "tint2": ["tint2"],
    "pcmanfm_desktop": ["pcmanfm", "--desktop"],
    "openbox_restart": ["openbox", "--restart"],
    "xfwm4_replace": ["xfwm4", "--replace"],
}
XCLIP_EVENT = pygame.USEREVENT + 1
DESKTOP_STATUS_EVENT = pygame.USEREVENT + 2
BUFFER_EVENT = pygame.USEREVENT + 3

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

LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=str(ULTRAMODE_LOG),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("ultramode")
logger.info("ultramode starting (%s r1) via %s", "v9.4", GAMEPAD_SOURCE)
append_runtime_note(f"um.py launch via {GAMEPAD_SOURCE}", "BOOT")

pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()

menu_font = pygame.font.SysFont("monospace", 24, bold=True)
small = pygame.font.SysFont("monospace", 18)
small_bold = pygame.font.SysFont("monospace", 18, bold=True)
tiny = pygame.font.SysFont("monospace", 15)
tiny_bold = pygame.font.SysFont("monospace", 15, bold=True)

pad = UMGamepad()
main_selected = 0
dev_selected = 0
focus_box = "main"
running = True
last_nav_time = 0.0
last_accept = False
last_back = False
status_message = "Ready."
desktop_scan_cache = {}
desktop_scan_time = 0.0
buffer_check_cache = {}
buffer_check_time = 0.0


def post_simple_event(event_type: int, ok: bool, msg: str):
    try:
        pygame.event.post(pygame.event.Event(event_type, {"ok": ok, "msg": str(msg)}))
    except Exception:
        logger.exception("failed to post pygame event %s", event_type)


def run_in_thread(target, *args, **kwargs):
    thread = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return thread


def set_status(message: str):
    global status_message
    status_message = message


def safe_run_capture(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result.returncode, (result.stdout or "").strip(), (result.stderr or "").strip()
    except Exception as exc:
        return 1, "", str(exc)


def command_exists(name):
    return shutil.which(name) is not None


def process_running(name):
    code, _, _ = safe_run_capture(["pgrep", "-x", name])
    if code == 0:
        return True
    code, out, _ = safe_run_capture(["ps", "aux"])
    if code != 0:
        return False
    return f" {name}" in f" {out}" or f"/{name}" in out


def find_patcher_path():
    for candidate in PATCHER_PATHS:
        if os.path.exists(candidate):
            return candidate
    return ""


def check_ultramode_enabled():
    return bool(find_patcher_path()) and os.path.isdir(LOG_DIR)


def get_clock_text():
    return time.strftime("%Y-%m-%d  %H:%M:%S")


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


def rounded_box(rect, fill_key="PANEL", border_key="BORDER", radius=18, shadow=True):
    if shadow:
        shadow_rect = rect.move(4, 5)
        pygame.draw.rect(screen, COLORS["SHADOW"], shadow_rect, border_radius=radius)
    pygame.draw.rect(screen, COLORS[fill_key], rect, border_radius=radius)
    pygame.draw.rect(screen, COLORS[border_key], rect, 2, border_radius=radius)


def rounded_panel(rect, title=None, fill_key="PANEL", border_key="BORDER", title_color=None):
    rounded_box(rect, fill_key=fill_key, border_key=border_key, radius=18, shadow=True)
    if title:
        title_surf = tiny_bold.render(title, True, title_color or COLORS["NEON"])
        screen.blit(title_surf, (rect.x + 14, rect.y + 10))


def grid_cell(rect, label, value, value_color=None):
    rounded_box(rect, fill_key="CELL_BG", border_key="NEON", radius=14, shadow=False)
    label_surf = tiny_bold.render(label, True, COLORS["NEON"])
    value_surf = tiny.render(str(value), True, value_color or COLORS["WHITE"])
    screen.blit(label_surf, (rect.x + 9, rect.y + 8))
    screen.blit(value_surf, (rect.x + 9, rect.y + 30))


def footer_bubble(rect, label, text, label_color=None, text_color=None):
    rounded_box(rect, fill_key="PANEL_ALT", border_key="BORDER", radius=14, shadow=False)
    label_surf = tiny_bold.render(label, True, label_color or COLORS["NEON"])
    text_surf = tiny.render(str(text), True, text_color or COLORS["TEXT"])
    screen.blit(label_surf, (rect.x + 12, rect.y + 8))
    screen.blit(text_surf, (rect.x + 96, rect.y + 8))


def check_xclip_raw() -> bool:
    try:
        return bool(xclip_is_installed())
    except Exception:
        return False


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
        post_simple_event(XCLIP_EVENT, ok, msg)
    except Exception as exc:
        logger.exception("install_xclip_background exception")
        post_simple_event(XCLIP_EVENT, False, str(exc))


def uninstall_xclip_background():
    try:
        ok, msg = uninstall_xclip()
        append_runtime_note(f"xclip uninstall result: {ok} {msg}", "XCLIP")
        post_simple_event(XCLIP_EVENT, ok, msg)
    except Exception as exc:
        logger.exception("uninstall_xclip_background exception")
        post_simple_event(XCLIP_EVENT, False, str(exc))


def desktop_env():
    env = os.environ.copy()
    env.setdefault("DISPLAY", ":0")
    if not env.get("XAUTHORITY"):
        env.pop("XAUTHORITY", None)
    return env


def process_snapshot_text():
    code, out, err = safe_run_capture(["ps", "aux"])
    if code != 0:
        return err or "ps snapshot unavailable"
    lines = []
    for line in out.splitlines():
        if any(token in line for token in DESKTOP_SCAN_ORDER):
            lines.append(line)
    return "\n".join(lines) if lines else "(no desktop processes matched filter)"


def panel_running_name(running_map):
    for name in DESKTOP_PANEL_ORDER:
        if running_map.get(name):
            return name
    return ""


def format_bool(value):
    return "yes" if value else "no"


def scan_desktop_environment():
    binaries = {name: shutil.which(name) for name in DESKTOP_SCAN_ORDER}
    running_map = {name: process_running(name) for name in DESKTOP_SCAN_ORDER}
    panel_name = panel_running_name(running_map)
    display_value = os.environ.get("DISPLAY") or ":0"
    xauthority_value = os.environ.get("XAUTHORITY") or "not set"
    wayland_value = os.environ.get("WAYLAND_DISPLAY") or "not set"
    desktop_ok = running_map.get("openbox", False) and running_map.get("pcmanfm", False)
    return {
        "binaries": binaries,
        "running": running_map,
        "panel_name": panel_name,
        "panel_ok": bool(panel_name),
        "desktop_ok": desktop_ok,
        "display": display_value,
        "xauthority": xauthority_value,
        "wayland": wayland_value,
        "snapshot": process_snapshot_text(),
    }


def get_desktop_scan(force=False):
    global desktop_scan_cache, desktop_scan_time
    now = time.time()
    if force or not desktop_scan_cache or (now - desktop_scan_time) > 1.0:
        desktop_scan_cache = scan_desktop_environment()
        desktop_scan_time = now
    return desktop_scan_cache


def write_restore_log(line, reset=False):
    RESTORE_LOG.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if reset else "a"
    with RESTORE_LOG.open(mode, encoding="utf-8") as handle:
        handle.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {line}\n")


def start_background_process(cmd):
    with RESTORE_LOG.open("a", encoding="utf-8") as log_handle:
        try:
            subprocess.Popen(
                cmd,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                env=desktop_env(),
                start_new_session=True,
            )
            return True, f"started: {' '.join(cmd)}"
        except Exception as exc:
            return False, str(exc)


def stop_process(name):
    try:
        subprocess.run(["pkill", "-x", name], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def refresh_scan_and_log():
    scan = get_desktop_scan(force=True)
    write_restore_log("Final process snapshot:")
    for line in scan["snapshot"].splitlines():
        write_restore_log(line)
    return scan


def restore_desktop_taskbar():
    scan = get_desktop_scan(force=True)
    write_restore_log("Restore run started.", reset=True)
    write_restore_log(f"DISPLAY={scan['display']} XAUTHORITY={scan['xauthority']} WAYLAND_DISPLAY={scan['wayland']}")
    write_restore_log("Detected binaries:")
    for name in DESKTOP_SCAN_ORDER:
        write_restore_log(f"  {name}: {scan['binaries'].get(name) or 'NOT FOUND'}")
    write_restore_log("Initial process snapshot:")
    for line in scan["snapshot"].splitlines():
        write_restore_log(line)

    if scan["panel_name"]:
        panel_name = scan["panel_name"]
        write_restore_log(f"{panel_name} already running; restarting.")
        stop_process(panel_name)
        time.sleep(0.5)
        ok, msg = start_background_process(DESKTOP_START_COMMANDS[panel_name])
        write_restore_log(msg if ok else f"start failed: {msg}")
        time.sleep(1.0)
        scan = get_desktop_scan(force=True)
        if scan["panel_ok"]:
            scan = refresh_scan_and_log()
            return True, f"desktop ok: {scan['panel_name']} running"

    for panel_name in DESKTOP_PANEL_ORDER:
        if scan["binaries"].get(panel_name):
            if panel_name == "tint2":
                write_restore_log("Starting tint2. WARNING: tint2 may be unstable on this system; do not auto-respawn.")
            else:
                write_restore_log(f"Starting {panel_name}.")
            ok, msg = start_background_process(DESKTOP_START_COMMANDS[panel_name])
            write_restore_log(msg if ok else f"start failed: {msg}")
            time.sleep(1.0)
            scan = get_desktop_scan(force=True)
            if scan["running"].get(panel_name):
                scan = refresh_scan_and_log()
                return True, f"desktop ok: {panel_name} running"

    if scan["binaries"].get("pcmanfm"):
        write_restore_log("Starting pcmanfm --desktop.")
        ok, msg = start_background_process(DESKTOP_START_COMMANDS["pcmanfm_desktop"])
        write_restore_log(msg if ok else f"start failed: {msg}")
        time.sleep(1.0)

    if scan["running"].get("openbox") and scan["binaries"].get("openbox"):
        write_restore_log("Restarting openbox.")
        ok, msg = start_background_process(DESKTOP_START_COMMANDS["openbox_restart"])
        write_restore_log(msg if ok else f"start failed: {msg}")
        time.sleep(1.0)

    scan = get_desktop_scan(force=True)
    if scan["panel_ok"]:
        scan = refresh_scan_and_log()
        return True, f"desktop ok: {scan['panel_name']} running"

    if scan["binaries"].get("xfwm4"):
        write_restore_log("Trying xfwm4 --replace.")
        ok, msg = start_background_process(DESKTOP_START_COMMANDS["xfwm4_replace"])
        write_restore_log(msg if ok else f"start failed: {msg}")
        time.sleep(1.0)

    scan = refresh_scan_and_log()
    if scan["panel_ok"]:
        return True, f"desktop ok: {scan['panel_name']} running"
    return False, "desktop restore failed; see /tmp/restore_taskbar.log"


def desktop_scan_fix_background():
    try:
        scan = get_desktop_scan(force=True)
        if scan["panel_ok"]:
            msg = f"desktop already ok: {scan['panel_name']} running"
            write_restore_log("Scan only; panel already present.", reset=True)
            write_restore_log(msg)
            write_restore_log("Current process snapshot:")
            for line in scan["snapshot"].splitlines():
                write_restore_log(line)
            append_runtime_note(msg, "DESKTOP")
            post_simple_event(DESKTOP_STATUS_EVENT, True, msg)
            return
        ok, msg = restore_desktop_taskbar()
        append_runtime_note(msg, "DESKTOP")
        post_simple_event(DESKTOP_STATUS_EVENT, ok, msg)
    except Exception as exc:
        logger.exception("desktop_scan_fix_background exception")
        append_runtime_note(f"desktop restore exception: {exc}", "DESKTOP")
        post_simple_event(DESKTOP_STATUS_EVENT, False, str(exc))


def can_write_path(path_obj: Path):
    try:
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        with path_obj.open("a", encoding="utf-8") as handle:
            handle.write("")
        return True
    except Exception:
        return False


def run_buffer_check():
    patcher = find_patcher_path()
    display = os.environ.get("DISPLAY") or ":0"
    xauthority = os.environ.get("XAUTHORITY") or "not set"
    checks = {
        "display": bool(display),
        "xclip": check_xclip_raw(),
        "patcher": bool(patcher),
        "logs_dir": LOG_DIR.exists() and os.access(str(LOG_DIR), os.W_OK),
        "tmp_log": can_write_path(BUFFER_LOG),
        "restore_log_path": can_write_path(RESTORE_LOG),
    }
    ready = checks["display"] and checks["xclip"] and checks["patcher"] and checks["logs_dir"]
    detail = {
        "ready": ready,
        "checks": checks,
        "display": display,
        "xauthority": xauthority,
        "patcher": patcher or "missing",
        "buffer_log": str(BUFFER_LOG),
        "restore_log": str(RESTORE_LOG),
    }
    BUFFER_LOG.parent.mkdir(parents=True, exist_ok=True)
    with BUFFER_LOG.open("w", encoding="utf-8") as handle:
        handle.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] UltraMode buffer check\n")
        handle.write(f"DISPLAY={display}\n")
        handle.write(f"XAUTHORITY={xauthority}\n")
        handle.write(f"PATCHER={patcher or 'missing'}\n")
        for key, value in checks.items():
            handle.write(f"{key}={'yes' if value else 'no'}\n")
    return detail


def get_buffer_check(force=False):
    global buffer_check_cache, buffer_check_time
    now = time.time()
    if force or not buffer_check_cache or (now - buffer_check_time) > 2.0:
        buffer_check_cache = run_buffer_check()
        buffer_check_time = now
    return buffer_check_cache


def buffer_check_background():
    try:
        detail = get_buffer_check(force=True)
        msg = "buffer ready" if detail["ready"] else "buffer check found missing pieces"
        append_runtime_note(msg, "BUFFER")
        post_simple_event(BUFFER_EVENT, detail["ready"], msg)
    except Exception as exc:
        logger.exception("buffer_check_background exception")
        append_runtime_note(f"buffer check exception: {exc}", "BUFFER")
        post_simple_event(BUFFER_EVENT, False, str(exc))


def menu_items(submenu=False, dev_box=False):
    if submenu:
        return XCLIP_SUBMENU
    return DEV_MENU if dev_box else MAIN_MENU


def current_item(submenu=False, sub_selected=0):
    if submenu:
        idx = max(0, min(sub_selected, len(XCLIP_SUBMENU) - 1))
        return XCLIP_SUBMENU[idx]
    items = DEV_MENU if focus_box == "dev" else MAIN_MENU
    idx = dev_selected if focus_box == "dev" else main_selected
    idx = max(0, min(idx, len(items) - 1))
    return items[idx]


def selection_status_color(ok_value):
    return COLORS["GREEN"] if ok_value else COLORS["RED"]


def detail_lines(item_name):
    scan = get_desktop_scan()
    buffer_detail = get_buffer_check()
    patcher = find_patcher_path()
    panel_color = COLORS["GREEN"] if scan["panel_ok"] else COLORS["RED"]
    desktop_color = COLORS["GREEN"] if scan["desktop_ok"] else COLORS["YELLOW"]
    buffer_color = COLORS["GREEN"] if buffer_detail["ready"] else COLORS["RED"]

    if item_name == "Desktop Scan / Fix":
        binaries_summary = " ".join(
            f"{name}={'yes' if scan['binaries'].get(name) else 'no'}"
            for name in ("lxpanel", "xfce4-panel", "tint2", "pcmanfm", "openbox")
        )
        running_summary = " ".join(
            f"{name}={'yes' if scan['running'].get(name) else 'no'}"
            for name in ("lxpanel", "xfce4-panel", "tint2", "pcmanfm", "openbox")
        )
        return [
            ("Panel", scan["panel_name"] or "missing", panel_color),
            ("Desktop", f"openbox={format_bool(scan['running'].get('openbox'))} pcmanfm={format_bool(scan['running'].get('pcmanfm'))}", desktop_color),
            ("Display", scan["display"], COLORS["BLUE"]),
            ("Binaries", binaries_summary, COLORS["TEXT"]),
            ("Running", running_summary, COLORS["TEXT"]),
            ("Log", str(RESTORE_LOG), COLORS["DIM"]),
        ]

    if item_name == "Buffer Checker":
        checks = buffer_detail["checks"]
        checks_summary = " ".join(
            f"{key}={'yes' if value else 'no'}"
            for key, value in checks.items()
        )
        return [
            ("Ready", "yes" if buffer_detail["ready"] else "no", buffer_color),
            ("Display", buffer_detail["display"], COLORS["BLUE"]),
            ("XAUTH", buffer_detail["xauthority"], COLORS["DIM"]),
            ("Checks", checks_summary, COLORS["TEXT"]),
            ("Patcher", buffer_detail["patcher"], COLORS["GREEN"] if patcher else COLORS["RED"]),
            ("Log", buffer_detail["buffer_log"], COLORS["DIM"]),
        ]

    if item_name == "System Info":
        return [
            ("Selected", item_name, COLORS["SELECT"]),
            ("Desktop", f"panel={scan['panel_name'] or 'missing'}", panel_color),
            ("Buffer", "ready" if buffer_detail["ready"] else "missing pieces", buffer_color),
            ("Gamepad", GAMEPAD_SOURCE, COLORS["BLUE"]),
            ("Patcher", patcher if patcher else "missing", COLORS["GREEN"] if patcher else COLORS["RED"]),
            ("xclip", "ready" if check_xclip_raw() else "missing", COLORS["GREEN"] if check_xclip_raw() else COLORS["RED"]),
        ]

    return [
        ("Selected", item_name, COLORS["SELECT"]),
        ("Purpose", HELP_TEXT.get(item_name, "No help text yet."), COLORS["TEXT"]),
        ("Desktop", f"panel={scan['panel_name'] or 'missing'}", panel_color),
        ("Buffer", "ready" if buffer_detail["ready"] else "needs checks", buffer_color),
        ("Patcher", patcher if patcher else "missing", COLORS["GREEN"] if patcher else COLORS["RED"]),
        ("Logs", str(LOG_DIR), COLORS["DIM"]),
    ]


def draw_header():
    rect = pygame.Rect(20, 16, WIDTH - 40, 46)
    rounded_panel(rect, fill_key="HEADER")
    title_surf = small_bold.render(WINDOW_TITLE, True, COLORS["TITLE"])
    clock_surf = tiny.render(get_clock_text(), True, COLORS["NEON"])
    screen.blit(title_surf, (rect.x + 14, rect.y + 12))
    screen.blit(clock_surf, (rect.right - clock_surf.get_width() - 14, rect.y + 15))


def draw_top_grid():
    scan = get_desktop_scan()
    buffer_detail = get_buffer_check()
    area = pygame.Rect(20, 74, WIDTH - 40, 84)
    rounded_panel(area, fill_key="PANEL_ALT")
    inner_x = area.x + 10
    inner_y = area.y + 12
    gap = 8
    cell_w = (area.width - 20 - gap * 5) // 6
    item = current_item()
    patcher_ok = bool(find_patcher_path())
    cells = [
        ("FOCUS", "DEV BOX" if focus_box == "dev" else "MAIN BOX", COLORS["WHITE"]),
        ("SELECTED", item, COLORS["SELECT"]),
        ("DESKTOP", scan["panel_name"] if scan["panel_ok"] else "NO PANEL", COLORS["GREEN"] if scan["panel_ok"] else COLORS["RED"]),
        ("BUFFER", "READY" if buffer_detail["ready"] else "CHECK", COLORS["GREEN"] if buffer_detail["ready"] else COLORS["RED"]),
        ("PATCHER", "READY" if patcher_ok else "MISSING", COLORS["GREEN"] if patcher_ok else COLORS["RED"]),
        ("XCLIP", "READY" if check_xclip_raw() else "MISSING", COLORS["GREEN"] if check_xclip_raw() else COLORS["RED"]),
    ]
    for idx, (label, value, color) in enumerate(cells):
        rect = pygame.Rect(inner_x + idx * (cell_w + gap), inner_y, cell_w, 58)
        grid_cell(rect, label, value, color)


def draw_list_box(rect, title, items, selected_idx, active, kind="main"):
    border_key = "NEON" if active else "BORDER"
    title_color = COLORS["TITLE"] if active else COLORS["NEON"]
    fill_key = "PANEL_SOFT" if active else "PANEL"
    rounded_panel(rect, title=title, fill_key=fill_key, border_key=border_key, title_color=title_color)

    base_y = rect.y + 44
    line_h = 34
    for idx, item in enumerate(items):
        active_item = idx == selected_idx
        color = COLORS["TEXT"]
        if item == "Desktop Scan / Fix":
            color = COLORS["GREEN"] if get_desktop_scan()["panel_ok"] else COLORS["RED"]
        elif item == "Buffer Checker":
            color = COLORS["GREEN"] if get_buffer_check()["ready"] else COLORS["RED"]
        elif item == "Fix xclip":
            color = COLORS["GREEN"] if check_xclip_raw() else COLORS["YELLOW"]
        if active_item:
            color = COLORS["SELECT"]
        prefix = "> " if active_item else "  "
        surf = menu_font.render(prefix + item, True, color)
        screen.blit(surf, (rect.x + 18, base_y + idx * line_h))

    bottom_label = "ACTIVE" if active else "INACTIVE"
    bottom_color = COLORS["GREEN"] if active else COLORS["DIM"]
    lbl = tiny_bold.render("BOX STATE", True, COLORS["NEON"])
    val = tiny.render(bottom_label, True, bottom_color)
    screen.blit(lbl, (rect.x + 16, rect.bottom - 28))
    screen.blit(val, (rect.right - val.get_width() - 16, rect.bottom - 28))


def draw_detail_panel():
    rect = pygame.Rect(410, 170, 454, 370)
    rounded_panel(rect, "DETAILS", fill_key="PANEL")
    lines = detail_lines(current_item())
    y = rect.y + 44
    for label, value, color in lines:
        label_surf = tiny_bold.render(f"{label}:", True, COLORS["NEON"])
        screen.blit(label_surf, (rect.x + 16, y))
        wrap_width = rect.width - 148
        wrapped = wrap_text(str(value), tiny, wrap_width)
        for i, line in enumerate(wrapped[:3]):
            value_surf = tiny.render(line, True, color)
            screen.blit(value_surf, (rect.x + 138, y + i * 16))
        y += 38 if len(wrapped) == 1 else 54


def draw_status_bubble():
    rect = pygame.Rect(20, 554, WIDTH - 40, 34)
    lower = status_message.lower()
    color = COLORS["TEXT"]
    if any(token in lower for token in ("ready", "ok", "success", "running", "finished")):
        color = COLORS["GREEN"]
    if any(token in lower for token in ("failed", "missing", "error")):
        color = COLORS["RED"]
    footer_bubble(rect, "STATUS", status_message, label_color=COLORS["NEON"], text_color=color)


def draw_help_bubble():
    rect = pygame.Rect(20, 596, WIDTH - 40, 28)
    footer_bubble(rect, "HELP", HELP_TEXT.get(current_item(), "No help text yet."))


def draw_ctrl_bubble():
    rect = pygame.Rect(20, 632, WIDTH - 40, 28)
    footer_bubble(rect, "CTRL", "UP/DOWN move   LEFT/RIGHT switch box   ENTER/A select   ESC/B back/exit")


def draw_path_bubble():
    rect = pygame.Rect(20, 668, WIDTH - 40, 28)
    footer_bubble(rect, "PATH", "/userdata/system/ultramode/um.py", text_color=COLORS["DIM"])


def draw_ui():
    screen.fill(COLORS["BG"])
    draw_header()
    draw_top_grid()
    draw_list_box(
        pygame.Rect(20, 170, 372, 370),
        "MAIN ACTIONS",
        MAIN_MENU,
        main_selected,
        focus_box == "main",
        kind="main",
    )
    draw_detail_panel()
    draw_list_box(
        pygame.Rect(882, 170, 378, 370),
        "DEV MODE TOOLS",
        DEV_MENU,
        dev_selected,
        focus_box == "dev",
        kind="dev",
    )
    draw_status_bubble()
    draw_help_bubble()
    draw_ctrl_bubble()
    draw_path_bubble()


def launch_patcher():
    patcher = find_patcher_path()
    if not patcher:
        append_runtime_note("patcher launch requested but no patcher file found", "PATCHER")
        return "patcher not found"
    try:
        pygame.quit()
    except Exception:
        pass
    try:
        subprocess.run([sys.executable or "python3", patcher], check=False)
    except Exception as exc:
        print("[UltraMode] Failed to launch patcher:", exc)
        time.sleep(2)
    sys.exit(0)


def launch_tools():
    append_runtime_note("tools placeholder opened", "TOOLS")
    return "Tools placeholder not wired yet."


def system_info():
    scan = get_desktop_scan(force=True)
    buffer_detail = get_buffer_check(force=True)
    patcher = find_patcher_path() or "missing"
    return (
        f"desktop={scan['panel_name'] or 'missing'} | "
        f"openbox={format_bool(scan['running'].get('openbox'))} | "
        f"pcmanfm={format_bool(scan['running'].get('pcmanfm'))} | "
        f"buffer={'ready' if buffer_detail['ready'] else 'check'} | "
        f"xclip={'ready' if check_xclip_raw() else 'missing'} | "
        f"patcher={patcher}"
    )


def launch_desktop_scan_fix():
    set_status("Scanning desktop / attempting fix...")
    run_in_thread(desktop_scan_fix_background)
    return "Desktop scan started..."


def launch_buffer_checker():
    set_status("Running buffer checker...")
    run_in_thread(buffer_check_background)
    return "Buffer check started..."


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


def fix_xclip_menu_action():
    global last_nav_time
    sub_selected = 0
    in_submenu = True
    local_last_accept = False
    local_last_back = False
    while in_submenu:
        screen.fill(COLORS["BG"])
        draw_header()
        draw_top_grid()
        draw_list_box(
            pygame.Rect(20, 170, 372, 370),
            "MAIN ACTIONS",
            MAIN_MENU,
            main_selected,
            False,
            kind="main",
        )
        draw_detail_panel()
        draw_list_box(
            pygame.Rect(882, 170, 378, 370),
            "XCLIP SUBMENU",
            XCLIP_SUBMENU,
            sub_selected,
            True,
            kind="dev",
        )
        draw_status_bubble()
        draw_help_bubble()
        draw_ctrl_bubble()
        draw_path_bubble()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == XCLIP_EVENT:
                ok = getattr(event, "ok", False)
                msg = getattr(event, "msg", "")
                set_status("xclip action finished." if ok else f"xclip action failed: {msg}")
            elif event.type == DESKTOP_STATUS_EVENT:
                ok = getattr(event, "ok", False)
                msg = getattr(event, "msg", "")
                set_status(msg if ok else f"desktop action failed: {msg}")
            elif event.type == BUFFER_EVENT:
                ok = getattr(event, "ok", False)
                msg = getattr(event, "msg", "")
                set_status(msg if ok else f"buffer action failed: {msg}")
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


def handle_main_select(index):
    if index == 0:
        return launch_patcher()
    if index == 1:
        return launch_tools()
    if index == 2:
        return system_info()
    if index == 3:
        return launch_installer()
    if index == 4:
        do_reboot()
    if index == 5:
        pygame.quit()
        sys.exit(0)
    return ""


def handle_dev_select(index):
    if index == 0:
        return launch_desktop_scan_fix()
    if index == 1:
        return launch_buffer_checker()
    if index == 2:
        return fix_xclip_menu_action()
    return ""


def move_selection(delta):
    global main_selected, dev_selected
    if focus_box == "main":
        main_selected = (main_selected + delta) % len(MAIN_MENU)
    else:
        dev_selected = (dev_selected + delta) % len(DEV_MENU)


draw_ui()
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == XCLIP_EVENT:
            ok = getattr(event, "ok", False)
            msg = getattr(event, "msg", "")
            set_status("xclip action finished." if ok else f"xclip action failed: {msg}")
            get_buffer_check(force=True)
            get_desktop_scan(force=True)
        elif event.type == DESKTOP_STATUS_EVENT:
            ok = getattr(event, "ok", False)
            msg = getattr(event, "msg", "")
            set_status(msg if ok else f"desktop action failed: {msg}")
            get_desktop_scan(force=True)
            get_buffer_check(force=True)
        elif event.type == BUFFER_EVENT:
            ok = getattr(event, "ok", False)
            msg = getattr(event, "msg", "")
            set_status(msg if ok else f"buffer action failed: {msg}")
            get_buffer_check(force=True)
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                move_selection(-1)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                move_selection(1)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                focus_box = "main"
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                focus_box = "dev"
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                message = handle_dev_select(dev_selected) if focus_box == "dev" else handle_main_select(main_selected)
                if message is not None:
                    set_status(message)
            elif event.key == pygame.K_ESCAPE:
                running = False

    now = time.time()
    if pad.up() and now - last_nav_time > INPUT_DELAY:
        move_selection(-1)
        last_nav_time = now
    elif pad.down() and now - last_nav_time > INPUT_DELAY:
        move_selection(1)
        last_nav_time = now
    elif pad.left() and now - last_nav_time > INPUT_DELAY:
        focus_box = "main"
        last_nav_time = now
    elif pad.right() and now - last_nav_time > INPUT_DELAY:
        focus_box = "dev"
        last_nav_time = now

    accept = pad.accept()
    back = pad.back()
    if accept and not last_accept:
        message = handle_dev_select(dev_selected) if focus_box == "dev" else handle_main_select(main_selected)
        if message is not None:
            set_status(message)
    if back and not last_back:
        running = False
    last_accept = accept
    last_back = back

    draw_ui()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit(0)

# =============================================================================
# FUTURE / THINKTANK APPEND-ONLY NOTES
# =============================================================================
# 2026-03-22 | ChatGPT | v9.4 r1
#   - The cleaner logic was to separate developer diagnostics from everyday
#     launcher actions instead of stacking more rows into one tall menu.
#   - Desktop Scan / Fix now lives in a DEV MODE TOOLS box with Buffer Checker
#     and Fix xclip so controller navigation remains simple: left/right chooses
#     box, up/down chooses item.
#   - Buffer Checker is intentionally non-destructive and meant to answer a
#     practical question: are the display / clipboard / patcher / writable log
#     pieces present for patch-buffer style workflows to behave?
#   - Current size is fixed to 1280x720 to better match a fuller patcher-style
#     screen and give the footer bubbles more room.
#   - A future version could add a hidden Developer Mode toggle so the dev box
#     can be collapsed for normal users while still preserving the code path.
#
# =============================================================================
# ### ULTRAMODE PROTECTED END
# =============================================================================
# ###EOL###
