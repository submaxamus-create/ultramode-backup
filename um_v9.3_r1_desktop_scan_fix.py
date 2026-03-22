#!/usr/bin/env python3
# =============================================================================
# PROJECT NOTATIONS — DO NOT DELETE OR MODIFY EXISTING LINES — ONLY APPEND
# =============================================================================
# FILENAME:      um.py
# FOLDER PATH:   /userdata/system/ultramode/
# DESTINATION:   /userdata/system/ultramode/um.py
# Version:       v9.3
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
WINDOW_TITLE = "ULTRAMODE MAIN MENU v9.3"
WIDTH, HEIGHT = 1024, 600
FPS = 30
INPUT_DELAY = 0.15
MENU = [
    "UltraMode Patcher",
    "Tools",
    "System Info",
    "Desktop Scan / Fix",
    "Automatic Installer",
    "Fix xclip",
    "Reboot",
    "Exit",
]
XCLIP_SUBMENU = ["Install xclip", "Uninstall xclip", "Back"]
HELP_TEXT = {
    "UltraMode Patcher": "Launch the patcher module from the patcher folder if present.",
    "Tools": "Placeholder for future modular utilities.",
    "System Info": "Show current launcher, patcher, xclip, and desktop scan status.",
    "Desktop Scan / Fix": "Scan Batocera desktop state, show red/green panel status, and attempt a safe taskbar restore if needed.",
    "Automatic Installer": "Attempt to enable xclip using helper modules or package-manager fallbacks.",
    "Fix xclip": "Open install / uninstall submenu for clipboard support used by patch workflows.",
    "Reboot": "Exit the UI and ask the system to reboot.",
    "Exit": "Exit UltraMode cleanly.",
    "Install xclip": "Install xclip in the background and report the result here.",
    "Uninstall xclip": "Uninstall xclip in the background and report the result here.",
    "Back": "Return to the main menu.",
}
COLORS = {
    "BG": (6, 6, 10),
    "HEADER": (0, 0, 0),
    "PANEL": (16, 16, 22),
    "PANEL_ALT": (10, 10, 14),
    "CELL_BG": (12, 12, 12),
    "BORDER": (190, 70, 45),
    "BORDER_SOFT": (90, 40, 28),
    "TITLE": (240, 235, 90),
    "NEON": (238, 230, 70),
    "TEXT": (230, 230, 230),
    "DIM": (150, 150, 150),
    "WHITE": (245, 245, 245),
    "GREEN": (80, 230, 120),
    "RED": (235, 90, 90),
    "YELLOW": (240, 210, 90),
    "ORANGE": (225, 140, 60),
    "BLUE": (120, 180, 255),
    "SELECT": (245, 245, 120),
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
DESKTOP_STATUS_EVENT = pygame.USEREVENT + 2

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
logger.info("ultramode starting (%s r1) via %s", "v9.3", GAMEPAD_SOURCE)
append_runtime_note(f"um.py launch via {GAMEPAD_SOURCE}", "BOOT")

pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 28, bold=True)
menu_font = pygame.font.SysFont("monospace", 26, bold=True)
small = pygame.font.SysFont("monospace", 18)
small_bold = pygame.font.SysFont("monospace", 18, bold=True)
tiny = pygame.font.SysFont("monospace", 15)
tiny_bold = pygame.font.SysFont("monospace", 15, bold=True)
pad = UMGamepad()
selected = 0
running = True
last_nav_time = 0.0
last_accept = False
last_back = False
xclip_status_message = "Standing by."
status_message = "Ready."
desktop_scan_cache = {}
desktop_scan_time = 0.0
XCLIP_EVENT = pygame.USEREVENT + 1


def post_xclip_event(ok: bool, msg: str):
    try:
        pygame.event.post(pygame.event.Event(XCLIP_EVENT, {"ok": ok, "msg": str(msg)}))
    except Exception:
        logger.exception("failed to post xclip event")


def post_desktop_event(ok: bool, msg: str):
    try:
        pygame.event.post(pygame.event.Event(DESKTOP_STATUS_EVENT, {"ok": ok, "msg": str(msg)}))
    except Exception:
        logger.exception("failed to post desktop event")


def run_in_thread(target, *args, **kwargs):
    thread = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return thread


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


def panel(rect, title=None, fill_key="PANEL", border_key="BORDER"):
    pygame.draw.rect(screen, COLORS[fill_key], rect)
    pygame.draw.rect(screen, COLORS[border_key], rect, 2)
    if title:
        title_surf = tiny_bold.render(title, True, COLORS["NEON"])
        screen.blit(title_surf, (rect.x + 10, rect.y + 8))


def grid_cell(rect, label, value, value_color=None):
    pygame.draw.rect(screen, COLORS["CELL_BG"], rect)
    pygame.draw.rect(screen, COLORS["NEON"], rect, 2)
    label_surf = tiny_bold.render(label, True, COLORS["NEON"])
    value_surf = tiny.render(value, True, value_color or COLORS["WHITE"])
    screen.blit(label_surf, (rect.x + 8, rect.y + 7))
    screen.blit(value_surf, (rect.x + 8, rect.y + 26))


def footer_bubble(rect, label, text, label_color=None, text_color=None):
    pygame.draw.rect(screen, COLORS["PANEL_ALT"], rect)
    pygame.draw.rect(screen, COLORS["BORDER"], rect, 2)
    label_surf = tiny_bold.render(label, True, label_color or COLORS["NEON"])
    text_surf = tiny.render(text, True, text_color or COLORS["TEXT"])
    screen.blit(label_surf, (rect.x + 10, rect.y + 8))
    screen.blit(text_surf, (rect.x + 92, rect.y + 8))


def menu_items(submenu=False):
    return XCLIP_SUBMENU if submenu else MENU


def current_item(submenu=False, sub_selected=0):
    items = menu_items(submenu)
    idx = sub_selected if submenu else selected
    idx = max(0, min(idx, len(items) - 1))
    return items[idx]


def safe_run_capture(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result.returncode, (result.stdout or "").strip(), (result.stderr or "").strip()
    except Exception as exc:
        return 1, "", str(exc)


def process_running(name):
    code, _, _ = safe_run_capture(["pgrep", "-x", name])
    if code == 0:
        return True
    code, out, _ = safe_run_capture(["ps", "aux"])
    if code != 0:
        return False
    return f" {name}" in f" {out}" or f"/{name}" in out


def process_snapshot_text():
    code, out, err = safe_run_capture(["ps", "aux"])
    if code != 0:
        return err or "ps snapshot unavailable"
    lines = []
    for line in out.splitlines():
        if any(token in line for token in DESKTOP_SCAN_ORDER):
            lines.append(line)
    return "\n".join(lines) if lines else "(no desktop processes matched filter)"


def desktop_env():
    env = os.environ.copy()
    env.setdefault("DISPLAY", ":0")
    if not env.get("XAUTHORITY"):
        env.pop("XAUTHORITY", None)
    return env


def command_exists(name):
    return shutil.which(name) is not None


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
            post_desktop_event(True, msg)
            return
        ok, msg = restore_desktop_taskbar()
        append_runtime_note(msg, "DESKTOP")
        post_desktop_event(ok, msg)
    except Exception as exc:
        logger.exception("desktop_scan_fix_background exception")
        append_runtime_note(f"desktop restore exception: {exc}", "DESKTOP")
        post_desktop_event(False, str(exc))


def detail_lines(item_name):
    scan = get_desktop_scan()
    patcher = find_patcher_path()
    panel_color = COLORS["GREEN"] if scan["panel_ok"] else COLORS["RED"]
    desktop_color = COLORS["GREEN"] if scan["desktop_ok"] else COLORS["YELLOW"]
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
            ("Display", scan["display"], COLORS["BLUE"] if scan["display"] else COLORS["RED"]),
            ("Binaries", binaries_summary, COLORS["TEXT"]),
            ("Running", running_summary, COLORS["TEXT"]),
            ("Log", str(RESTORE_LOG), COLORS["DIM"]),
        ]
    if item_name == "System Info":
        return [
            ("Selected", item_name, COLORS["SELECT"]),
            ("Desktop", f"panel={scan['panel_name'] or 'missing'}", panel_color),
            ("X Env", f"DISPLAY={scan['display']} XAUTHORITY={scan['xauthority']}", COLORS["BLUE"]),
            ("Gamepad", GAMEPAD_SOURCE, COLORS["BLUE"]),
            ("Patcher", patcher if patcher else "missing", COLORS["GREEN"] if patcher else COLORS["RED"]),
            ("xclip", "ready" if check_xclip_raw() else "missing", COLORS["GREEN"] if check_xclip_raw() else COLORS["RED"]),
        ]
    return [
        ("Selected", item_name, COLORS["SELECT"]),
        ("Purpose", HELP_TEXT.get(item_name, "No help text yet."), COLORS["TEXT"]),
        ("Desktop", f"panel={scan['panel_name'] or 'missing'}", panel_color),
        ("Gamepad", GAMEPAD_SOURCE, COLORS["BLUE"]),
        ("Patcher", patcher if patcher else "missing", COLORS["GREEN"] if patcher else COLORS["RED"]),
        ("xclip", "ready" if check_xclip_raw() else "missing", COLORS["GREEN"] if check_xclip_raw() else COLORS["RED"]),
    ]


def draw_header():
    rect = pygame.Rect(20, 16, WIDTH - 40, 42)
    pygame.draw.rect(screen, COLORS["HEADER"], rect)
    pygame.draw.rect(screen, COLORS["BORDER"], rect, 2)
    title_surf = small_bold.render(WINDOW_TITLE, True, COLORS["TITLE"])
    clock_surf = tiny.render(get_clock_text(), True, COLORS["NEON"])
    screen.blit(title_surf, (rect.x + 12, rect.y + 9))
    screen.blit(clock_surf, (rect.right - clock_surf.get_width() - 12, rect.y + 12))


def draw_top_grid(submenu=False, sub_selected=0):
    scan = get_desktop_scan()
    area = pygame.Rect(20, 68, WIDTH - 40, 74)
    panel(area, None, fill_key="PANEL_ALT")
    inner_x = area.x + 10
    inner_y = area.y + 9
    gap = 8
    cell_w = (area.width - 20 - gap * 4) // 5
    item = current_item(submenu, sub_selected)
    patcher_ok = bool(find_patcher_path())
    panel_text = scan["panel_name"] if scan["panel_ok"] else "NO PANEL"
    panel_color = COLORS["GREEN"] if scan["panel_ok"] else COLORS["RED"]
    cells = [
        ("MODE", "XCLIP SUBMENU" if submenu else "MAIN MENU", COLORS["WHITE"]),
        ("SELECTED", item, COLORS["SELECT"]),
        ("DESKTOP", panel_text, panel_color),
        ("PATCHER", "READY" if patcher_ok else "MISSING", COLORS["GREEN"] if patcher_ok else COLORS["RED"]),
        ("XCLIP", "READY" if check_xclip_raw() else "MISSING", COLORS["GREEN"] if check_xclip_raw() else COLORS["RED"]),
    ]
    for idx, (label, value, color) in enumerate(cells):
        rect = pygame.Rect(inner_x + idx * (cell_w + gap), inner_y, cell_w, 56)
        grid_cell(rect, label, value, color)


def draw_menu_panel(submenu=False, sub_selected=0):
    rect = pygame.Rect(20, 154, 410, 284)
    panel(rect, "MAIN ACTIONS")
    items = menu_items(submenu)
    idx_now = sub_selected if submenu else selected
    base_y = rect.y + 44
    line_h = 30
    scan = get_desktop_scan()
    for idx, item in enumerate(items):
        active = idx == idx_now
        color = COLORS["TEXT"]
        if item == "Desktop Scan / Fix":
            color = COLORS["GREEN"] if scan["panel_ok"] else COLORS["RED"]
        if active:
            color = COLORS["SELECT"]
        text = ("> " if active else "  ") + item
        surf = menu_font.render(text, True, color)
        screen.blit(surf, (rect.x + 18, base_y + idx * line_h))
    status_y = rect.bottom - 48
    state = "READY" if check_ultramode_enabled() else "PARTIAL"
    state_color = COLORS["GREEN"] if state == "READY" else COLORS["YELLOW"]
    lbl = tiny_bold.render("ULTRAMODE STATUS", True, COLORS["NEON"])
    val = tiny.render(state, True, state_color)
    screen.blit(lbl, (rect.x + 14, status_y))
    screen.blit(val, (rect.right - val.get_width() - 14, status_y))


def draw_detail_panel(submenu=False, sub_selected=0):
    rect = pygame.Rect(444, 154, WIDTH - 464, 284)
    panel(rect, "DETAILS")
    lines = detail_lines(current_item(submenu, sub_selected))
    y = rect.y + 42
    for label, value, color in lines:
        label_surf = tiny_bold.render(f"{label}:", True, COLORS["NEON"])
        screen.blit(label_surf, (rect.x + 14, y))
        wrap_width = rect.width - 150
        wrapped = wrap_text(str(value), tiny, wrap_width)
        for i, line in enumerate(wrapped[:3]):
            value_surf = tiny.render(line, True, color)
            screen.blit(value_surf, (rect.x + 138, y + i * 16))
        y += 34 if len(wrapped) == 1 else 50


def draw_status_bubble():
    rect = pygame.Rect(20, 448, WIDTH - 40, 34)
    color = COLORS["GREEN"] if "success" in status_message.lower() or "ready" in status_message.lower() or "ok" in status_message.lower() else COLORS["TEXT"]
    if "failed" in status_message.lower() or "missing" in status_message.lower():
        color = COLORS["RED"]
    footer_bubble(rect, "STATUS", status_message, label_color=COLORS["NEON"], text_color=color)


def draw_help_bubble(submenu=False, sub_selected=0):
    rect = pygame.Rect(20, 490, WIDTH - 40, 28)
    footer_bubble(rect, "HELP", HELP_TEXT.get(current_item(submenu, sub_selected), "No help text yet."))


def draw_ctrl_bubble():
    rect = pygame.Rect(20, 526, WIDTH - 40, 28)
    footer_bubble(rect, "CTRL", "UP/DOWN move   ENTER/A select   ESC/B back/exit")


def draw_path_bubble():
    rect = pygame.Rect(20, 562, WIDTH - 40, 28)
    footer_bubble(rect, "PATH", "/userdata/system/ultramode/um.py", text_color=COLORS["DIM"])


def draw_ui(submenu=False, sub_selected=0):
    screen.fill(COLORS["BG"])
    draw_header()
    draw_top_grid(submenu, sub_selected)
    draw_menu_panel(submenu, sub_selected)
    draw_detail_panel(submenu, sub_selected)
    draw_status_bubble()
    draw_help_bubble(submenu, sub_selected)
    draw_ctrl_bubble()
    draw_path_bubble()


def set_status(message):
    global status_message, xclip_status_message
    status_message = message
    xclip_status_message = message


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
    patcher = find_patcher_path() or "missing"
    return f"desktop={scan['panel_name'] or 'missing'} | openbox={format_bool(scan['running'].get('openbox'))} | pcmanfm={format_bool(scan['running'].get('pcmanfm'))} | xclip={'ready' if check_xclip_raw() else 'missing'} | patcher={patcher}"


def launch_desktop_scan_fix():
    set_status("Scanning desktop / attempting fix...")
    draw_ui()
    pygame.display.flip()
    run_in_thread(desktop_scan_fix_background)
    return "Desktop scan started..."


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
        draw_ui(submenu=True, sub_selected=sub_selected)
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


def handle_select(index):
    if index == 0:
        return launch_patcher()
    if index == 1:
        return launch_tools()
    if index == 2:
        return system_info()
    if index == 3:
        return launch_desktop_scan_fix()
    if index == 4:
        return launch_installer()
    if index == 5:
        return fix_xclip_menu_action()
    if index == 6:
        do_reboot()
    if index == 7:
        pygame.quit()
        sys.exit(0)
    return ""


draw_ui()
pygame.display.flip()

while running:
    redraw = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == XCLIP_EVENT:
            ok = getattr(event, "ok", False)
            msg = getattr(event, "msg", "")
            set_status("xclip action finished." if ok else f"xclip action failed: {msg}")
            redraw = True
        elif event.type == DESKTOP_STATUS_EVENT:
            ok = getattr(event, "ok", False)
            msg = getattr(event, "msg", "")
            set_status(msg if ok else f"desktop action failed: {msg}")
            get_desktop_scan(force=True)
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
        draw_ui()
        pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit(0)

# =============================================================================
# FUTURE / THINKTANK APPEND-ONLY NOTES
# =============================================================================
# 2026-03-22 | ChatGPT | v9.3 r1
#   - Batocera Desktop Mode recovery was folded into the main launcher because
#     the user wanted a controller-accessible Python fix rather than relying on
#     a shell script handoff.
#   - Current logic is intentionally non-destructive: process checks, process
#     restarts, and log writing only. No package installs, config edits, or
#     auto-respawn loops for tint2.
#   - A future cleaner version could split desktop repair into its own helper
#     module under modules/tools while preserving this launcher hook.
#
# =============================================================================
# ### ULTRAMODE PROTECTED END
# =============================================================================
# ###EOL###
