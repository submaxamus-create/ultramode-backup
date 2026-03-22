#!/usr/bin/env python3
# =============================================================================
# FILENAME:      directory_list.py
# PURPOSE:
#   - Walk a folder tree and write a richer directory listing to a text file.
#   - Includes modified timestamp, size, type marker, and full path.
#   - Helps compare newer/older files and spot likely important files faster.
# =============================================================================

import os
import sys
from datetime import datetime


def format_timestamp(ts):
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "UNKNOWN_TIME"


def format_size(num_bytes):
    try:
        num_bytes = int(num_bytes)
    except Exception:
        return "UNKNOWN_SIZE"

    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024.0


def list_files_and_folders(startpath="."):
    startpath = os.path.abspath(startpath)
    output_file = os.path.join(
        os.getcwd(),
        f"directory_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("DIRECTORY LIST REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"Scan root: {startpath}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        for root, dirs, files in os.walk(startpath):
            dirs.sort()
            files.sort()

            level = root.replace(startpath, "").count(os.sep)
            indent = " " * 4 * level

            try:
                root_stat = os.stat(root)
                root_time = format_timestamp(root_stat.st_mtime)
            except Exception:
                root_time = "UNKNOWN_TIME"

            f.write(f"{indent}[DIR ] [MOD: {root_time}] {root}\n")

            subindent = " " * 4 * (level + 1)
            for name in files:
                full_path = os.path.join(root, name)
                try:
                    st = os.stat(full_path)
                    mod_time = format_timestamp(st.st_mtime)
                    size_text = format_size(st.st_size)
                except Exception:
                    mod_time = "UNKNOWN_TIME"
                    size_text = "UNKNOWN_SIZE"

                ext = os.path.splitext(name)[1].lower() or "[no_ext]"
                f.write(
                    f"{subindent}[FILE] [MOD: {mod_time}] [SIZE: {size_text:>10}] "
                    f"[EXT: {ext}] {full_path}\n"
                )

    print(f"Created: {output_file}")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    list_files_and_folders(target)
