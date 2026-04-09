# Script Ideas Filed From Chat — 2026-04-09

- Date: 2026-04-09
- Time: 08:20pm America/New_York
- Source: current ChatGPT conversation
- Purpose: pull script and module ideas out of chat flow and store them in a dedicated, easier-to-find note

## Priority order discussed

### Immediate / strongest next builds
1. `um_file_map_builder.py`
   - Scan the UltraMode tree
   - Build a master map of files
   - Mark likely live, duplicate, obsolete, broken, backup, helper, and orphaned items

2. `um_header_auditor.py`
   - Check shebang
   - Check top header zone placement
   - Verify required fields
   - Detect misplaced notation
   - Detect missing protected markers

3. `um_dependency_mapper.py`
   - Map imports and helper relationships
   - Find missing modules
   - Surface broken references
   - Flag circular import risks

4. `um_file_map_rules.py`
   - Apply classification logic to scan results
   - Label likely live, backup, orphan, duplicate cluster, bad header, wrong folder

5. `um_module_registry.py`
   - Build a clean registry of tools, menu paths, launch targets, dependencies, and return paths

## Additional modules discussed

6. `um_shared_ui_contract.py`
   - Lock shared rules for top bar, lamps, footer/help bars, title behavior, sizing, and safe areas

7. `um_recovery_history.py`
   - Backup list
   - Rollback points
   - Patch history
   - Restore targets

8. `um_sidecar_splitter.py`
   - Move heavy thinktank/help/rules out of scripts into `_log.txt` sidecars safely

9. `um_duplicate_cluster_viewer.py`
   - Group same/similar scripts
   - Show likely winner and stale variants

10. `um_launcher_router.py`
   - Central launch/return handler
   - Keep module navigation consistent

11. `um_status_lamp_service.py`
   - Shared lamp meanings and health checks for header/gui/input/file/runtime/safe-write

12. `um_preview_panel.py`
   - Reusable file preview widget for patcher/browser/harvester/registry/scanner tools

13. `um_scan_report_formatter.py`
   - Turn raw scan data into human-usable ticket and report output

14. `um_obsolete_quarantine.py`
   - Move likely dead/old files into review/quarantine instead of deleting

15. `um_reference_rewriter.py`
   - Update references/paths/imports when files move or are renamed

16. `um_master_log_sync.py`
   - Gather worthwhile rules/ideas/lessons from modules into master logs

17. `um_asset_recovery_checker.py`
   - Check for missing assets, sidecars, backgrounds, icons, helper files, menu targets

18. `um_input_test_lab.py`
   - Validate keyboard/gamepad behavior across modules

19. `um_menu_health_check.py`
   - Check menu entries for broken targets, missing files, bad labels, and bad return paths

20. `um_canonical_promoter.py`
   - Let the user mark a file as approved/live/canonical and record why

## Suggested phase grouping

### Phase 1 — map and classify
- `um_file_map_builder.py`
- `um_header_auditor.py`
- `um_dependency_mapper.py`
- `um_file_map_rules.py`
- `um_duplicate_cluster_viewer.py`

### Phase 2 — stabilize shared behavior
- `um_shared_ui_contract.py`
- `um_status_lamp_service.py`
- `um_preview_panel.py`
- `um_launcher_router.py`
- `um_input_test_lab.py`

### Phase 3 — organize and reduce chaos
- `um_sidecar_splitter.py`
- `um_scan_report_formatter.py`
- `um_obsolete_quarantine.py`
- `um_module_registry.py`
- `um_menu_health_check.py`

### Phase 4 — safety and growth
- `um_recovery_history.py`
- `um_asset_recovery_checker.py`
- `um_reference_rewriter.py`
- `um_master_log_sync.py`
- `um_canonical_promoter.py`

## Filing note
These ideas were separated from the raw chat backup so they can later be moved into a more permanent thinktank / planning / registry area.

## Related backup file
- `chat_backups/chat_backup_2026-04-09_2018_full_reconstruct.md`
