#!/usr/bin/env python3
# =============================================================================
# FILENAME:      iron_gardener_ui_v0_3_r1_color_list.py
# PROGRAM_NAME:  Iron Gardener UI
# FOLDER PATH:   /userdata/system/ultramode/modules/tools/iron_gardener/
# DESTINATION:   /userdata/system/ultramode/modules/tools/iron_gardener/iron_gardener_ui.py
# VERSION:       v0.3
# REVISION:      r1
# SUMMARY:       Colorful family/branch review UI for Iron Gardener grouped scan data.
# DATE:          2026-04-09 08:35
# AUTHOR:        ChatGPT + Paul
# Hi Mom.
# =============================================================================

from __future__ import annotations
import json
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

DEFAULT_ROOT = Path("/userdata/system/ultramode/modules/tools/iron_gardener/reports")

STAGE_COLORS = {
    "KEEP": "#1f7a1f",
    "REVIEW": "#b36b00",
    "ARCHIVE": "#666666",
    "LOST_INTELLIGENCE": "#6d28d9",
    "TROUBLE": "#b00020",
    "DUPLICATE": "#005bbb",
}

STAGE_LAMPS = {
    "KEEP": "🟢",
    "REVIEW": "🟠",
    "ARCHIVE": "⚪",
    "LOST_INTELLIGENCE": "🟣",
    "TROUBLE": "🔴",
    "DUPLICATE": "🔵",
}

class IronGardenerUI:
    def __init__(self, root, initial=None):
        self.root = root
        self.root.title("Iron Gardener — Color List UI")
        self.root.geometry("1480x860")
        self.report = {}
        self.groups = []
        self.filtered_groups = []
        self._build_ui()
        if initial and initial.exists():
            self.load_report(initial)
        else:
            auto = self.find_latest_grouped_report()
            if auto:
                self.load_report(auto)

    def _build_ui(self):
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        top = ttk.Frame(self.root, padding=8)
        top.grid(row=0, column=0, columnspan=3, sticky="ew")
        top.grid_columnconfigure(6, weight=1)

        ttk.Button(top, text="Open Report", command=self.pick_report).grid(row=0, column=0, padx=4)
        ttk.Button(top, text="Refresh", command=self.refresh_view).grid(row=0, column=1, padx=4)

        ttk.Label(top, text="Branch").grid(row=0, column=2, padx=(12,4))
        self.branch_var = tk.StringVar(value="ALL")
        self.branch_box = ttk.Combobox(top, textvariable=self.branch_var, state="readonly", width=24)
        self.branch_box.grid(row=0, column=3, padx=4)
        self.branch_box.bind("<<ComboboxSelected>>", lambda _e: self.refresh_view())

        ttk.Label(top, text="Stage").grid(row=0, column=4, padx=(12,4))
        self.stage_var = tk.StringVar(value="ALL")
        self.stage_box = ttk.Combobox(top, textvariable=self.stage_var, state="readonly", width=20)
        self.stage_box.grid(row=0, column=5, padx=4)
        self.stage_box.bind("<<ComboboxSelected>>", lambda _e: self.refresh_view())

        self.path_var = tk.StringVar(value="No report loaded")
        ttk.Label(top, textvariable=self.path_var).grid(row=0, column=6, sticky="ew", padx=(12,0))

        left = ttk.Frame(self.root, padding=(8,0,6,8))
        left.grid(row=1, column=0, sticky="nsw")
        left.grid_rowconfigure(1, weight=1)
        ttk.Label(left, text="Branches").grid(row=0, column=0, sticky="w")
        self.branch_list = tk.Listbox(left, width=26, height=40, exportselection=False)
        self.branch_list.grid(row=1, column=0, sticky="ns")
        self.branch_list.bind("<<ListboxSelect>>", self.branch_from_list)

        middle = ttk.Frame(self.root, padding=(0,0,6,8))
        middle.grid(row=1, column=1, sticky="nsew")
        middle.grid_rowconfigure(1, weight=1)
        middle.grid_columnconfigure(0, weight=1)

        ttk.Label(middle, text="Colorful Group List").grid(row=0, column=0, sticky="w")
        cols = ("lamp", "family", "branch", "count", "newest", "top_stage")
        self.tree = ttk.Treeview(middle, columns=cols, show="headings", height=28)
        self.tree.grid(row=1, column=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_group_select)

        for col, width in [("lamp", 60), ("family", 220), ("branch", 170), ("count", 70), ("newest", 170), ("top_stage", 180)]:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=width, anchor="w")

        y1 = ttk.Scrollbar(middle, orient="vertical", command=self.tree.yview)
        y1.grid(row=1, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=y1.set)

        right = ttk.Frame(self.root, padding=(0,0,8,8))
        right.grid(row=1, column=2, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self.detail_var = tk.StringVar(value="Inspector")
        ttk.Label(right, textvariable=self.detail_var).grid(row=0, column=0, sticky="w")

        text_wrap = ttk.Frame(right)
        text_wrap.grid(row=1, column=0, sticky="nsew")
        text_wrap.grid_columnconfigure(0, weight=1)
        text_wrap.grid_rowconfigure(0, weight=1)

        self.text = tk.Text(text_wrap, wrap="word", font=("TkDefaultFont", 11))
        self.text.grid(row=0, column=0, sticky="nsew")
        y2 = ttk.Scrollbar(text_wrap, orient="vertical", command=self.text.yview)
        y2.grid(row=0, column=1, sticky="ns")
        self.text.configure(yscrollcommand=y2.set)

        self.text.tag_configure("head", font=("TkDefaultFont", 12, "bold"))
        self.text.tag_configure("good", foreground=STAGE_COLORS["KEEP"])
        self.text.tag_configure("review", foreground=STAGE_COLORS["REVIEW"])
        self.text.tag_configure("archive", foreground=STAGE_COLORS["ARCHIVE"])
        self.text.tag_configure("lost", foreground=STAGE_COLORS["LOST_INTELLIGENCE"])
        self.text.tag_configure("trouble", foreground=STAGE_COLORS["TROUBLE"])
        self.text.tag_configure("dup", foreground=STAGE_COLORS["DUPLICATE"])

        bottom = ttk.Frame(self.root, padding=8)
        bottom.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.status_var = tk.StringVar(value="READY")
        ttk.Label(bottom, textvariable=self.status_var).grid(row=0, column=0, sticky="w")

    def find_latest_grouped_report(self):
        if not DEFAULT_ROOT.exists():
            return None
        files = sorted(DEFAULT_ROOT.glob("iron_gardener_v2_grouped_report_*.json"))
        return files[-1] if files else None

    def pick_report(self):
        chosen = filedialog.askopenfilename(
            title="Open Iron Gardener grouped report",
            initialdir=str(DEFAULT_ROOT),
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if chosen:
            self.load_report(Path(chosen))

    def load_report(self, path):
        try:
            self.report = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            messagebox.showerror("Load Error", str(exc))
            return
        self.groups = self.report.get("groups", [])
        self.path_var.set(str(path))
        self.populate_filters()
        self.populate_branches()
        self.refresh_view()
        self.status_var.set("LOADED: " + path.name)

    def populate_filters(self):
        branches = ["ALL"] + sorted({g["branch"] for g in self.groups})
        stages = ["ALL"] + sorted({stage for g in self.groups for stage in g.get("stages", {}).keys()})
        self.branch_box["values"] = branches
        self.stage_box["values"] = stages
        if self.branch_var.get() not in branches:
            self.branch_var.set("ALL")
        if self.stage_var.get() not in stages:
            self.stage_var.set("ALL")

    def populate_branches(self):
        self.branch_list.delete(0, tk.END)
        self.branch_list.insert(tk.END, "ALL")
        for b in sorted({g["branch"] for g in self.groups}):
            self.branch_list.insert(tk.END, b)

    def branch_from_list(self, _event=None):
        sel = self.branch_list.curselection()
        if not sel:
            return
        self.branch_var.set(self.branch_list.get(sel[0]))
        self.refresh_view()

    def refresh_view(self):
        branch = self.branch_var.get()
        stage = self.stage_var.get()
        self.tree.delete(*self.tree.get_children())
        self.filtered_groups = []
        for g in self.groups:
            if branch != "ALL" and g["branch"] != branch:
                continue
            if stage != "ALL" and stage not in g.get("stages", {}):
                continue
            self.filtered_groups.append(g)

        for idx, g in enumerate(self.filtered_groups):
            top_stage = self.pick_top_stage(g.get("stages", {}))
            lamp = STAGE_LAMPS.get(top_stage, "•")
            iid = "g" + str(idx)
            self.tree.insert("", "end", iid=iid, values=(lamp, g["family"], g["branch"], g["count"], g["newest"], top_stage), tags=(top_stage,))
        for st in STAGE_COLORS:
            self.tree.tag_configure(st, foreground=STAGE_COLORS[st])

        self.detail_var.set("Inspector")
        self.text.delete("1.0", tk.END)
        self.status_var.set("GROUPS: " + str(len(self.filtered_groups)))

    def pick_top_stage(self, stages):
        if not stages:
            return "REVIEW"
        priority = ["TROUBLE", "LOST_INTELLIGENCE", "DUPLICATE", "ARCHIVE", "REVIEW", "KEEP"]
        for p in priority:
            if p in stages:
                return p
        return next(iter(stages.keys()))

    def on_group_select(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0][1:])
        g = self.filtered_groups[idx]
        self.show_group(g)

    def show_group(self, g):
        self.text.delete("1.0", tk.END)
        self.detail_var.set(g["branch"] + " :: " + g["family"])
        self.write(g["branch"] + " :: " + g["family"] + "\n", "head")
        self.write("COUNT: " + str(g["count"]) + "\n")
        self.write("NEWEST: " + str(g["newest"]) + "\n")
        self.write("STAGES: " + str(g.get("stages", {})) + "\n\n")

        self.write("FILES\n", "head")
        for p in g.get("files", [])[:200]:
            self.write("- " + p + "\n")
        if len(g.get("files", [])) > 200:
            self.write("\n... more files omitted in view ...\n", "review")

        stage_keys = set(g.get("stages", {}).keys())
        if "TROUBLE" in stage_keys:
            self.write("\nACTION HINT: TROUBLE branch — inspect first.\n", "trouble")
        elif "LOST_INTELLIGENCE" in stage_keys:
            self.write("\nACTION HINT: preserve and bundle nearby files.\n", "lost")
        elif "ARCHIVE" in stage_keys:
            self.write("\nACTION HINT: strong archive candidates.\n", "archive")
        elif "DUPLICATE" in stage_keys:
            self.write("\nACTION HINT: compare winners before move.\n", "dup")
        else:
            self.write("\nACTION HINT: review / group / promote.\n", "review")

        self.status_var.set("SELECTED: " + g["branch"] + "::" + g["family"])

    def write(self, text, tag=None):
        if tag:
            self.text.insert(tk.END, text, tag)
        else:
            self.text.insert(tk.END, text)

def main():
    initial = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
    root = tk.Tk()
    IronGardenerUI(root, initial)
    root.mainloop()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
