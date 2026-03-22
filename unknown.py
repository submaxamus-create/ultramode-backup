This is the most logical direction because it supports:
- easier debugging
- cleaner AI handoff
- safer modular growth
- stronger gamepad integration
- future GUI upgrades without destabilizing core behavior

AI RULE REMINDER:
Future AI should preserve this orchestration model and avoid pushing unrelated
responsibilities back into um.py unless absolutely necessary.

PATCHER / LOG.TXT NOTE:
This block is intended to be patcher-friendly and sidecar-friendly.
It may be appended into a larger log.txt / help_log.txt / notation sidecar file
without changing runtime behavior.
