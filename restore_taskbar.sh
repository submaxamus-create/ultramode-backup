#!/bin/sh
# restore_taskbar.sh
# Auto-detect and attempt to restore a missing desktop panel (non-destructive).

LOG="/tmp/restore_taskbar.log"
echo "Restore run: $(date -Is)" >"$LOG"

# Helpers
exists() { command -v "$1" >/dev/null 2>&1; }
running() { pgrep -x "$1" >/dev/null 2>&1; }
try_start() {
  echo "Trying: $*" >>"$LOG"
  sh -c "$*" >>"$LOG" 2>&1 &
  sleep 1
}

echo "Detected binaries:" >>"$LOG"
for b in lxpanel xfce4-panel tint2 pcmanfm lxsession xfwm4 openbox; do
  printf "%s: " "$b" >>"$LOG"
  if exists "$b"; then echo "yes" >>"$LOG"; else echo "no" >>"$LOG"; fi
done

echo "Running processes snapshot:" >>"$LOG"
ps aux | egrep 'lxpanel|xfce4-panel|tint2|openbox|pcmanfm|xfwm4|lxsession' | egrep -v egrep >>"$LOG" 2>&1

# 1) If a panel process is present, try to restart it
if running lxpanel; then
  echo "lxpanel running; restarting" >>"$LOG"
  pkill lxpanel 2>/dev/null || true
  try_start "lxpanel --profile LXDE"
  exit 0
fi

if running xfce4-panel; then
  echo "xfce4-panel running; restarting" >>"$LOG"
  pkill xfce4-panel 2>/dev/null || true
  try_start "xfce4-panel"
  exit 0
fi

if running tint2; then
  echo "tint2 running; restarting" >>"$LOG"
  pkill tint2 2>/dev/null || true
  try_start "tint2"
  exit 0
fi

# 2) No panel running — attempt to start available panel binaries (safe, non-destructive)
if exists lxpanel; then
  echo "Starting lxpanel" >>"$LOG"
  try_start "lxpanel --profile LXDE"
  sleep 1
  if running lxpanel; then echo "lxpanel started" >>"$LOG"; exit 0; fi
fi

if exists xfce4-panel; then
  echo "Starting xfce4-panel" >>"$LOG"
  try_start "xfce4-panel"
  sleep 1
  if running xfce4-panel; then echo "xfce4-panel started" >>"$LOG"; exit 0; fi
fi

if exists tint2; then
  echo "Starting tint2 (may crash if binary unstable)" >>"$LOG"
  try_start "tint2"
  sleep 1
  if running tint2; then echo "tint2 started" >>"$LOG"; exit 0; fi
fi

# 3) Try to bring back desktop icons/wallpaper (pcmanfm) and restart openbox
if exists pcmanfm; then
  echo "Starting pcmanfm --desktop" >>"$LOG"
  try_start "pcmanfm --desktop"
fi

if running openbox; then
  echo "Restarting openbox" >>"$LOG"
  try_start "openbox --restart"
fi

# 4) Try replacing window manager (xfwm4) if available
if exists xfwm4; then
  echo "Replacing window manager with xfwm4" >>"$LOG"
  try_start "xfwm4 --replace"
fi

# Final status
echo "Final process snapshot:" >>"$LOG"
ps aux | egrep 'lxpanel|xfce4-panel|tint2|openbox|pcmanfm|xfwm4|lxsession' | egrep -v egrep >>"$LOG" 2>&1
echo "Done. Check $LOG for details." >>"$LOG"
