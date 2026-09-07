import tkinter as tk
from animation import CanvasAnimationManager

class ACStatFullScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AC Stat - Building Management")
        # State Variables
        self.is_dark = True
        self.current_floor = "Floor 1"
        self.selected_room = None

        # Fullscreen Defaults
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())

        # Floor Map Datasets
        self.floors_data = {
            "Floor 1": [
                {"name": "XII G", "coords": (100, 100, 200, 180), "temp": 72, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XII F", "coords": (100, 200, 200, 280), "temp": 70, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "R. Data", "coords": (100, 300, 200, 380), "temp": 74, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XII E", "coords": (250, 400, 330, 480), "temp": 71, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XII D", "coords": (350, 400, 430, 480), "temp": 73, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XII C", "coords": (450, 400, 530, 480), "temp": 75, "status": "Eco", "ac_power": "ON", "color": "#FF5722"},
                {"name": "XII B", "coords": (550, 400, 630, 480), "temp": 72, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XII A", "coords": (650, 400, 730, 480), "temp": 70, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "R. Kepsek", "coords": (780, 100, 880, 180), "temp": 68, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "R. TU", "coords": (780, 200, 880, 280), "temp": 72, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
            ],
            "Floor 2": [
                {"name": "XII H", "coords": (100, 100, 200, 180), "temp": 70, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XII I", "coords": (100, 200, 200, 280), "temp": 71, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XI G", "coords": (100, 300, 200, 380), "temp": 74, "status": "Eco", "ac_power": "ON", "color": "#FF5722"},
                {"name": "XI F", "coords": (250, 400, 330, 480), "temp": 72, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XI E", "coords": (350, 400, 430, 480), "temp": 73, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "Guru 1", "coords": (450, 400, 530, 480), "temp": 69, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XI D", "coords": (550, 400, 630, 480), "temp": 75, "status": "Warning", "ac_power": "ON", "color": "#FF5722"},
                {"name": "Guru 2", "coords": (650, 400, 730, 480), "temp": 71, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XI A", "coords": (780, 100, 880, 180), "temp": 70, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XI B", "coords": (780, 200, 880, 280), "temp": 72, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XI C", "coords": (780, 300, 880, 380), "temp": 74, "status": "Eco", "ac_power": "ON", "color": "#FF5722"},
            ],
            "Floor 3": [
                {"name": "XI H", "coords": (100, 100, 200, 180), "temp": 70, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XI I", "coords": (100, 200, 200, 280), "temp": 71, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "X A", "coords": (100, 300, 200, 380), "temp": 73, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "X B", "coords": (210, 400, 290, 480), "temp": 72, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "X C", "coords": (300, 400, 380, 480), "temp": 71, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "X D", "coords": (390, 400, 470, 480), "temp": 74, "status": "Eco", "ac_power": "ON", "color": "#FF5722"},
                {"name": "X E", "coords": (480, 400, 560, 480), "temp": 70, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "X F", "coords": (570, 400, 650, 480), "temp": 73, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "R. Heru", "coords": (660, 400, 740, 480), "temp": 68, "status": "Cooling", "ac_power": "OFF", "color": "#00ADB5", "has_stats": False},
                {"name": "X I", "coords": (780, 100, 880, 180), "temp": 70, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "X H", "coords": (780, 200, 880, 280), "temp": 72, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "X G", "coords": (780, 300, 880, 380), "temp": 74, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
            ]
        }

        ac_number = 1
        for floor_rooms in self.floors_data.values():
            for room in floor_rooms:
                room.update({
                    "ac_id": f"AC-{ac_number:02d}",
                    "ac_ids": [f"AC-{ac_number:02d}A", f"AC-{ac_number:02d}B"],
                    "ac_model": "Daikin Inverter",
                    "ac_condition": "Needs service" if room["status"] == "Warning" else "Good",
                })
                ac_number += 1

        # Theme Configuration
        self.themes = {
            "dark": {
                "bg": "#121212", "top_bg": "#1E1E1E", "card_bg": "#1E1E1E",
                "canvas_bg": "#181818", "text": "#EEEEEE", "muted": "#888888",
                "accent": "#00ADB5", "btn_bg": "#2A2A2A", "btn_fg": "#FFFFFF",
                "border": "#333333"
            },
            "light": {
                "bg": "#F4F6F9", "top_bg": "#FFFFFF", "card_bg": "#FFFFFF",
                "canvas_bg": "#EAEAEA", "text": "#222831", "muted": "#666666",
                "accent": "#00ADB5", "btn_bg": "#E0E0E0", "btn_fg": "#222831",
                "border": "#DDDDDD"
            }
        }

        self.setup_ui()
        self.animator = CanvasAnimationManager(self.canvas, self.root, self.get_current_theme)
        self.reload_floor_map()
        self.apply_theme()

    def get_current_theme(self):
        return self.themes["dark"] if self.is_dark else self.themes["light"]

    def setup_ui(self):
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)

        # Header Bar
        self.top_bar = tk.Frame(self.main_container, height=70, highlightthickness=1)
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        # Left Header
        self.left_box = tk.Frame(self.top_bar)
        self.left_box.pack(side="left", padx=25)

        self.app_title = tk.Label(self.left_box, text="AC STAT", font=("Segoe UI", 18, "bold"))
        self.app_title.pack(side="left", padx=(0, 15))

        self.status_badge = tk.Label(self.left_box, text="● SYSTEM ONLINE", font=("Segoe UI", 9, "bold"), fg="#00E676")
        self.status_badge.pack(side="left")

        # Center Metrics
        self.center_box = tk.Frame(self.top_bar)
        self.center_box.pack(side="left", expand=True)

        self.stat1_val = tk.Label(self.center_box, text="71°F", font=("Segoe UI", 13, "bold"))
        self.stat1_val.pack(side="left")
        self.stat1_lbl = tk.Label(self.center_box, text=" Avg Temp  |  ", font=("Segoe UI", 10))
        self.stat1_lbl.pack(side="left")

        self.stat2_val = tk.Label(self.center_box, text="6 / 7", font=("Segoe UI", 13, "bold"))
        self.stat2_val.pack(side="left")
        self.stat2_lbl = tk.Label(self.center_box, text=" Active Zones", font=("Segoe UI", 10))
        self.stat2_lbl.pack(side="left")

        # Right Controls
        self.right_box = tk.Frame(self.top_bar)
        self.right_box.pack(side="right", padx=25)

        self.btn_theme = tk.Button(
            self.right_box, text="☀️ Light Mode", font=("Segoe UI", 9, "bold"),
            bd=0, padx=12, pady=6, cursor="hand2", command=self.toggle_theme
        )
        self.btn_theme.pack(side="left", padx=5)

        self.btn_fullscreen = tk.Button(
            self.right_box, text="🗗 Windowed", font=("Segoe UI", 9, "bold"),
            bd=0, padx=12, pady=6, cursor="hand2", command=self.toggle_fullscreen
        )
        self.btn_fullscreen.pack(side="left", padx=5)

        self.img_placeholder = tk.Label(
            self.right_box, text="[ Image Placeholder ]", 
            font=("Segoe UI", 9, "italic"), bg="#444444", fg="#FFFFFF", padx=10
        )
        self.img_placeholder.pack(side="left", fill="y", padx=(15, 0), pady=10)

        # Workspace Area
        self.workspace = tk.Frame(self.main_container)
        self.workspace.pack(fill="both", expand=True, padx=25, pady=20)

        self.map_area = tk.Frame(self.workspace)
        self.map_area.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Floor Tabs
        self.floor_tabs_frame = tk.Frame(self.map_area)
        self.floor_tabs_frame.pack(fill="x", pady=(0, 10))

        self.btn_floor1 = tk.Button(self.floor_tabs_frame, text="Floor 1", font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=lambda: self.change_floor("Floor 1"))
        self.btn_floor1.pack(side="left", padx=(0, 10))

        self.btn_floor2 = tk.Button(self.floor_tabs_frame, text="Floor 2", font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=lambda: self.change_floor("Floor 2"))
        self.btn_floor2.pack(side="left", padx=(0, 10))

        self.btn_floor3 = tk.Button(self.floor_tabs_frame, text="Floor 3", font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=lambda: self.change_floor("Floor 3"))
        self.btn_floor3.pack(side="left")

        # Map Canvas
        self.canvas = tk.Canvas(self.map_area, highlightthickness=1)
        self.canvas.pack(fill="both", expand=True)

        # Preview Side Panel
        self.preview_card = tk.Frame(self.workspace, width=280, highlightthickness=1)
        self.preview_card.pack_propagate(False)
        self.preview_card.pack(side="right", fill="y")

        self.setup_dashboard_card()

        # Footer
        self.footer = tk.Label(
            self.main_container, 
            text="Shortcuts: [ESC] Exit Fullscreen  |  [F11] Toggle Fullscreen", 
            font=("Segoe UI", 9)
        )
        self.footer.pack(side="bottom", anchor="w", padx=25, pady=8)

    def setup_dashboard_card(self):
        self.dashboard_title = tk.Label(self.preview_card, text="BUILDING DASHBOARD", font=("Segoe UI", 10, "bold"))
        self.dashboard_title.pack(anchor="w", padx=20, pady=(20, 5))
        self.dashboard_floor = tk.Label(self.preview_card, font=("Segoe UI", 13, "bold"))
        self.dashboard_floor.pack(anchor="w", padx=20, pady=(0, 8))
        self.dashboard_canvas = tk.Canvas(self.preview_card, width=280, height=560, highlightthickness=0)
        self.dashboard_canvas.pack(fill="both", expand=True, padx=5, pady=5)

    def reload_floor_map(self):
        self.canvas.delete("all")
        floor_data = self.floors_data[self.current_floor]
        self.animator.draw_floor_items(
            floor_data, self.current_floor,
            hover_callback=self.on_room_hover,
            click_callback=self.on_room_click
        )

    def change_floor(self, target_floor):
        if self.animator.is_animating:
            return

        if self.animator.is_in_room_menu:
            self.animator.zoom_out_room_view(lambda: self._change_floor_after_room(target_floor))
            return

        if self.current_floor == target_floor:
            return

        self._change_floor_after_room(target_floor)

    def _change_floor_after_room(self, target_floor):
        if self.current_floor == target_floor:
            self.reload_floor_map()
            return

        current_floor_number = int(self.current_floor.split()[-1])
        target_floor_number = int(target_floor.split()[-1])
        direction = "up" if target_floor_number > current_floor_number else "down"
        self.current_floor = target_floor
        self.update_floor_selection()
        self.animator.change_floor_slide(
            self.floors_data[target_floor], target_floor,
            direction,
            hover_cb=self.on_room_hover,
            click_cb=self.on_room_click,
            on_complete=self.update_dashboard
        )

    def on_room_hover(self, room_data, entering):
        self.animator.hover_zoom(room_data, entering)
        if entering:
            self.update_preview(room_data)
        else:
            self.clear_preview()

    def on_room_click(self, room_data):
        self.selected_room = room_data
        self.animator.zoom_into_room(room_data, on_complete_callback=self.open_room_menu)

    def open_room_menu(self, room_data):
        self.animator.draw_room_menu_overlay(room_data, back_callback=self.return_to_current_floor)

    def return_to_current_floor(self):
        if self.animator.is_animating:
            return
        self.animator.zoom_out_room_view(self.reload_floor_map)

    def update_preview(self, room_data):
        self.update_dashboard()

    def clear_preview(self):
        self.update_dashboard()

    def update_dashboard(self):
        all_rooms = [room for floor in self.floors_data.values() for room in floor if room.get("has_stats", True)]
        rooms = [room for room in self.floors_data[self.current_floor] if room.get("has_stats", True)]
        temperatures = [room["temp"] for room in rooms]
        active_count = sum(room["ac_power"] == "ON" for room in all_rooms)
        average_temp = round(sum(temperatures) / len(temperatures)) if temperatures else 0
        condition_counts = {"Good": 0, "Needs service": 0}
        for room in all_rooms:
            condition_counts[room["ac_condition"]] = condition_counts.get(room["ac_condition"], 0) + 1

        self.stat1_val.config(text=f"{average_temp} F")
        self.stat2_val.config(text=f"{active_count} / {len(all_rooms)}")
        self.dashboard_floor.config(text=self.current_floor)
        self.dashboard_canvas.delete("all")
        t = self.get_current_theme()
        self.dashboard_canvas.create_text(20, 24, anchor="w", text="TEMPERATURE", fill=t["muted"], font=("Segoe UI", 10, "bold"))
        max_temp = max(temperatures) if temperatures else 1
        for index, room in enumerate(rooms):
            y = 55 + index * 22
            bar_width = 170 * room["temp"] / max_temp
            self.dashboard_canvas.create_text(20, y, anchor="w", text=room["name"], fill=t["text"], font=("Segoe UI", 9))
            self.dashboard_canvas.create_rectangle(85, y - 6, 85 + bar_width, y + 6, fill=room["color"], outline="")
            self.dashboard_canvas.create_text(270, y, anchor="e", text=f"{room['temp']} F", fill=t["text"], font=("Segoe UI", 9, "bold"))
        status_y = 55 + len(rooms) * 22 + 18
        self.dashboard_canvas.create_text(20, status_y, anchor="w", text="AC CONDITION", fill=t["muted"], font=("Segoe UI", 10, "bold"))
        self.dashboard_canvas.create_text(20, status_y + 30, anchor="w", text=f"Good units       {condition_counts.get('Good', 0)}", fill="#00E676", font=("Segoe UI", 10, "bold"))
        self.dashboard_canvas.create_text(20, status_y + 58, anchor="w", text=f"Needs service    {condition_counts.get('Needs service', 0)}", fill="#FFB020", font=("Segoe UI", 10, "bold"))

    def apply_theme(self):
        t = self.get_current_theme()

        self.root.configure(bg=t["bg"])
        self.main_container.configure(bg=t["bg"])
        self.workspace.configure(bg=t["bg"])
        self.map_area.configure(bg=t["bg"])
        self.floor_tabs_frame.configure(bg=t["bg"])
        
        self.top_bar.configure(bg=t["top_bg"], highlightbackground=t["border"])
        self.left_box.configure(bg=t["top_bg"])
        self.center_box.configure(bg=t["top_bg"])
        self.right_box.configure(bg=t["top_bg"])

        self.canvas.configure(bg=t["canvas_bg"], highlightbackground=t["border"])
        self.preview_card.configure(bg=t["card_bg"], highlightbackground=t["border"])

        self.app_title.configure(bg=t["top_bg"], fg=t["accent"])
        self.status_badge.configure(bg=t["top_bg"])
        self.footer.configure(bg=t["bg"], fg=t["muted"])

        for val, lbl in [(self.stat1_val, self.stat1_lbl), (self.stat2_val, self.stat2_lbl)]:
            val.configure(bg=t["top_bg"], fg=t["text"])
            lbl.configure(bg=t["top_bg"], fg=t["muted"])

        self.dashboard_title.configure(bg=t["card_bg"], fg=t["muted"])
        self.dashboard_floor.configure(bg=t["card_bg"], fg=t["text"])
        self.dashboard_canvas.configure(bg=t["card_bg"])

        self.btn_theme.configure(text="☀️ Light Mode" if self.is_dark else "🌙 Dark Mode", bg=t["btn_bg"], fg=t["btn_fg"])
        self.btn_fullscreen.configure(text="🗗 Windowed" if self.root.attributes("-fullscreen") else "🗖 Fullscreen", bg=t["btn_bg"], fg=t["btn_fg"])
        
        self.btn_floor1.configure(bg=t["btn_bg"], fg=t["btn_fg"])
        self.btn_floor2.configure(bg=t["btn_bg"], fg=t["btn_fg"])
        self.btn_floor3.configure(bg=t["btn_bg"], fg=t["btn_fg"])
        self.update_floor_selection()

        if self.animator.is_in_room_menu and self.selected_room:
            self.animator.draw_room_menu_overlay(self.selected_room, back_callback=self.return_to_current_floor)

        self.update_dashboard()

    def update_floor_selection(self):
        """Give the active floor a clear visual state."""
        t = self.get_current_theme()
        floor_buttons = {
            "Floor 1": self.btn_floor1,
            "Floor 2": self.btn_floor2,
            "Floor 3": self.btn_floor3,
        }

        for floor_name, button in floor_buttons.items():
            is_selected = floor_name == self.current_floor
            button.configure(
                bg=t["accent"] if is_selected else t["btn_bg"],
                fg="#FFFFFF" if is_selected else t["btn_fg"],
                relief="sunken" if is_selected else "flat",
                highlightthickness=1 if is_selected else 0,
                highlightbackground=t["accent"] if is_selected else t["btn_bg"],
            )

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()

    def toggle_fullscreen(self):
        is_fs = not self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", is_fs)
        self.btn_fullscreen.config(text="🗗 Windowed" if is_fs else "🗖 Fullscreen")

    def exit_fullscreen(self):
        self.root.attributes("-fullscreen", False)
        self.btn_fullscreen.config(text="🗖 Fullscreen")

if __name__ == "__main__":
    root = tk.Tk()
    app = ACStatFullScreenApp(root)
    root.mainloop()