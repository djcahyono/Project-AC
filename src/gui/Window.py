import tkinter as tk
from animation import CanvasAnimationManager
try:
    from dataAndExec.data import RoomDataProvider
except ModuleNotFoundError:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from dataAndExec.data import RoomDataProvider

class ACStatFullScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AC Stat - Building Management")
        # State Variables
        self.is_dark = True
        self.current_floor = "Floor 1"
        # x1 y1 x2 y2 coordinated
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
                {"name": "Ruang guru", "coords": (415, 350, 635, 430)},
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
                {"name": "R. Heru", "coords": (780, 350, 850, 430)},
                {"name": "X I", "coords": (780, 50, 880, 130)},
                {"name": "X H", "coords": (780, 150, 880, 230)},
                {"name": "X G", "coords": (780, 250, 880, 330)},
            ],
            "Floor 4": [
                {"name": "coming soon", "coords": (30, 30, 920 ,480)}
            ]
        }
        self.data_provider = RoomDataProvider()
        self.floors_data = self.data_provider.get_floors_data(floor_layout)

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

        self.btn_floor4 = tk.Button(self.floor_tabs_frame, text="Floor 4", font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=lambda: self.change_floor("Floor 4"))
        self.btn_floor4.pack(side="left", padx=(10, 0))

        # Map Canvas
        self.canvas = tk.Canvas(self.map_area, highlightthickness=1)
        self.canvas.pack(fill="both", expand=True)

        # Preview Side Panel
        self.preview_card = tk.Frame(self.workspace, width=260, highlightthickness=1)
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
        self.dashboard_title = tk.Label(self.preview_card, text="", font=("Segoe UI", 10, "bold"))
        self.dashboard_title.pack(anchor="w", padx=20, pady=(20, 5))
        self.dashboard_floor = tk.Label(self.preview_card, text="", font=("Segoe UI", 13, "bold"))
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
    #change floor animation
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
    #room hover effect
    def on_room_hover(self, room_data, entering):
        self.animator.hover_zoom(room_data, entering)
        if entering:
            self.update_preview(room_data)
        else:
            self.clear_preview()
    #room click effect
    def on_room_click(self, room_data):
        self.selected_room = room_data
        self.animator.zoom_into_room(room_data, on_complete_callback=self.open_room_menu)

    def open_room_menu(self, room_data):
        self.animator.draw_room_menu_overlay(room_data, back_callback=self.return_to_current_floor)
    #room menu back button
    def return_to_current_floor(self):
        if self.animator.is_animating:
            return
        self.animator.zoom_out_room_view(self.reload_floor_map)

    def update_preview(self, room_data):
        self.update_dashboard()

    def clear_preview(self):
        self.update_dashboard()

    def update_dashboard(self):
        self.dashboard_canvas.delete("all")
    #Theme application (would add more later)
    def apply_theme(self):
        t = self.get_current_theme()

        self.root.configure(bg=t["bg"])
        self.main_container.configure(bg=t["bg"])
        self.workspace.configure(bg=t["bg"])
        self.map_area.configure(bg=t["bg"])
        self.floor_tabs_frame.configure(bg=t["bg"])
        
        self.top_bar.configure(bg=t["top_bg"], highlightbackground=t["border"])
        self.left_box.configure(bg=t["top_bg"])
        self.right_box.configure(bg=t["top_bg"])

        self.canvas.configure(bg=t["canvas_bg"], highlightbackground=t["border"])
        self.preview_card.configure(bg=t["card_bg"], highlightbackground=t["border"])

        self.app_title.configure(bg=t["top_bg"], fg=t["accent"])
        self.footer.configure(bg=t["bg"], fg=t["muted"])

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
        # Gives the active floor a clear visual state.
        t = self.get_current_theme()
        floor_buttons = {
            "Floor 1": self.btn_floor1,
            "Floor 2": self.btn_floor2,
            "Floor 3": self.btn_floor3,
            "Floor 4" : self.btn_floor4 if hasattr(self, 'btn_floor4') else None
        }
    #change floor thing
        for floor_name, button in floor_buttons.items():
            is_selected = floor_name == self.current_floor
            button.configure(
                bg=t["accent"] if is_selected else t["btn_bg"],
                fg="#FFFFFF" if is_selected else t["btn_fg"],
                relief="sunken" if is_selected else "flat",
                highlightthickness=1 if is_selected else 0,
                highlightbackground=t["accent"] if is_selected else t["btn_bg"],
            )
    # toggleables
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