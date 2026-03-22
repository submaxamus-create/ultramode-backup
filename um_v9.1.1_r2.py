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
PATCHER_PATHS = [
    f"{ULTRAMODE_ROOT}/modules/patcher/umpatcher.py",
    f"{ULTRAMODE_ROOT}/umpatcher.py",
]
LOG_DIR = Path(f"{ULTRAMODE_ROOT}/logs")
ULTRAMODE_LOG = LOG_DIR / "ultramode.log"
WINDOW_TITLE = "ULTRAMODE MAIN MENU v9.1.1"
WIDTH, HEIGHT = 1024, 600
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
    "Tools": "Placeholder for future modular utilities.",
    "System Info": "Placeholder for status and environment details.",
    "Automatic Installer": "Attempts to enable xclip if the helper or package manager route works.",
    "Fix xclip": "Open install / uninstall submenu for clipboard support used by patch workflows.",
    "Reboot": "Exit the UI and ask the system to reboot.",
    "Exit": "Exit UltraMode cleanly.",
}
COLORS = {
    "BG": (5, 8, 22),
    "PANEL": (10, 12, 30),
    "PANEL_ALT": (15, 18, 40),
    "BORDER": (100, 180, 255),
    "TITLE": (200, 120, 255),
    "TEXT": (230, 235, 245),
    "DIM": (150, 165, 190),
    "CYAN": (110, 230, 255),
    "GREEN": (90, 255, 130),
    "RED": (255, 110, 110),
    "YELLOW": (255, 230, 120),
}

for extra_path in (MODULES_PATH, MANDATORY_PATH, XCLIP_PATH):
    if extra_path not in sys.path:
        sys.path.append(extra_path)

try:
    from um_gamepad import UMGamepad  # preferred permanent module path
    GAMEPAD_SOURCE = "um_gamepad"
except Exception:
    try:
        from um_gamepad_shim import UMGamepad  # compatibility fallback only
        GAMEPAD_SOURCE = "um_gamepad_shim"
    except Exception:
        GAMEPAD_SOURCE = "builtin_fallback"

        class UMGamepad:  # minimal fallback so keyboard UI still works
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
logger.info("ultramode starting (%s r2) via %s", "v9.1.1", GAMEPAD_SOURCE)
append_runtime_note(f"um.py launch via {GAMEPAD_SOURCE}", "BOOT")

pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 30, bold=True)
small = pygame.font.SysFont("monospace", 21)
tiny = pygame.font.SysFont("monospace", 17)
pad = UMGamepad()
selected = 0
running = True
last_nav_time = 0.0
last_accept = False
last_back = False
xclip_status_message = ""
XCLIP_EVENT = pygame.USEREVENT + 1


def post_xclip_event(ok: bool, msg: str):
    try:
        pygame.event.post(pygame.event.Event(XCLIP_EVENT, {"ok": ok, "msg": str(msg)}))
    except Exception:
        logger.exception("failed to post xclip event")


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


def draw_panel(rect, title=None):
    pygame.draw.rect(screen, COLORS["PANEL"], rect)
    pygame.draw.rect(screen, COLORS["BORDER"], rect, 2)
    if title:
        title_surf = tiny.render(title, True, COLORS["CYAN"])
        screen.blit(title_surf, (rect.x + 12, rect.y + 8))


def draw_status_row(y_pos, label, ok):
    color = COLORS["GREEN"] if ok else COLORS["RED"]
    state = "READY" if ok else "MISSING"
    surf = small.render(f"{label}: {state}", True, color)
    screen.blit(surf, (100, y_pos))


def draw_help_bar(current_item):
    rect = pygame.Rect(20, HEIGHT - 120, WIDTH - 40, 100)
    draw_panel(rect, "HELP / STATUS")
    help_text = HELP_TEXT.get(current_item, "No help text yet.")
    status_text = xclip_status_message or "Standing by."
    line_1 = tiny.render(help_text, True, COLORS["TEXT"])
    line_2 = tiny.render(status_text, True, COLORS["DIM"])
    line_3 = tiny.render("UP/DOWN or D-Pad = Move   ENTER/A = Select   ESC/B = Exit/Back", True, COLORS["DIM"])
    screen.blit(line_1, (rect.x + 12, rect.y + 32))
    screen.blit(line_2, (rect.x + 12, rect.y + 54))
    screen.blit(line_3, (rect.x + 12, rect.y + 74))


def draw_header():
    top = pygame.Rect(20, 18, WIDTH - 40, 68)
    draw_panel(top, "ULTRAMODE")
    title = font.render(WINDOW_TITLE, True, COLORS["TITLE"])
    screen.blit(title, (top.x + 12, top.y + 24))
    path_text = tiny.render("/userdata/system/ultramode/um.py", True, COLORS["DIM"])
    screen.blit(path_text, (WIDTH - path_text.get_width() - 34, top.y + 12))


def draw_center(submenu=False, sub_selected=0):
    rect = pygame.Rect(20, 100, WIDTH - 40, HEIGHT - 240)
    draw_panel(rect, "MAIN MENU")
    draw_status_row(rect.y + 34, "XCLIP", check_xclip_raw())
    draw_status_row(rect.y + 64, "PATCHER", bool(find_patcher_path()))
    items = XCLIP_SUBMENU if submenu else MENU
    current_index = sub_selected if submenu else selected
    base_y = rect.y + 120
    if submenu:
        label = small.render("FIX XCLIP SUBMENU", True, COLORS["YELLOW"])
        screen.blit(label, (rect.x + 12, rect.y + 92))
    for idx, item in enumerate(items):
        active = idx == current_index
        prefix = "► " if active else "  "
        color = COLORS["CYAN"] if active else COLORS["TEXT"]
        surf = font.render(prefix + item, True, color)
        screen.blit(surf, (rect.x + 70, base_y + (idx * 42)))


def draw_menu(message="", submenu=False, sub_selected=0):
    global xclip_status_message
    if message:
        xclip_status_message = message
    screen.fill(COLORS["BG"])
    draw_header()
    draw_center(submenu=submenu, sub_selected=sub_selected)
    current_item = (XCLIP_SUBMENU[sub_selected] if submenu else MENU[selected])
    draw_help_bar(current_item)


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
    patcher = find_patcher_path() or "missing"
    return f"gamepad={GAMEPAD_SOURCE} | xclip={'ready' if check_xclip_raw() else 'missing'} | patcher={patcher}"


def launch_installer():
    ok, msg = try_install_xclip_with_module(None)
    append_runtime_note(f"automatic installer result: {ok} {msg}", "INSTALLER")
    return "xclip enabled successfully." if ok else f"xclip enable failed: {msg}"


def do_reboot():
    try:
        pygame.quit()
    except Exception:
        pass
    os.system("reboot")
    sys.exit(0)


def fix_xclip_menu_action():
    global xclip_status_message
    sub_selected = 0
    in_submenu = True
    while in_submenu:
        draw_menu("", submenu=True, sub_selected=sub_selected)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    sub_selected = (sub_selected - 1) % len(XCLIP_SUBMENU)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    sub_selected = (sub_selected + 1) % len(XCLIP_SUBMENU)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    choice = XCLIP_SUBMENU[sub_selected]
                    if choice == "Install xclip":
                        xclip_status_message = "Installing xclip..."
                        run_in_thread(install_xclip_background, None)
                    elif choice == "Uninstall xclip":
                        xclip_status_message = "Uninstalling xclip..."
                        run_in_thread(uninstall_xclip_background)
                    else:
                        in_submenu = False
                elif event.key == pygame.K_ESCAPE:
                    in_submenu = False
            elif event.type == XCLIP_EVENT:
                ok = getattr(event, "ok", False)
                msg = getattr(event, "msg", "")
                xclip_status_message = "xclip action finished." if ok else f"xclip action failed: {msg}"
        now = time.time()
        if pad.up() and now - last_nav_time > INPUT_DELAY:
            sub_selected = (sub_selected - 1) % len(XCLIP_SUBMENU)
        elif pad.down() and now - last_nav_time > INPUT_DELAY:
            sub_selected = (sub_selected + 1) % len(XCLIP_SUBMENU)
        if pad.accept():
            choice = XCLIP_SUBMENU[sub_selected]
            if choice == "Install xclip":
                xclip_status_message = "Installing xclip..."
                run_in_thread(install_xclip_background, None)
            elif choice == "Uninstall xclip":
                xclip_status_message = "Uninstalling xclip..."
                run_in_thread(uninstall_xclip_background)
            else:
                in_submenu = False
            time.sleep(INPUT_DELAY)
        if pad.back():
            in_submenu = False
            time.sleep(INPUT_DELAY)
        clock.tick(FPS)
    return ""


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


draw_menu()
pygame.display.flip()

while running:
    redraw = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
                    draw_menu(message)
                    pygame.display.flip()
                redraw = True
            elif event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == XCLIP_EVENT:
            ok = getattr(event, "ok", False)
            msg = getattr(event, "msg", "")
            xclip_status_message = "xclip action finished." if ok else f"xclip action failed: {msg}"
            redraw = True
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
            draw_menu(message)
            pygame.display.flip()
        redraw = True
    if back and not last_back:
        running = False
    last_accept = accept
    last_back = back
    if redraw:
        draw_menu()
        pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit(0)

# =============================================================================
# ### ULTRAMODE PROTECTED END
# =============================================================================
# ###EOL###
