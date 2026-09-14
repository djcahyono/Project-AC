import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod


# =====================================================================
# OOP Principle: Abstraction — Abstract Base for Facility Panels
# =====================================================================
class BaseFacilityPanel(ABC):
    """
    Abstract Base Class for all top-level facility management panels.
    Demonstrates:
    - Abstraction: Enforces a uniform setup_ui() / load_data() contract.
    - Encapsulation: Theme palette stored as instance attributes, not globals.
    - Template Method Pattern: __init__ calls setup_ui() then load_data() in order.
    - Inheritance & Polymorphism: AdminPanelUI inherits this and overrides both methods.
    """

    # Persona 3 Reload Dark Hour Palette — shared by all subclasses (Class Variable)
    DEFAULT_THEME = {
        "bg":           "#070A12",
        "card_bg":      "#0D1322",
        "header_bg":    "#00A2FF",
        "text_primary": "#FFFFFF",
        "text_muted":   "#38BDF8",
        "accent_cyan":  "#00D2FF",
        "danger_red":   "#FF2A42",
        "warning_amber":"#F59E0B",
        "success_cyan": "#00FFCC",
    }

    def __init__(self, parent_root, data_provider, title, geometry, on_close_callback=None):
        self.root = parent_root
        self.data_provider = data_provider
        self.on_close_callback = on_close_callback

        # Encapsulated theme properties from class-level palette
        theme = self.DEFAULT_THEME
        self.bg           = theme["bg"]
        self.card_bg      = theme["card_bg"]
        self.header_bg    = theme["header_bg"]
        self.text_primary = theme["text_primary"]
        self.text_muted   = theme["text_muted"]
        self.accent_cyan  = theme["accent_cyan"]
        self.danger_red   = theme["danger_red"]
        self.warning_amber= theme["warning_amber"]
        self.success_cyan = theme["success_cyan"]

        self.window = tk.Toplevel(self.root)
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.minsize(900, 560)
        self.window.transient(self.root)
        self.window.grab_set()
        self.window.configure(bg=self.bg)

        # Template Method: subclass must implement these two lifecycle steps
        self.setup_ui()
        self.load_data()

    @abstractmethod
    def setup_ui(self):
        """Polymorphic UI layout — each panel builds its own interface."""
        pass

    @abstractmethod
    def load_data(self):
        """Polymorphic data loading — each panel fetches its own dataset."""
        pass


class AdminPanelUI(BaseFacilityPanel):
    """
    Persona 3 Reload styled Admin Panel for managing school AC facility incident reports.
    Demonstrates Inheritance: extends BaseFacilityPanel.
    Demonstrates Polymorphism: overrides setup_ui() and load_data() with admin-specific logic.
    """

    def __init__(self, parent_root, data_provider, on_close_callback=None):
        self.status_filter_var = tk.StringVar(value="ALL")
        self.room_filter_var = tk.StringVar(value="ALL")
        # Calls BaseFacilityPanel.__init__ → setup_ui() → load_data() via Template Method
        super().__init__(
            parent_root, data_provider,
            title="SEES CENTRAL COMMAND // ADMIN FACILITY PANEL",
            geometry="1100x680",
            on_close_callback=on_close_callback
        )

    def load_data(self):
        """Polymorphic implementation: loads incident reports from the database."""
        self.load_reports()



    def setup_ui(self):
        # 1. Top Header Banner
        self.header_frame = tk.Frame(self.window, bg=self.header_bg, height=64)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        header_left = tk.Frame(self.header_frame, bg=self.header_bg)
        header_left.pack(side="left", padx=20, pady=8)

        tk.Label(
            header_left, text="✦ SEES CENTRAL COMMAND // MARSUDIRINI AC ADMIN PANEL",
            font=("Segoe UI", 14, "bold"), bg=self.header_bg, fg="#000000"
        ).pack(anchor="w")

        tk.Label(
            header_left, text="管理者パネル // 施設報告履歴  •  INCIDENT TRACKING & RESOLUTION PROTOCOL",
            font=("Segoe UI", 8, "bold"), bg=self.header_bg, fg="#062544"
        ).pack(anchor="w")

        header_right = tk.Frame(self.header_frame, bg=self.header_bg)
        header_right.pack(side="right", padx=20)

        tk.Button(
            header_right, text="✕ CLOSE", command=self.close,
            bg="#000000", fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=1, relief="solid", padx=14, pady=5, cursor="hand2"
        ).pack()

        # 2. Metric Cards Strip
        self.metrics_strip = tk.Frame(self.window, bg=self.bg)
        self.metrics_strip.pack(fill="x", padx=20, pady=(16, 10))

        self.metric_labels = {}
        cards = [
            ("TOTAL TICKETS", "total", self.accent_cyan),
            ("PENDING ACTION", "pending", self.danger_red),
            ("IN PROGRESS", "in_progress", self.warning_amber),
            ("RESOLVED", "resolved", self.success_cyan),
        ]

        for title, key, color in cards:
            c_frame = tk.Frame(self.metrics_strip, bg=self.card_bg, highlightbackground=color, highlightthickness=1)
            c_frame.pack(side="left", expand=True, fill="both", padx=6)

            tk.Label(
                c_frame, text=title, font=("Segoe UI", 8, "bold"),
                bg=self.card_bg, fg=self.text_muted
            ).pack(anchor="w", padx=14, pady=(8, 0))

            val_lbl = tk.Label(
                c_frame, text="0", font=("Segoe UI", 18, "bold"),
                bg=self.card_bg, fg=color
            )
            val_lbl.pack(anchor="w", padx=14, pady=(0, 8))
            self.metric_labels[key] = val_lbl

        # 3. Filter Controls Bar
        filter_bar = tk.Frame(self.window, bg=self.card_bg, highlightbackground="#1E293B", highlightthickness=1)
        filter_bar.pack(fill="x", padx=24, pady=(4, 12))

        tk.Label(
            filter_bar, text="FILTER STATUS:", font=("Segoe UI", 9, "bold"),
            bg=self.card_bg, fg=self.text_muted
        ).pack(side="left", padx=(14, 6), pady=8)

        status_menu = ttk.Combobox(
            filter_bar, textvariable=self.status_filter_var, width=14, state="readonly",
            values=["ALL", "PENDING", "IN PROGRESS", "RESOLVED"]
        )
        status_menu.pack(side="left", padx=4, pady=8)
        status_menu.bind("<<ComboboxSelected>>", lambda e: self.load_reports())

        tk.Label(
            filter_bar, text="FILTER ROOM:", font=("Segoe UI", 9, "bold"),
            bg=self.card_bg, fg=self.text_muted
        ).pack(side="left", padx=(18, 6), pady=8)

        # Get room list
        rooms = ["ALL"]
        all_rooms = self.data_provider.getReports()
        room_names = sorted(list({r["roomName"] for r in all_rooms if r.get("roomName")}))
        rooms.extend(room_names)

        self.room_menu = ttk.Combobox(
            filter_bar, textvariable=self.room_filter_var, width=14, state="readonly",
            values=rooms
        )
        self.room_menu.pack(side="left", padx=4, pady=8)
        self.room_menu.bind("<<ComboboxSelected>>", lambda e: self.load_reports())

        tk.Button(
            filter_bar, text="⟳ REFRESH", command=self.load_reports,
            bg="#0F172A", fg=self.accent_cyan, font=("Segoe UI", 8, "bold"),
            bd=1, relief="solid", highlightbackground=self.accent_cyan, padx=12, pady=3, cursor="hand2"
        ).pack(side="left", padx=16)

        # 4. Table Frame (Treeview)
        table_frame = tk.Frame(self.window, bg=self.bg)
        table_frame.pack(fill="both", expand=True, padx=24, pady=4)

        # Style Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "P3.Treeview",
            background="#0A0E18",
            foreground="#FFFFFF",
            fieldbackground="#0A0E18",
            rowheight=28,
            font=("Segoe UI", 9)
        )
        style.configure(
            "P3.Treeview.Heading",
            background="#0F1B2E",
            foreground="#00D2FF",
            font=("Segoe UI", 9, "bold"),
            relief="solid"
        )
        style.map("P3.Treeview", background=[("selected", "#005580")], foreground=[("selected", "#FFFFFF")])

        columns = ("id", "date", "room", "ac", "issue", "reporter", "status", "desc")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="P3.Treeview", selectmode="browse")

        self.tree.heading("id", text="# ID")
        self.tree.heading("date", text="TIMESTAMP")
        self.tree.heading("room", text="ROOM")
        self.tree.heading("ac", text="AC UNIT")
        self.tree.heading("issue", text="ISSUE CATEGORY")
        self.tree.heading("reporter", text="REPORTER")
        self.tree.heading("status", text="STATUS")
        self.tree.heading("desc", text="DESCRIPTION")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("date", width=140, anchor="center")
        self.tree.column("room", width=90, anchor="center")
        self.tree.column("ac", width=90, anchor="center")
        self.tree.column("issue", width=160, anchor="w")
        self.tree.column("reporter", width=110, anchor="w")
        self.tree.column("status", width=110, anchor="center")
        self.tree.column("desc", width=300, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 5. Action Toolbar at Bottom
        action_bar = tk.Frame(self.window, bg=self.bg)
        action_bar.pack(fill="x", padx=24, pady=14)

        tk.Button(
            action_bar, text="⏳ MARK IN PROGRESS", command=lambda: self.update_selected_status("IN PROGRESS"),
            bg=self.warning_amber, fg="#000000", font=("Segoe UI", 9, "bold"),
            bd=1, relief="solid", padx=16, pady=6, cursor="hand2"
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            action_bar, text="✔ MARK RESOLVED", command=lambda: self.update_selected_status("RESOLVED"),
            bg=self.success_cyan, fg="#000000", font=("Segoe UI", 9, "bold"),
            bd=1, relief="solid", padx=16, pady=6, cursor="hand2"
        ).pack(side="left", padx=8)

        tk.Button(
            action_bar, text="⚠ SET PENDING", command=lambda: self.update_selected_status("PENDING"),
            bg=self.danger_red, fg="#FFFFFF", font=("Segoe UI", 9, "bold"),
            bd=1, relief="solid", padx=16, pady=6, cursor="hand2"
        ).pack(side="left", padx=8)

        tk.Button(
            action_bar, text="🗑 DELETE REPORT", command=self.delete_selected,
            bg="#1E293B", fg="#EF4444", font=("Segoe UI", 9, "bold"),
            bd=1, relief="solid", padx=14, pady=6, cursor="hand2"
        ).pack(side="left", padx=16)

    def load_reports(self):
        # Update metrics
        stats = self.data_provider.getReportStats()
        for k in ["total", "pending", "in_progress", "resolved"]:
            if k in self.metric_labels:
                self.metric_labels[k].config(text=str(stats.get(k, 0)))

        # Fetch filtered reports
        status_filter = self.status_filter_var.get()
        room_filter = self.room_filter_var.get()

        reports = self.data_provider.getReports(
            statusFilter=status_filter if status_filter != "ALL" else None,
            roomFilter=room_filter if room_filter != "ALL" else None,
        )

        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in reports:
            self.tree.insert("", "end", values=(
                f"#{r['id']}",
                r.get("createdAt", "-"),
                r.get("roomName", "-"),
                r.get("acId", "-"),
                r.get("issueType", "-"),
                r.get("reporterName", "Anonymous"),
                r.get("status", "PENDING"),
                r.get("description", "-"),
            ))

    def get_selected_report_id(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Ticket", "Please select a report ticket from the list first.", parent=self.window)
            return None
        item = self.tree.item(selected[0])
        val = item["values"][0]
        try:
            return int(str(val).replace("#", ""))
        except ValueError:
            return None

    def update_selected_status(self, new_status):
        rep_id = self.get_selected_report_id()
        if not rep_id:
            return
        self.data_provider.updateReportStatus(rep_id, new_status)
        self.load_reports()

    def delete_selected(self):
        rep_id = self.get_selected_report_id()
        if not rep_id:
            return
        if messagebox.askyesno("Confirm Delete", f"Delete ticket #{rep_id} permanently?", parent=self.window):
            self.data_provider.deleteReport(rep_id)
            self.load_reports()

    def close(self):
        self.window.destroy()
        if self.on_close_callback:
            self.on_close_callback()