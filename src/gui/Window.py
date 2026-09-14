import math
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

src_dir = Path(__file__).resolve().parents[1]
project_root = src_dir.parent
for candidate in (str(src_dir), str(project_root)):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

try:
    from gui.animation import CanvasAnimationManager
except ModuleNotFoundError:
    try:
        from src.gui.animation import CanvasAnimationManager
    except ModuleNotFoundError:
        from animation import CanvasAnimationManager

try:
    from gui.adminPanelUi import AdminPanelUI
except ModuleNotFoundError:
    try:
        from src.gui.adminPanelUi import AdminPanelUI
    except ModuleNotFoundError:
        from adminPanelUi import AdminPanelUI

try:
    from dataAndExec.data import RoomDataProvider
except ModuleNotFoundError:
    from src.dataAndExec.data import RoomDataProvider


class ACStatFullScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AC STAT // SEES FACILITY MANAGEMENT - MARSUDIRINI")
        self.root.geometry("1320x840")
        self.root.minsize(1050, 680)

        # State Variables
        self.is_dark = True
        self.current_floor = "Floor 1"
        self.selectedRoom = None

        # Coordinates for rooms per floor
        floor_layout = {
            "Floor 1": [
                {"name": "XII G", "coords": (75, 50, 175, 130)},
                {"name": "XII F", "coords": (75, 150, 175, 230)},
                {"name": "R. Data", "coords": (75, 250, 175, 330)},
                {"name": "XII E", "coords": (175, 350, 275, 430)},
                {"name": "XII D", "coords": (295, 350, 395, 430)},
                {"name": "XII C", "coords": (415, 350, 515, 430)},
                {"name": "XII B", "coords": (535, 350, 635, 430)},
                {"name": "XII A", "coords": (655, 350, 755, 430)},
                {"name": "R. Kepsek", "coords": (755, 90, 855, 190)},
                {"name": "R. TU", "coords": (755, 200, 855, 330)},
            ],
            "Floor 2": [
                {"name": "XII H", "coords": (75, 50, 175, 130)},
                {"name": "XII I", "coords": (75, 150, 175, 230)},
                {"name": "XI G", "coords": (75, 250, 175, 330)},
                {"name": "XI F", "coords": (175, 350, 275, 430)},
                {"name": "XI E", "coords": (295, 350, 395, 430)},
                {"name": "Ruang Guru", "coords": (415, 350, 635, 430)},
                {"name": "XI D", "coords": (655, 350, 755, 430)},
                {"name": "XI A", "coords": (780, 50, 880, 130)},
                {"name": "XI B", "coords": (780, 150, 880, 230)},
                {"name": "XI C", "coords": (780, 250, 880, 330)},
            ],
            "Floor 3": [
                {"name": "XI H", "coords": (75, 50, 175, 130)},
                {"name": "XI I", "coords": (75, 150, 175, 230)},
                {"name": "X A", "coords": (75, 250, 175, 330)},
                {"name": "X B", "coords": (175, 350, 275, 430)},
                {"name": "X C", "coords": (295, 350, 395, 430)},
                {"name": "X D", "coords": (415, 350, 515, 430)},
                {"name": "X E", "coords": (535, 350, 635, 430)},
                {"name": "X F", "coords": (655, 350, 755, 430)},
                {"name": "X I", "coords": (780, 50, 880, 130)},
                {"name": "X H", "coords": (780, 150, 880, 230)},
                {"name": "X G", "coords": (780, 250, 880, 330)},
            ],
            "Floor 4": [
                {"name": "coming soon", "coords": (30, 30, 920, 480)}
            ]
        }
        self.dataProvider = RoomDataProvider()
        self.floorsData = self.dataProvider.getFloorsData(floor_layout)

        # Persona 3 Reload Theme Configuration
        self.themes = {
            "dark": {
                "bg": "#070A12",
                "top_bg": "#00A2FF",
                "top_fg": "#000000",
                "top_sub_fg": "#05203C",
                "card_bg": "#0A0F1D",
                "card_border": "#00D2FF",
                "canvas_bg": "#050811",
                "text": "#FFFFFF",
                "text_secondary": "#94A3B8",
                "muted": "#38BDF8",
                "accent": "#00D2FF",
                "danger": "#FF2A42",
                "btn_bg": "#0A1322",
                "btn_fg": "#FFFFFF",
                "btn_border": "#00A2FF",
                "border": "#1E293B",
                "active_tab_bg": "#00D2FF",
                "active_tab_fg": "#000000",
            },
            "light": {
                "bg": "#F1F5F9",
                "top_bg": "#0095E8",
                "top_fg": "#FFFFFF",
                "top_sub_fg": "#DDF2FF",
                "card_bg": "#FFFFFF",
                "card_border": "#0284C7",
                "canvas_bg": "#E2E8F0",
                "text": "#0F172A",
                "text_secondary": "#475569",
                "muted": "#0284C7",
                "accent": "#0284C7",
                "danger": "#DC2626",
                "btn_bg": "#E2E8F0",
                "btn_fg": "#0F172A",
                "btn_border": "#0284C7",
                "border": "#CBD5E1",
                "active_tab_bg": "#0284C7",
                "active_tab_fg": "#FFFFFF",
            }
        }

        # Load & hold references to Persona 3 image assets
        self.load_p3_assets()

        self.setup_ui()
        self.animator = CanvasAnimationManager(self.canvas, self.root, self.get_current_theme)
        self.reloadFloorMap()
        self.apply_theme()

        # Keyboard shortcuts
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())

    def get_current_theme(self):
        return self.themes["dark"] if self.is_dark else self.themes["light"]

    def load_p3_assets(self):
        assets_dir = project_root / "assets"
        self.p3_images = {}
        file_map = {
            "badge": "Marsudirini_Logo.png",
            "thumb": "p3_classroom_thumb_small.png",
            "character": "p3_character_art_dash.png",
            "thanatos": "p3_thanatos_small.png",
            "moon_star": "p3_moon_star_small.png",
        }
        for key, filename in file_map.items():
            img_path = assets_dir / filename
            if img_path.exists():
                try:
                    if HAS_PIL:
                        image = Image.open(img_path)
                        if key == "badge":
                            image.thumbnail((58, 58), Image.Resampling.LANCZOS)
                        self.p3_images[key] = ImageTk.PhotoImage(image)
                    else:
                        image = tk.PhotoImage(file=str(img_path))
                        if key == "badge":
                            image = image.subsample(max(1, image.width() // 58))
                        self.p3_images[key] = image
                except Exception as e:
                    print(f"Warning loading {filename}: {e}")

    def setup_ui(self):
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)

        # Top Header Bar (Electric Cyan Banner from Reference)
        self.top_bar = tk.Frame(self.main_container, height=76, highlightthickness=1)
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        # Left Header: Marsudirini logo and title
        self.left_box = tk.Frame(self.top_bar)
        self.left_box.pack(side="left", padx=14)

        if "badge" in self.p3_images:
            self.badge_label = tk.Label(self.left_box, image=self.p3_images["badge"], bd=0, relief="flat", highlightthickness=0)
            self.badge_label.pack(side="left", padx=(0, 10))

        self.title_box = tk.Frame(self.left_box)
        self.title_box.pack(side="left", fill="y", pady=8)

        self.app_title = tk.Label(
            self.title_box, text="AC STAT",
            font=("Segoe UI", 18, "bold")
        )
        self.app_title.pack(anchor="w")

        self.app_subtitle = tk.Label(
            self.title_box,
            text="Marsudirini • AC Control",
            font=("Segoe UI", 9, "bold")
        )
        self.app_subtitle.pack(anchor="w")

        # Center Header: Clean & Minimalist (Toned down text art)
        self.center_box = tk.Frame(self.top_bar)
        self.center_box.pack(side="left", expand=True, padx=4)

        self.ticker_top = tk.Label(
            self.center_box,
            text="✦ MARSUDIRINI CLIMATE ✦",
            font=("Segoe UI", 10, "bold")
        )
        self.ticker_top.pack(anchor="center")

        self.ticker_sub = tk.Label(
            self.center_box,
            text="SEES FACILITY MONITOR",
            font=("Segoe UI", 8)
        )
        self.ticker_sub.pack(anchor="center", pady=(1, 0))

        # Right Header: Classroom Thumbnail & Controls
        self.right_box = tk.Frame(self.top_bar)
        self.right_box.pack(side="right", padx=14)

        if "thumb" in self.p3_images:
            self.thumb_label = tk.Label(self.right_box, image=self.p3_images["thumb"], bd=1, relief="solid")
            self.thumb_label.pack(side="left", padx=(0, 10))

        # 1. Report Button (Quick issue report)
        self.btn_report = tk.Button(
            self.right_box, text="⚠ REPORT", font=("Segoe UI", 9, "bold"),
            bg="#F59E0B", fg="#000000", bd=1, relief="solid",
            padx=10, pady=4, cursor="hand2", command=lambda: self.openReportDialog()
        )
        self.btn_report.pack(side="left", padx=4)

        # 2. Admin Panel Button
        self.btn_admin = tk.Button(
            self.right_box, text="🛡 ADMIN", font=("Segoe UI", 9, "bold"),
            bg="#0F172A", fg="#00D2FF", bd=1, relief="solid",
            padx=10, pady=4, cursor="hand2", command=self.openAdminAuthentication
        )
        self.btn_admin.pack(side="left", padx=4)

        # 3. System / Actions Dropdown Menu
        self.menu_btn = tk.Menubutton(
            self.right_box, text="⚙ MENU ▾", font=("Segoe UI", 9, "bold"),
            bg="#000000", fg="#FFFFFF", bd=1, relief="solid",
            padx=10, pady=4, cursor="hand2"
        )
        self.system_menu = tk.Menu(
            self.menu_btn, tearoff=0,
            bg="#0A0F1D", fg="#FFFFFF",
            activebackground="#00A2FF", activeforeground="#000000",
            font=("Segoe UI", 9)
        )
        self.system_menu.add_command(
            label="☀️ Toggle Light / Dark Mode",
            command=self.toggle_theme
        )
        self.system_menu.add_command(
            label="⛶ Toggle Fullscreen (F11)",
            command=self.toggle_fullscreen
        )
        self.system_menu.add_separator()
        self.system_menu.add_command(
            label="🛡 Admin Panel",
            command=self.openAdminAuthentication
        )
        self.system_menu.add_command(
            label="⚠ Report AC Issue",
            command=lambda: self.openReportDialog()
        )
        self.menu_btn["menu"] = self.system_menu
        self.menu_btn.pack(side="left", padx=4)

        # Workspace Area
        self.workspace = tk.Frame(self.main_container)
        self.workspace.pack(fill="both", expand=True, padx=20, pady=(15, 10))

        # Map Area (Left)
        self.map_area = tk.Frame(self.workspace)
        self.map_area.pack(side="left", fill="both", expand=True, padx=(0, 16))

        # Floor Navigation Tabs Frame
        self.floor_tabs_frame = tk.Frame(self.map_area)
        self.floor_tabs_frame.pack(fill="x", pady=(0, 12))

        # Persona 3 Reload Styled Floor Command Tabs
        self.btn_floor1 = tk.Button(
            self.floor_tabs_frame, text="✦ 01 FLOOR", font=("Segoe UI", 10, "bold"),
            bd=1, relief="solid", padx=18, pady=6, cursor="hand2",
            command=lambda: self.changeFloor("Floor 1")
        )
        self.btn_floor1.pack(side="left", padx=(0, 8))

        self.btn_floor2 = tk.Button(
            self.floor_tabs_frame, text="✦ 02 FLOOR", font=("Segoe UI", 10, "bold"),
            bd=1, relief="solid", padx=18, pady=6, cursor="hand2",
            command=lambda: self.changeFloor("Floor 2")
        )
        self.btn_floor2.pack(side="left", padx=(0, 8))

        self.btn_floor3 = tk.Button(
            self.floor_tabs_frame, text="✦ 03 FLOOR", font=("Segoe UI", 10, "bold"),
            bd=1, relief="solid", padx=18, pady=6, cursor="hand2",
            command=lambda: self.changeFloor("Floor 3")
        )
        self.btn_floor3.pack(side="left", padx=(0, 8))

        self.btn_floor4 = tk.Button(
            self.floor_tabs_frame, text="✦ 04 FLOOR", font=("Segoe UI", 10, "bold"),
            bd=1, relief="solid", padx=18, pady=6, cursor="hand2",
            command=lambda: self.changeFloor("Floor 4")
        )
        self.btn_floor4.pack(side="left")

        # Map Canvas
        self.canvas = tk.Canvas(self.map_area, highlightthickness=1)
        self.canvas.pack(fill="both", expand=True)

        # Right Side Dashboard / Preview Panel
        self.preview_card = tk.Frame(self.workspace, width=310, highlightthickness=1)
        self.preview_card.pack_propagate(False)
        self.preview_card.pack(side="right", fill="y")

        self.setup_dashboard_card()

        # Footer Ticker Bar
        self.footer = tk.Label(
            self.main_container,
            text="[ESC] Windowed  |  [F11] Fullscreen  |  SEES HVAC CLIMATE PROTOCOL ACTIVE  •  MARSUDIRINI ONLINE",
            font=("Segoe UI", 9)
        )
        self.footer.pack(side="bottom", anchor="w", padx=20, pady=6)

    def setup_dashboard_card(self):
        # Header Box
        self.dash_header_frame = tk.Frame(self.preview_card)
        self.dash_header_frame.pack(fill="x", padx=16, pady=(14, 4))

        self.dashboard_title = tk.Label(
            self.dash_header_frame, text="FLOOR SUMMARY",
            font=("Segoe UI", 11, "bold")
        )
        self.dashboard_title.pack(anchor="w")

        self.dashboard_sub = tk.Label(
            self.dash_header_frame, text="memento mori  •  memento vivere",
            font=("Segoe UI", 8, "italic")
        )
        self.dashboard_sub.pack(anchor="w", pady=(1, 0))

        self.dashboard_floor = tk.Label(
            self.dash_header_frame, text="",
            font=("Segoe UI", 13, "bold")
        )
        self.dashboard_floor.pack(anchor="w", pady=(4, 0))

        # Dashboard Canvas for Donut, Gauges, and Art
        self.dashboard_canvas = tk.Canvas(self.preview_card, highlightthickness=0)
        self.dashboard_canvas.pack(fill="both", expand=True, padx=4, pady=(2, 6))

    def reloadFloorMap(self):
        self.canvas.delete("all")
        floorData = self.floorsData[self.current_floor]
        self.animator.drawFloorItems(
            floorData, self.current_floor,
            hoverCallback=self.onRoomHover,
            clickCallback=self.onRoomClick
        )

    def changeFloor(self, targetFloor):
        if self.animator.isAnimating:
            return

        if self.animator.isInRoomMenu:
            self.animator.zoomOutRoomView(lambda: self.changeFloorAfterRoom(targetFloor))
            return

        if self.current_floor == targetFloor:
            return

        self.changeFloorAfterRoom(targetFloor)

    def changeFloorAfterRoom(self, targetFloor):
        if self.current_floor == targetFloor:
            self.reloadFloorMap()
            return

        current_floor_number = int(self.current_floor.split()[-1])
        target_floor_number = int(targetFloor.split()[-1])
        direction = "up" if target_floor_number > current_floor_number else "down"
        self.current_floor = targetFloor
        self.updateFloorSelection()
        if hasattr(self, "dashboard_canvas"):
            self.updateDashboard()
        self.animator.changeFloorSlide(
            self.floorsData[targetFloor], targetFloor,
            direction,
            hoverCallback=self.onRoomHover,
            clickCallback=self.onRoomClick,
            onComplete=self.updateDashboard
        )

    def onRoomHover(self, roomData, entering):
        self.animator.hoverZoom(roomData, entering)
        if entering:
            self.updatePreview(roomData)
        else:
            self.clearPreview()

    def onRoomClick(self, roomData):
        self.selectedRoom = roomData
        self.animator.zoomIntoRoom(roomData, onCompleteCallback=self.openRoomMenu)

    def openRoomMenu(self, roomData):
        self.animator.drawRoomMenuOverlay(
            roomData,
            backCallback=self.returnToCurrentFloor,
            editCallback=lambda: self.openEditAuthentication(roomData),
            reportCallback=lambda r, ac=None: self.openReportDialog(r, ac),
        )

    def openReportDialog(self, roomData=None, defaultAc=None):
        # Open the incident reporting modal.
        theme = self.get_current_theme()
        dialog = tk.Toplevel(self.root)
        dialog.title("SEES INCIDENT REPORT // MARSUDIRINI AC")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.configure(bg=theme["card_bg"])

        # Header
        header = tk.Frame(dialog, bg=theme["top_bg"], height=42)
        header.pack(fill="x")
        tk.Label(
            header, text="✦ SEES INCIDENT REPORT // MARSUDIRINI AC FACILITY",
            font=("Segoe UI", 11, "bold"), bg=theme["top_bg"], fg=theme["top_fg"]
        ).pack(side="left", padx=16, pady=10)

        body = tk.Frame(dialog, bg=theme["card_bg"])
        body.pack(padx=28, pady=20)

        # Collect all classroom names
        all_room_names = []
        for rooms in self.floorsData.values():
            for r in rooms:
                if r.get("name") and r["name"].lower() != "coming soon":
                    if r["name"] not in all_room_names:
                        all_room_names.append(r["name"])

        init_room = roomData["name"] if roomData and roomData.get("name") else (all_room_names[0] if all_room_names else "")

        entry_bg = "#111827" if self.is_dark else "#FFFFFF"

        # 1. Room Name
        tk.Label(body, text="LOCATION / ROOM:", font=("Segoe UI", 9, "bold"), bg=theme["card_bg"], fg=theme["muted"]).grid(row=0, column=0, sticky="w", pady=6)
        room_var = tk.StringVar(value=init_room)
        room_combo = ttk.Combobox(body, textvariable=room_var, values=all_room_names, width=28, state="readonly")
        room_combo.grid(row=0, column=1, pady=6, padx=(10, 0))

        # 2. AC Unit
        init_ac = defaultAc or "All AC Units"
        tk.Label(body, text="AC UNIT ID:", font=("Segoe UI", 9, "bold"), bg=theme["card_bg"], fg=theme["muted"]).grid(row=1, column=0, sticky="w", pady=6)
        ac_var = tk.StringVar(value=init_ac)
        ac_combo = ttk.Combobox(body, textvariable=ac_var, values=["All AC Units", "AC-01", "AC-02", "AC-03"], width=28)
        ac_combo.grid(row=1, column=1, pady=6, padx=(10, 0))

        # 3. Issue Category
        tk.Label(body, text="ISSUE CATEGORY:", font=("Segoe UI", 9, "bold"), bg=theme["card_bg"], fg=theme["muted"]).grid(row=2, column=0, sticky="w", pady=6)
        issues = [
            "AC Not Cold / Kurang Dingin",
            "Water Leaking / Bocor Air",
            "Remote Missing / Rusak",
            "Strange Noise / Suara Bising",
            "Power Failure / Mati Total",
            "Foul Smell / Bau Kurang Sedap",
            "Other / Masalah Lain"
        ]
        issue_var = tk.StringVar(value=issues[0])
        issue_combo = ttk.Combobox(body, textvariable=issue_var, values=issues, width=28, state="readonly")
        issue_combo.grid(row=2, column=1, pady=6, padx=(10, 0))

        # 4. Reporter Name
        tk.Label(body, text="REPORTER NAME:", font=("Segoe UI", 9, "bold"), bg=theme["card_bg"], fg=theme["muted"]).grid(row=3, column=0, sticky="w", pady=6)
        reporter_entry = tk.Entry(body, width=30, font=("Segoe UI", 10), bg=entry_bg, fg=theme["text"], insertbackground=theme["accent"])
        reporter_entry.insert(0, "Student / Staff")
        reporter_entry.grid(row=3, column=1, pady=6, padx=(10, 0))

        # 5. Description
        tk.Label(body, text="DESCRIPTION / NOTES:", font=("Segoe UI", 9, "bold"), bg=theme["card_bg"], fg=theme["muted"]).grid(row=4, column=0, sticky="nw", pady=6)
        desc_text = tk.Text(body, width=30, height=4, font=("Segoe UI", 9), bg=entry_bg, fg=theme["text"], insertbackground=theme["accent"])
        desc_text.grid(row=4, column=1, pady=6, padx=(10, 0))

        status_lbl = tk.Label(body, text="", font=("Segoe UI", 9, "bold"), bg=theme["card_bg"], fg=theme["accent"])
        status_lbl.grid(row=5, column=0, columnspan=2, pady=4)

        def submit():
            r_name = room_var.get()
            a_id = ac_var.get()
            i_type = issue_var.get()
            rep_name = reporter_entry.get().strip() or "Anonymous"
            desc = desc_text.get("1.0", tk.END).strip()

            if not desc:
                status_lbl.configure(text="Please enter description details.", fg=theme["danger"])
                return

            try:
                ticket_id = self.dataProvider.createReport(r_name, a_id, i_type, desc, rep_name)
                status_lbl.configure(text=f"REPORT LOGGED! TICKET #{ticket_id}", fg="#00FFCC")
                dialog.after(900, dialog.destroy)
            except Exception as ex:
                status_lbl.configure(text=f"Error saving report: {ex}", fg=theme["danger"])

        btn_box = tk.Frame(body, bg=theme["card_bg"])
        btn_box.grid(row=6, column=0, columnspan=2, pady=(12, 0))

        tk.Button(
            btn_box, text="✦ SUBMIT REPORT", command=submit,
            bg=theme["accent"], fg="#000000" if self.is_dark else "#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=16, pady=6, cursor="hand2"
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btn_box, text="CANCEL", command=dialog.destroy,
            bg=theme["btn_bg"], fg=theme["btn_fg"],
            font=("Segoe UI", 9), bd=1, relief="solid", padx=14, pady=6, cursor="hand2"
        ).pack(side="left")

    def openAdminAuthentication(self):
        # Authenticate the administrator and launch AdminPanelUI.
        theme = self.get_current_theme()
        dialog = tk.Toplevel(self.root)
        dialog.title("ADMIN AUTHENTICATION // SEES CENTRAL")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.configure(bg=theme["card_bg"])

        header = tk.Frame(dialog, bg=theme["top_bg"], height=36)
        header.pack(fill="x")
        tk.Label(
            header, text="✦ SEES ADMIN ACCESS VERIFICATION",
            font=("Segoe UI", 10, "bold"), bg=theme["top_bg"], fg=theme["top_fg"]
        ).pack(side="left", padx=16, pady=8)

        body = tk.Frame(dialog, bg=theme["card_bg"])
        body.pack(padx=28, pady=20)

        tk.Label(
            body, text="Enter administrator access key (default: admin123):",
            font=("Segoe UI", 10), bg=theme["card_bg"], fg=theme["text"]
        ).pack(anchor="w", pady=(0, 8))

        password_entry = tk.Entry(
            body, show="*", width=30, font=("Segoe UI", 10),
            bg="#111827" if self.is_dark else "#FFFFFF",
            fg=theme["text"], insertbackground=theme["accent"]
        )
        password_entry.pack(fill="x", pady=4)
        password_entry.focus_set()

        error_label = tk.Label(body, text="", fg=theme["danger"], bg=theme["card_bg"], font=("Segoe UI", 9))
        error_label.pack(pady=4)

        def verify():
            pwd = password_entry.get()
            if self.dataProvider.authenticateAdmin(pwd):
                dialog.destroy()
                AdminPanelUI(self.root, self.dataProvider)
            else:
                error_label.configure(text="ACCESS DENIED: Invalid Admin Passkey")
                password_entry.select_range(0, tk.END)
                password_entry.focus_set()

        btn_box = tk.Frame(body, bg=theme["card_bg"])
        btn_box.pack(fill="x", pady=(10, 0))

        tk.Button(
            btn_box, text="UNLOCK ADMIN PANEL", command=verify,
            bg=theme["accent"], fg="#000000" if self.is_dark else "#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=16, pady=6, cursor="hand2"
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btn_box, text="CANCEL", command=dialog.destroy,
            bg=theme["btn_bg"], fg=theme["btn_fg"],
            font=("Segoe UI", 9), bd=1, relief="solid", padx=14, pady=6, cursor="hand2"
        ).pack(side="left")

        password_entry.bind("<Return>", lambda event: verify())

    def openEditAuthentication(self, roomData):
        theme = self.get_current_theme()
        dialog = tk.Toplevel(self.root)
        dialog.title(f"AUTHENTICATION // {roomData['name']}")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.configure(bg=theme["card_bg"])

        # Styled header
        header = tk.Frame(dialog, bg=theme["top_bg"], height=36)
        header.pack(fill="x")
        tk.Label(
            header, text=f"SEES SECURITY CHECK // {roomData['name']}",
            font=("Segoe UI", 10, "bold"), bg=theme["top_bg"], fg=theme["top_fg"]
        ).pack(side="left", padx=16, pady=8)

        body = tk.Frame(dialog, bg=theme["card_bg"])
        body.pack(padx=28, pady=20)

        tk.Label(
            body, text=f"Enter security passkey for {roomData['name']}:",
            font=("Segoe UI", 10), bg=theme["card_bg"], fg=theme["text"]
        ).pack(anchor="w", pady=(0, 8))

        password_entry = tk.Entry(
            body, show="*", width=30, font=("Segoe UI", 10),
            bg="#111827" if self.is_dark else "#FFFFFF",
            fg=theme["text"], insertbackground=theme["accent"]
        )
        password_entry.pack(fill="x", pady=4)
        password_entry.focus_set()

        error_label = tk.Label(body, text="", fg=theme["danger"], bg=theme["card_bg"], font=("Segoe UI", 9))
        error_label.pack(pady=4)

        def authenticate():
            if self.dataProvider.authenticateRoom(roomData["name"], password_entry.get()):
                dialog.destroy()
                self.openRoomEditor(roomData)
            else:
                error_label.configure(text="ACCESS DENIED: Incorrect passkey")
                password_entry.select_range(0, tk.END)
                password_entry.focus_set()

        btn_box = tk.Frame(body, bg=theme["card_bg"])
        btn_box.pack(fill="x", pady=(10, 0))

        tk.Button(
            btn_box, text="VERIFY & CONTINUE", command=authenticate,
            bg=theme["accent"], fg="#000000" if self.is_dark else "#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=16, pady=6, cursor="hand2"
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btn_box, text="CANCEL", command=dialog.destroy,
            bg=theme["btn_bg"], fg=theme["btn_fg"],
            font=("Segoe UI", 9), bd=1, relief="solid", padx=14, pady=6, cursor="hand2"
        ).pack(side="left")

        password_entry.bind("<Return>", lambda event: authenticate())

    def openRoomEditor(self, roomData):
        theme = self.get_current_theme()
        dialog = tk.Toplevel(self.root)
        dialog.title(f"EDIT EQUIPMENT // {roomData['name']}")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        dialog.configure(bg=theme["card_bg"])

        # Styled header
        header = tk.Frame(dialog, bg=theme["top_bg"], height=36)
        header.pack(fill="x")
        tk.Label(
            header, text=f"✦ SEES HVAC SYSTEM OVERRIDE // {roomData['name']}",
            font=("Segoe UI", 10, "bold"), bg=theme["top_bg"], fg=theme["top_fg"]
        ).pack(side="left", padx=16, pady=8)

        fields = (
            ("Wall Temperature (°C)", "temp"),
            ("AC Units Count", "jumlahAc"),
            ("AC Brand / Model", "merkAc"),
            ("Remote Count", "remoteCount"),
            ("Remote Brand", "remoteBrand"),
        )
        entries = {}
        form = tk.Frame(dialog, bg=theme["card_bg"])
        form.pack(padx=28, pady=18)

        entry_bg = "#111827" if self.is_dark else "#FFFFFF"

        for row, (label, key) in enumerate(fields):
            tk.Label(
                form, text=label, anchor="w", width=22,
                font=("Segoe UI", 9, "bold"), bg=theme["card_bg"], fg=theme["muted"]
            ).grid(row=row, column=0, padx=(0, 12), pady=6, sticky="w")

            entry = tk.Entry(
                form, width=28, font=("Segoe UI", 10),
                bg=entry_bg, fg=theme["text"], insertbackground=theme["accent"]
            )
            entry.insert(0, "" if roomData.get(key) is None else str(roomData[key]))
            entry.grid(row=row, column=1, pady=6)
            entries[key] = entry

        power_var = tk.StringVar(value=roomData.get("acPower") or "ON")
        tk.Label(
            form, text="AC Power State", anchor="w", width=22,
            font=("Segoe UI", 9, "bold"), bg=theme["card_bg"], fg=theme["muted"]
        ).grid(row=len(fields), column=0, padx=(0, 12), pady=6, sticky="w")

        pwr_menu = tk.OptionMenu(form, power_var, "ON", "OFF")
        pwr_menu.configure(
            bg=entry_bg, fg=theme["text"], activebackground=theme["accent"],
            font=("Segoe UI", 9, "bold"), bd=1, relief="solid"
        )
        pwr_menu.grid(row=len(fields), column=1, sticky="w", pady=6)

        error_label = tk.Label(dialog, text="", fg=theme["danger"], bg=theme["card_bg"], font=("Segoe UI", 9))
        error_label.pack(pady=4)

        def save_changes():
            try:
                values = {
                    "temperature": float(entries["temp"].get()),
                    "acCount": int(entries["jumlahAc"].get()),
                    "acBrand": entries["merkAc"].get(),
                    "remoteCount": int(entries["remoteCount"].get()),
                    "remoteBrand": entries["remoteBrand"].get(),
                    "acPower": power_var.get(),
                }
                editor = self.dataProvider.getRoomEditor(roomData["name"])
                editor.update(**values)
            except (ValueError, PermissionError) as error:
                error_label.configure(text=str(error) or "Invalid input values")
                return

            updated = self.dataProvider.getRoom(roomData["name"])
            roomData.update({
                "temp": updated["temperature"],
                "acPower": updated["acPower"],
                "jumlahAc": updated["acCount"],
                "merkAc": updated["acBrand"],
                "remoteCount": updated["remoteCount"],
                "remoteBrand": updated["remoteBrand"],
            })
            for floor_rooms in self.floorsData.values():
                for floor_room in floor_rooms:
                    if floor_room["name"] == roomData["name"]:
                        floor_room.update(roomData)
            dialog.destroy()
            self.updateDashboard()
            self.animator.drawRoomMenuOverlay(
                roomData,
                backCallback=self.returnToCurrentFloor,
                editCallback=lambda: self.openEditAuthentication(roomData),
                reportCallback=lambda r, ac=None: self.openReportDialog(r, ac),
            )

        btn_box = tk.Frame(dialog, bg=theme["card_bg"])
        btn_box.pack(fill="x", padx=28, pady=(8, 20))

        tk.Button(
            btn_box, text="SAVE CONFIGURATION", command=save_changes,
            bg=theme["accent"], fg="#000000" if self.is_dark else "#FFFFFF",
            font=("Segoe UI", 9, "bold"), bd=1, relief="solid", padx=16, pady=6, cursor="hand2"
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            btn_box, text="CANCEL", command=dialog.destroy,
            bg=theme["btn_bg"], fg=theme["btn_fg"],
            font=("Segoe UI", 9), bd=1, relief="solid", padx=14, pady=6, cursor="hand2"
        ).pack(side="left")

    def returnToCurrentFloor(self):
        if self.animator.isAnimating:
            return
        self.animator.zoomOutRoomView(self.reloadFloorMap)

    def updatePreview(self, roomData):
        self.updateDashboard()

    def clearPreview(self):
        self.updateDashboard()

    def updateDashboard(self):
        theme = self.get_current_theme()
        floor_data = self.floorsData.get(self.current_floor, [])

        # Update Floor Indicator in Dashboard and Header
        floor_num = self.current_floor.split()[-1]
        self.dashboard_floor.configure(text=f"{self.current_floor.upper()}  [*0{floor_num}]")

        self.dashboard_canvas.delete("all")
        canvas_w = max(self.dashboard_canvas.winfo_width(), 300)

        if self.current_floor == "Floor 4":
            self.dashboard_canvas.create_text(
                canvas_w / 2, 100, text="// MARSUDIRINI LEVEL 4 //\nACCESS RESTRICTED",
                fill=theme["muted"], font=("Segoe UI", 12, "bold"), justify="center"
            )
            return

        # Metrics calculation: Focus on classroom / AC-equipped rooms
        ac_rooms = [r for r in floor_data if r.get("hasStats", True)]
        target_rooms = ac_rooms if ac_rooms else floor_data

        status_counts = {"ON": 0, "OFF": 0, "NO DATA": 0}
        temperatures = []
        ac_count = 0

        for room in target_rooms:
            temperature = room.get("temp")
            power = str(room.get("acPower") or "").upper()

            if power == "OFF":
                status_counts["OFF"] += 1
            elif power == "ON":
                status_counts["ON"] += 1
            else:
                status_counts["NO DATA"] += 1

            if temperature is not None:
                temperatures.append(temperature)

            ac_count += room.get("jumlahAc") or 0

        avg_temp_val = (sum(temperatures) / len(temperatures)) if temperatures else 0
        avg_temp_str = f"{avg_temp_val:.1f}°C" if temperatures else "--°C"

        # 1. Donut Chart (P3 Status Arc Gauge — enlarged, no image, more canvas space)
        center_x = canvas_w / 2
        center_y = 90
        radius = 72
        total = sum(status_counts.values())

        color_map = {
            "ON": "#00D2FF",
            "OFF": "#FF2A42",
            "NO DATA": "#475569"
        }

        if total > 0:
            active_slices = [(lbl, cnt) for lbl, cnt in status_counts.items() if cnt > 0]
            if len(active_slices) == 1:
                # All rooms are in one single state (e.g. ALL ON!)
                single_label, single_count = active_slices[0]
                self.dashboard_canvas.create_oval(
                    center_x - radius, center_y - radius,
                    center_x + radius, center_y + radius,
                    fill=color_map[single_label], outline=theme["card_bg"], width=2
                )
            else:
                start_angle = 90
                for label, count in status_counts.items():
                    if not count:
                        continue
                    extent = min(359.9, 360.0 * count / total)
                    self.dashboard_canvas.create_arc(
                        center_x - radius, center_y - radius,
                        center_x + radius, center_y + radius,
                        start=start_angle, extent=-extent,
                        fill=color_map[label], outline=theme["card_bg"], width=2
                    )
                    start_angle -= extent

            # Inner cutout circle for donut (larger hole to match bigger chart)
            self.dashboard_canvas.create_oval(
                center_x - 38, center_y - 38,
                center_x + 38, center_y + 38,
                fill=theme["card_bg"], outline=theme["card_bg"],
            )

            on_count = status_counts["ON"]
            if on_count == total and total > 0:
                self.dashboard_canvas.create_text(
                    center_x, center_y - 8, text="100%",
                    fill="#00FFCC", font=("Segoe UI", 15, "bold"),
                )
                self.dashboard_canvas.create_text(
                    center_x, center_y + 12, text="ALL ON",
                    fill="#00FFCC", font=("Segoe UI", 9, "bold"),
                )
            else:
                self.dashboard_canvas.create_text(
                    center_x, center_y - 7, text=f"{on_count}/{total}",
                    fill=theme["text"], font=("Segoe UI", 14, "bold"),
                )
                self.dashboard_canvas.create_text(
                    center_x, center_y + 12, text="ACTIVE",
                    fill=theme["muted"], font=("Segoe UI", 8, "bold"),
                )

        # Donut Legend
        legend_y = 178
        legend_items = [
            ("ON", status_counts["ON"], "#00D2FF"),
            ("OFF", status_counts["OFF"], "#FF2A42"),
            ("NONE", status_counts["NO DATA"], "#475569"),
        ]
        spacing = (canvas_w - 40) / 3
        for i, (l_name, l_val, l_col) in enumerate(legend_items):
            lx = 24 + i * spacing
            self.dashboard_canvas.create_rectangle(lx, legend_y, lx + 10, legend_y + 10, fill=l_col, outline="")
            self.dashboard_canvas.create_text(
                lx + 16, legend_y + 5,
                anchor="w", text=f"{l_name}: {l_val}",
                fill=theme["text"], font=("Segoe UI", 8, "bold")
            )

        # 2. Glowing Cyan Progress Bars
        bar_x1 = 20
        bar_x2 = canvas_w - 20
        bar_w = bar_x2 - bar_x1

        def draw_progress_meter(y_top, label_text, val_text, ratio, accent="#00D2FF"):
            self.dashboard_canvas.create_text(
                bar_x1, y_top,
                anchor="w", text=label_text,
                fill=theme["muted"], font=("Segoe UI", 8, "bold")
            )
            self.dashboard_canvas.create_text(
                bar_x2, y_top,
                anchor="e", text=val_text,
                fill=theme["text"], font=("Segoe UI", 9, "bold")
            )
            # Background pill bar
            py = y_top + 14
            ph = 8
            self.dashboard_canvas.create_rectangle(
                bar_x1, py, bar_x2, py + ph,
                fill="#162235" if self.is_dark else "#CBD5E1", outline="", width=0
            )
            # Filled glowing pill
            fill_len = max(4, min(bar_w, bar_w * ratio))
            self.dashboard_canvas.create_rectangle(
                bar_x1, py, bar_x1 + fill_len, py + ph,
                fill=accent, outline=""
            )

        # Metric 1: Average Temperature (Scale 18°C - 30°C)
        temp_ratio = max(0.0, min(1.0, (avg_temp_val - 18) / 12)) if avg_temp_val else 0.0
        draw_progress_meter(200, "AVG TEMPERATURE", avg_temp_str, temp_ratio, "#00D2FF")

        # Metric 2: Active AC Units Ratio
        active_ratio = (status_counts["ON"] / total) if total else 0.0
        draw_progress_meter(230, "ACTIVE POWER RATIO", f"{status_counts['ON']} / {total}", active_ratio, "#38BDF8")

        # Metric 3: Total AC units
        draw_progress_meter(260, "TOTAL AC UNITS", f"{ac_count} UNITS", min(1.0, ac_count / 24), "#00FFCC")

        # 3. Telemetry Lore Card (Bottom section)
        card_y = 300
        self.dashboard_canvas.create_text(
            center_x, card_y,
            text="✦  001   013   717   P3R   100   651   111   FES  ✦",
            fill="#38BDF8", font=("Segoe UI", 7, "bold"), anchor="center"
        )
        self.dashboard_canvas.create_text(
            center_x, card_y + 16,
            text="END OF THE WORLD",
            fill="#FFFFFF", font=("Segoe UI", 10, "bold"), anchor="center"
        )
        self.dashboard_canvas.create_text(
            center_x, card_y + 30,
            text="- MARSUDIRINI AC PROTOCOL -",
            fill="#64748B", font=("Segoe UI", 7, "bold"), anchor="center"
        )

        # Styled Box: JUDGEMENT / THE COMEDY IS OVER
        box_y1 = card_y + 44
        box_y2 = box_y1 + 34
        self.dashboard_canvas.create_rectangle(
            bar_x1, box_y1, bar_x2, box_y2,
            fill="#060C16" if self.is_dark else "#F1F5F9",
            outline="#00D2FF", width=1
        )
        self.dashboard_canvas.create_text(
            bar_x1 + 10, (box_y1 + box_y2) / 2,
            anchor="w", text="JUDGEMENT  •  THE COMEDY IS OVER",
            fill=theme["text"], font=("Segoe UI", 8, "bold")
        )
        self.dashboard_canvas.create_text(
            bar_x2 - 10, (box_y1 + box_y2) / 2,
            anchor="e", text="SEES",
            fill="#00D2FF", font=("Segoe UI", 8, "bold")
        )

    def apply_theme(self):
        t = self.get_current_theme()

        self.root.configure(bg=t["bg"])
        self.main_container.configure(bg=t["bg"])
        self.workspace.configure(bg=t["bg"])
        self.map_area.configure(bg=t["bg"])
        self.floor_tabs_frame.configure(bg=t["bg"])

        self.top_bar.configure(bg=t["top_bg"], highlightbackground="#000000")
        self.left_box.configure(bg=t["top_bg"])
        self.title_box.configure(bg=t["top_bg"])
        self.center_box.configure(bg=t["top_bg"])
        self.right_box.configure(bg=t["top_bg"])

        if hasattr(self, "badge_label"):
            self.badge_label.configure(bg=t["top_bg"])
        if hasattr(self, "thumb_label"):
            self.thumb_label.configure(bg=t["top_bg"])

        self.canvas.configure(bg=t["canvas_bg"], highlightbackground=t["card_border"])
        self.preview_card.configure(bg=t["card_bg"], highlightbackground=t["card_border"])
        self.dash_header_frame.configure(bg=t["card_bg"])

        self.app_title.configure(bg=t["top_bg"], fg=t["top_fg"])
        self.app_subtitle.configure(bg=t["top_bg"], fg=t["top_sub_fg"])
        self.ticker_top.configure(bg=t["top_bg"], fg=t["top_fg"])
        self.ticker_sub.configure(bg=t["top_bg"], fg=t["top_sub_fg"])

        self.footer.configure(bg=t["bg"], fg=t["muted"])

        self.dashboard_title.configure(bg=t["card_bg"], fg=t["text"])
        self.dashboard_sub.configure(bg=t["card_bg"], fg=t["muted"])
        self.dashboard_floor.configure(bg=t["card_bg"], fg=t["accent"])
        self.dashboard_canvas.configure(bg=t["card_bg"])

        # Control buttons
        self.btn_report.configure(
            bg="#F59E0B", fg="#000000",
            highlightbackground="#D97706"
        )
        self.btn_admin.configure(
            bg="#0F172A" if self.is_dark else "#E2E8F0",
            fg="#00D2FF" if self.is_dark else "#0284C7",
            highlightbackground="#00D2FF" if self.is_dark else "#0284C7"
        )
        if hasattr(self, "menu_btn"):
            self.menu_btn.configure(
                bg="#000000" if self.is_dark else "#FFFFFF",
                fg="#FFFFFF" if self.is_dark else "#000000",
                highlightbackground="#00D2FF" if self.is_dark else "#0284C7"
            )
        if hasattr(self, "system_menu"):
            menu_bg = "#0A0F1D" if self.is_dark else "#FFFFFF"
            menu_fg = "#FFFFFF" if self.is_dark else "#000000"
            self.system_menu.configure(
                bg=menu_bg, fg=menu_fg,
                activebackground="#00A2FF" if self.is_dark else "#0284C7",
                activeforeground="#000000" if self.is_dark else "#FFFFFF"
            )
            is_fs = self.root.attributes("-fullscreen")
            self.system_menu.entryconfigure(0, label="☀️ Switch to Light Mode" if self.is_dark else "🌙 Switch to Dark Mode")
            self.system_menu.entryconfigure(1, label="❐ Exit Fullscreen (F11)" if is_fs else "⛶ Enter Fullscreen (F11)")

        self.updateFloorSelection()

        if self.animator.isInRoomMenu and self.selectedRoom:
            self.animator.drawRoomMenuOverlay(
                self.selectedRoom,
                backCallback=self.returnToCurrentFloor,
                editCallback=lambda: self.openEditAuthentication(self.selectedRoom),
                reportCallback=lambda r, ac=None: self.openReportDialog(r, ac),
            )

        self.updateDashboard()

    def updateFloorSelection(self):
        t = self.get_current_theme()
        floor_buttons = {
            "Floor 1": self.btn_floor1,
            "Floor 2": self.btn_floor2,
            "Floor 3": self.btn_floor3,
            "Floor 4": self.btn_floor4 if hasattr(self, 'btn_floor4') else None
        }

        for floor_name, button in floor_buttons.items():
            if not button:
                continue
            is_selected = floor_name == self.current_floor
            button.configure(
                bg=t["active_tab_bg"] if is_selected else t["btn_bg"],
                fg=t["active_tab_fg"] if is_selected else t["btn_fg"],
                highlightbackground=t["accent"],
                highlightthickness=1,
            )

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()

    def toggle_fullscreen(self):
        is_fs = not self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", is_fs)
        if hasattr(self, "system_menu"):
            self.system_menu.entryconfigure(1, label="❐ Exit Fullscreen (F11)" if is_fs else "⛶ Enter Fullscreen (F11)")

    def exit_fullscreen(self):
        self.root.attributes("-fullscreen", False)
        if hasattr(self, "system_menu"):
            self.system_menu.entryconfigure(1, label="⛶ Enter Fullscreen (F11)")


if __name__ == "__main__":
    root = tk.Tk()
    app = ACStatFullScreenApp(root)
    root.mainloop()