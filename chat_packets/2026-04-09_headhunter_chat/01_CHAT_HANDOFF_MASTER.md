# UltraMode HeadHunter Chat — Master Handoff

## What happened in this chat

This chat began as a UMPatcher capability discussion about whether Python 3 code could be recognized and labeled before patch/apply. The direction then evolved into a larger UltraMode architecture discussion where header intelligence became the central design target. The final dominant outcome was the design and first seed draft of `headhunter.py`.

## Main outcome

### `headhunter.py`

HeadHunter is intended to be a single Python 3 **header truth / repair / routing engine** for UltraMode.

It should:
- scan the top recognition zone
- verify `#!/usr/bin/env python3`
- detect header drift
- validate required core fields
- validate useful extended fields
- preserve/check:
  - `Hi Mom.`
  - `### ULTRAMODE PROTECTED START`
  - `### ULTRAMODE PROTECTED END`
  - `### EOL ###`
- compare header claims against real facts:
  - actual filename
  - actual folder path
  - actual extension
  - live destination
  - sidecar/log/thinktank paths
- use notation as backup identity
- assign:
  - `HEADER_HEALTH`
  - `TRUST_CLASS`
- detect roles:
  - runtime script
  - helper/tool
  - patch packet
  - chat dump
  - sidecar/log
  - fragment
- return:
  - loud labels
  - lamp states
  - repair suggestions
  - patcher-safe tiny UI packet
  - deeper report for Hammer / Shredder / Code Bank

Key locked phrase from the chat:

> HeadHunter should be a compact truth engine, not a cosmetic header checker.

## Support scripts created in this chat

### `umpatcher_code_labeler.py`
Purpose:
- classify content as Python / fragment / text / broken syntax / etc.
- check syntax
- check header presence
- check notation hints
- check danger patterns
- output labels like:
  - `VALID_PATCH_PY`
  - `UNTRUSTED_PYTHON`
  - `PYTHON_FRAGMENT`
  - `BROKEN_SYNTAX`
  - `TEXT_NOT_CODE`

### `umpatcher_preflight_bridge.py`
Purpose:
- wrap the classifier
- convert results into:
  - primary lamp
  - syntax/header/destination/notation/danger/trust lamps
  - short UI decision block for UMPatcher

## Reference material pasted by user that shaped HeadHunter

### 1. Header law packet
Main ideas:
- header is architecture
- top recognition zone is truth zone
- required core fields must carry structured meaning
- extended fields exist to support scanners / menus / sidecars / digest logic / trust / lineage
- notation is a second identity system
- marker preservation is mandatory
- `HEADER_HEALTH` and `TRUST_CLASS` are visible UI/state concepts
- menu registration should eventually be self-describing
- digest / shredder / code bank behavior should be supported by headers

### 2. `um_idea_extractor_v1_0_r2_2026-04-05_progress_buffer.py`
This acted as a style / structure reference.
Important patterns:
- scan-safe top header
- protected block
- notation blocks
- report-first behavior
- future plug tags
- append-only changelog / goals / thinktank / patch points
- plain dataclasses and helper functions

### 3. `chat_sidecar_browser.py`
This acted as a header/UI/health-panel reference.
Important patterns:
- machine-readable header identity
- menu/self-registration fields
- lamp/health panel concepts
- separation of parser logic from GUI logic
- visible status signaling

## Newest-first script order from this chat

1. `headhunter.py`
2. `umpatcher_preflight_bridge.py`
3. `umpatcher_code_labeler.py`

If later asked what the newest or most important item from this chat is, the answer should point to **HeadHunter first**.

## Suggested other files to inspect later

These were identified in chat as likely helpful for future evolution:
- `umpatcher.py`
- current preferred `um.py`
- Rule Harvester script(s)
- sidecar standards / master rules text files
- incoming patch examples from `modules/patcher/incoming/`
- Iron Gate / stamper / digest-related scripts
- script-map / manifest / module registration helpers
- `um_script_map_builder*.py`

## Safe status / GitHub backup status

During the chat, the repo was confirmed as:
- `submaxamus-create/ultramode-backup`

A first attempted packet check showed the packet was not yet present. After that failure, this packet was intentionally written into GitHub.

## Filing order inside this packet

- `00_NEWEST_FIRST_INDEX.md`
- `01_CHAT_HANDOFF_MASTER.md`
- `02_CHAT_TRANSCRIPT_CURATED.md`
- `scripts/headhunter.py`
- `scripts/umpatcher_preflight_bridge.py`
- `scripts/umpatcher_code_labeler.py`
