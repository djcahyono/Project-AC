import tkinter as tk

class ACStatFullScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AC Stat - Building Management")
        
        # State Variables
        self.is_dark = True
        self.is_animating = False
        self.current_floor = "Floor 1"

        # Enable Fullscreen by default
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())


        # edit coords (x1, y1, x2, y2) or add new floors here
        self.floors_data = {
            "Floor 1": [
                # Left Wing
                {"name": "XII H", "coords": (70, 50, 200, 150), "temp": 72, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "XII I", "coords": (70, 160, 200, 260), "temp": 68, "status": "Idle", "ac_power": "ON", "color": "#00ADB5"},
                # Bottom Wing 
                {"name": "XI G",  "coords": (250, 310, 390, 410), "temp": 76, "status": "Warning (High)", "ac_power": "ON", "color": "#FF5722"},
                {"name": "XI A",  "coords": (420, 310, 560, 410), "temp": 71, "status": "Eco Mode", "ac_power": "ON", "color": "#00ADB5"},
                # Right Wing
                {"name": "XI B",  "coords": (600, 50, 690, 150), "temp": 0, "status": "Powered Off", "ac_power": "OFF", "color": "#555555"},
                {"name": "XI C",  "coords": (600, 160, 690, 260), "temp": 69, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
            ],
            "Floor 2": [
                # Placeholder layout for Floor 2 to demonstrate animation
                {"name": "Lab 1", "coords": (150, 100, 350, 200), "temp": 70, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "Lab 2", "coords": (400, 100, 600, 200), "temp": 72, "status": "Cooling", "ac_power": "ON", "color": "#00ADB5"},
                {"name": "Staff Room", "coords": (275, 250, 475, 350), "temp": 74, "status": "Eco", "ac_power": "ON", "color": "#FF5722"},
            ]
        }

        # Theme Color Palette
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
        self.apply_theme()

    def setup_ui(self):
        # Outer Main Container
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)

        # 1. TOP DASHBOARD HEADER BAR
        self.top_bar = tk.Frame(self.main_container, height=70, highlightthickness=1)
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        # Left Section: Logo & Status
        self.left_box = tk.Frame(self.top_bar)
        self.left_box.pack(side="left", padx=25)

        self.app_title = tk.Label(self.left_box, text="AC STAT", font=("Segoe UI", 18, "bold"))
        self.app_title.pack(side="left", padx=(0, 15))

        self.status_badge = tk.Label(self.left_box, text="● SYSTEM ONLINE", font=("Segoe UI", 9, "bold"), fg="#00E676")
        self.status_badge.pack(side="left")

        # Center Section: Quick Summary Metrics
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

        # Right Section: Controls & Image Placeholder
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

        # Image Placeholder (Requirement 3)
        self.img_placeholder = tk.Label(
            self.right_box, text="[ Image Placeholder ]", 
            font=("Segoe UI", 9, "italic"), bg="#444444", fg="#FFFFFF", padx=10
        )
        self.img_placeholder.pack(side="left", fill="y", padx=(15, 0), pady=10)


        # MAIN WORKSPACE (Map + Preview Side Panel)

        self.workspace = tk.Frame(self.main_container)
        self.workspace.pack(fill="both", expand=True, padx=25, pady=20)

        # Map Area containing Floor Tabs and Canvas
        self.map_area = tk.Frame(self.workspace)
        self.map_area.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Floor Selection Tabs
        self.floor_tabs_frame = tk.Frame(self.map_area)
        self.floor_tabs_frame.pack(fill="x", pady=(0, 10))

        self.btn_floor1 = tk.Button(self.floor_tabs_frame, text="Floor 1", font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=lambda: self.change_floor("Floor 1"))
        self.btn_floor1.pack(side="left", padx=(0, 10))

        self.btn_floor2 = tk.Button(self.floor_tabs_frame, text="Floor 2", font=("Segoe UI", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2", command=lambda: self.change_floor("Floor 2"))
        self.btn_floor2.pack(side="left")

        # Map Canvas
        self.canvas = tk.Canvas(self.map_area, highlightthickness=1)
        self.canvas.pack(fill="both", expand=True)

        # Right Column: Room Details Preview Card
        self.preview_card = tk.Frame(self.workspace, width=280, highlightthickness=1)
        self.preview_card.pack_propagate(False)
        self.preview_card.pack(side="right", fill="y")

        self.setup_preview_card()

        # Draw initial floor items onto canvas
        self.draw_floor_items(self.current_floor, offset_x=0)

        # Footer with shortcut hints
        self.footer = tk.Label(
            self.main_container, 
            text="Shortcuts: [ESC] Exit Fullscreen  |  [F11] Toggle Fullscreen", 
            font=("Segoe UI", 9)
        )
        self.footer.pack(side="bottom", anchor="w", padx=25, pady=8)

    def setup_preview_card(self):
        """Sets up widgets inside the right-hand stats preview card. Defaults to empty."""
        self.lbl_card_header = tk.Label(self.preview_card, text="SELECTED ZONE", font=("Segoe UI", 10, "bold"))
        self.lbl_card_header.pack(anchor="w", padx=20, pady=(20, 5))

        self.lbl_room_title = tk.Label(self.preview_card, font=("Segoe UI", 22, "bold"))
        self.lbl_room_title.pack(anchor="w", padx=20)

        self.lbl_temp_val = tk.Label(self.preview_card, font=("Segoe UI", 38, "bold"))
        self.lbl_temp_val.pack(anchor="w", padx=20, pady=5)

        self.lbl_status = tk.Label(self.preview_card, font=("Segoe UI", 11))
        self.lbl_status.pack(anchor="w", padx=20, pady=4)

        self.lbl_ac_power = tk.Label(self.preview_card, font=("Segoe UI", 11))
        self.lbl_ac_power.pack(anchor="w", padx=20, pady=4)

        # Property is hidden by default
        self.clear_preview()

    # ANIMATION & RENDERING ENGINE
    def draw_floor_items(self, floor_name, offset_x=0):
        """Draws the rooms for a specific floor. offset_x allows off-screen rendering for animation."""
        # Draw Courtyard Label if Floor 1
        if floor_name == "Floor 1":
            self.canvas.create_text(
                400 + offset_x, 215, text="Courtyard", 
                font=("Segoe UI", 16, "italic"), fill="#666666",
                tags=("floor_items",)
            )

        # Loop over the dynamic data structure
        for data in self.floors_data[floor_name]:
            name = data["name"]
            x1, y1, x2, y2 = data["coords"]
            fill_color = data["color"] if data["ac_power"] == "ON" else "#555555"
            temp_str = f"{data['temp']}°F" if data["ac_power"] == "ON" else "OFF"
            
            rect_tag = f"{name}_rect"

            # Draw Room Box
            self.canvas.create_rectangle(
                x1 + offset_x, y1, x2 + offset_x, y2, 
                fill=fill_color, outline="#121212", width=2, 
                tags=(name, rect_tag, "floor_items")
            )

            # Draw Room Label Inside
            self.canvas.create_text(
                (x1 + x2)/2 + offset_x, (y1 + y2)/2,
                text=f"{name}\n{temp_str}", justify="center",
                font=("Segoe UI", 11, "bold"), fill="#FFFFFF",
                tags=(name, "floor_items")
            )

            # Interactive Bindings (Hover to zoom and show data)
            self.canvas.tag_bind(name, "<Enter>", lambda e, r=name: self.on_room_hover(r, True))
            self.canvas.tag_bind(name, "<Leave>", lambda e, r=name: self.on_room_hover(r, False))

    def change_floor(self, target_floor):
        """Triggers the slide-in animation sequence to switch floors."""
        if self.current_floor == target_floor or self.is_animating:
            return
        
        self.is_animating = True
        
        # 1. Rename existing map items so we can move them off-screen
        for item in self.canvas.find_withtag("floor_items"):
            self.canvas.addtag_withtag("old_floor_items", item)
            self.canvas.dtag(item, "floor_items")
            
        # 2. Draw the new floor far off-screen to the right
        self.current_floor = target_floor
        slide_distance = 1500
        self.draw_floor_items(target_floor, offset_x=slide_distance)
        
        # 3. Start recursive animation
        self.animate_slide(0, slide_distance)

    def animate_slide(self, current_moved, total_to_move):
        """Recursively shifts canvas elements horizontally."""
        step = 100 # Animation speed (pixels per frame)
        if current_moved + step > total_to_move:
            step = total_to_move - current_moved
            
        # Move both the old items (out) and new items (in)
        self.canvas.move("old_floor_items", -step, 0)
        self.canvas.move("floor_items", -step, 0)
        
        current_moved += step
        
        if current_moved < total_to_move:
            # Continue loop
            self.root.after(16, self.animate_slide, current_moved, total_to_move)
        else:
            # Clean up old items once animation is finished
            self.canvas.delete("old_floor_items")
            self.is_animating = False

    # ==========================================
    # INTERACTIVITY & STATE UPDATES
    # ==========================================
    def get_room_data(self, room_name):
        """Helper to fetch a room's dictionary based on its name."""
        for room in self.floors_data[self.current_floor]:
            if room["name"] == room_name:
                return room
        return None

    def on_room_hover(self, room_name, entering):
        """Handles the zoom effect and right-panel populate on hover."""
        if self.is_animating: return 
        room = self.get_room_data(room_name)
        if not room: return

        rect_tag = f"{room_name}_rect"
        x1, y1, x2, y2 = room["coords"]

        if entering:
            # Zoom In Effect: Expand box by 8 pixels
            zoom = 8
            self.canvas.coords(rect_tag, x1-zoom, y1-zoom, x2+zoom, y2+zoom)
            self.canvas.itemconfig(rect_tag, outline="#FFFFFF", width=3)
            self.update_preview(room)
        else:
            # Zoom Out Effect: Restore original bounds
            self.canvas.coords(rect_tag, x1, y1, x2, y2)
            self.canvas.itemconfig(rect_tag, outline="#121212", width=2)
            self.clear_preview()

    def update_preview(self, room_data):
        """Populates the right-hand panel with active data."""
        t = self.themes["dark"] if self.is_dark else self.themes["light"]

        self.lbl_room_title.config(text=room_data["name"])
        if room_data["ac_power"] == "ON":
            self.lbl_temp_val.config(text=f"{room_data['temp']}°F", fg=room_data["color"])
        else:
            self.lbl_temp_val.config(text="OFF", fg=t["muted"])

        self.lbl_status.config(text=f"Status: {room_data['status']}")
        self.lbl_ac_power.config(text=f"AC Power: {room_data['ac_power']}")

    def clear_preview(self):
        """Resets the right-hand panel to its default empty state."""
        t = self.themes["dark"] if self.is_dark else self.themes["light"]
        self.lbl_room_title.config(text="Hover over a room")
        self.lbl_temp_val.config(text="--°F", fg=t["muted"])
        self.lbl_status.config(text="")
        self.lbl_ac_power.config(text="")

    def apply_theme(self):
        """Applies coloring across all widgets dynamically."""
        t = self.themes["dark"] if self.is_dark else self.themes["light"]

        # Main App Backgrounds
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

        # Text Colors
        self.app_title.configure(bg=t["top_bg"], fg=t["accent"])
        self.status_badge.configure(bg=t["top_bg"])
        self.footer.configure(bg=t["bg"], fg=t["muted"])

        for val, lbl in [(self.stat1_val, self.stat1_lbl), (self.stat2_val, self.stat2_lbl)]:
            val.configure(bg=t["top_bg"], fg=t["text"])
            lbl.configure(bg=t["top_bg"], fg=t["muted"])

        # Preview Panel Text
        self.lbl_card_header.configure(bg=t["card_bg"], fg=t["muted"])
        self.lbl_room_title.configure(bg=t["card_bg"], fg=t["text"])
        self.lbl_temp_val.configure(bg=t["card_bg"])
        self.lbl_status.configure(bg=t["card_bg"], fg=t["text"])
        self.lbl_ac_power.configure(bg=t["card_bg"], fg=t["text"])

        # Top Bar Buttons
        self.btn_theme.configure(text="☀️ Light Mode" if self.is_dark else "🌙 Dark Mode", bg=t["btn_bg"], fg=t["btn_fg"])
        self.btn_fullscreen.configure(text="🗗 Windowed" if self.root.attributes("-fullscreen") else "🗖 Fullscreen", bg=t["btn_bg"], fg=t["btn_fg"])
        
        # Floor Tabs
        self.btn_floor1.configure(bg=t["btn_bg"], fg=t["btn_fg"])
        self.btn_floor2.configure(bg=t["btn_bg"], fg=t["btn_fg"])

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