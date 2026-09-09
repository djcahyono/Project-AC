import tkinter as tk

class CanvasAnimationManager:
    #Handles canvas rendering, room hovering, zoom-to-menu transitions, and slide animations.
    
    def __init__(self, canvas, root, theme_getter):
        self.canvas = canvas
        self.root = root
        self.get_theme = theme_getter
        
        self.is_animating = False
        self.active_room = None
        self.is_in_room_menu = False

    def draw_floor_items(self, floor_data, floor_name, hover_callback, click_callback, offset_x=0):
        for room in floor_data:
            name = room["name"]
            x1, y1, x2, y2 = room["coords"]
            fill_color = self.get_temperature_color(room)
            
            rect_tag = f"{name}_rect"

            # Draw Room Box
            self.canvas.create_rectangle(
                x1 + offset_x, y1, x2 + offset_x, y2, 
                fill=fill_color, outline="#1254A0", width=2,
                tags=(name, rect_tag, "floor_items")
            )

            # Draw Room Label
            self.canvas.create_text(
                (x1 + x2) / 2 + offset_x, (y1 + y2) / 2,
                text=name, justify="center",
                font=("Segoe UI", 11, "bold"), fill="#FFFFFF",
                tags=(name, "floor_items")
            )

            # Only classroom rooms open the interactive room view.
            if room.get("has_stats", True):
                self.canvas.tag_bind(name, "<Enter>", lambda e, r=room: hover_callback(r, True))
                self.canvas.tag_bind(name, "<Leave>", lambda e, r=room: hover_callback(r, False))
                self.canvas.tag_bind(name, "<Button-1>", lambda e, r=room: click_callback(r))
    #color determination based on temperature and AC power state
    @staticmethod
    def get_temperature_color(room):
        if room.get("ac_power") == "OFF":
            return "#616161"

        temperature = room.get("temp")
        if temperature is None:
            return "#757575"
        if temperature >= 75:
            return "#FF5722"
        if temperature >= 73:
            return "#FFC107"
        return "#00ADB5"

    def hover_zoom(self, room_data, entering):
        # Expands room bounds slightly on mouse hover.
        if self.is_animating or self.is_in_room_menu:
            return

        rect_tag = f"{room_data['name']}_rect"
        x1, y1, x2, y2 = room_data["coords"]

        if entering:
            zoom = 8
            self.canvas.coords(rect_tag, x1 - zoom, y1 - zoom, x2 + zoom, y2 + zoom)
            self.canvas.itemconfig(rect_tag, outline="#FFFFFF", width=3)
        else:
            self.canvas.coords(rect_tag, x1, y1, x2, y2)
            self.canvas.itemconfig(rect_tag, outline="#1254A0", width=2)

    def zoom_into_room(self, room_data, on_complete_callback, step=0, total_steps=18):
        # Animates canvas scaling centered on the clicked room object.
        if step == 0:
            if self.is_animating:
                return
            self.is_animating = True
            self.is_in_room_menu = True

        tag = room_data["name"]
        bbox = self.canvas.bbox(tag)
        if not bbox:
            self.is_animating = False
            return

        # Target center calculation
        canvas_w = self.canvas.winfo_width() or 900
        canvas_h = self.canvas.winfo_height() or 500
        screen_cx, screen_cy = canvas_w / 2, canvas_h / 2
        obj_cx, obj_cy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2

        scale_factor = 1.12
        dx = (screen_cx - obj_cx) * 0.3
        dy = (screen_cy - obj_cy) * 0.3

        self.canvas.move("all", dx, dy)
        self.canvas.scale("all", screen_cx, screen_cy, scale_factor, scale_factor)

        if step < total_steps:
            self.root.after(16, lambda: self.zoom_into_room(room_data, on_complete_callback, step + 1, total_steps))
        else:
            self.is_animating = False
            on_complete_callback(room_data)
    def zoom_out_of_room(self, on_complete_callback, step=0, total_steps=18):
        # Reverses the zoom-in animation to return to the original canvas view.
        if step == 0:
            if self.is_animating:
                return
            self.is_animating = True

        scale_factor = 1 / 1.12
        canvas_w = self.canvas.winfo_width() or 900
        canvas_h = self.canvas.winfo_height() or 500
        screen_cx, screen_cy = canvas_w / 2, canvas_h / 2

        self.canvas.scale("all", screen_cx, screen_cy, scale_factor, scale_factor)
        self.canvas.move("all", -((screen_cx - screen_cx) * 0.3), -((screen_cy - screen_cy) * 0.3))

        if step < total_steps:
            self.root.after(16, lambda: self.zoom_out_of_room(on_complete_callback, step + 1, total_steps))
        else:
            self.is_animating = False
            self.is_in_room_menu = False
            on_complete_callback()

    def zoom_out_room_view(self, on_complete_callback, step=0, total_steps=12):
        # Animates the room scene away before returning to the floor map.
        if step == 0:
            if self.is_animating:
                return
            self.is_animating = True
            self.canvas.delete("ac_focus")

        canvas_w = self.canvas.winfo_width() or 1200
        canvas_h = self.canvas.winfo_height() or 700
        self.canvas.scale("all", canvas_w / 2, canvas_h / 2, 0.88, 0.88)
        if step < total_steps:
            self.root.after(16, lambda: self.zoom_out_room_view(on_complete_callback, step + 1, total_steps))
        else:
            self.is_animating = False
            self.is_in_room_menu = False
            self.canvas.delete("all")
            on_complete_callback()

    def draw_room_view(self, room_data, on_ac_click, on_back_click):
        #Renders the interior of specific roomS
        self.canvas.delete("all")
        self.is_in_room_menu = True
        self.active_room = room_data

        canvas_w = self.canvas.winfo_width() or 900
        canvas_h = self.canvas.winfo_height() or 560
        room_x1 = max(140, min(180, canvas_w * 0.18))
        room_y1 = 55
        room_x2, room_y2 = canvas_w - 40, canvas_h - 45
        room_width = room_x2 - room_x1
        room_height = room_y2 - room_y1

        # Simple top-down floor plan: a room outline, one tiny whiteboard, and chairs.
        self.canvas.create_rectangle(room_x1, room_y1, room_x2, room_y2, fill="#1E1E24", outline="#FF2A42", width=3, tags="room_element")
        whiteboard_x = room_x1 + room_width * 0.325
        self.canvas.create_rectangle(whiteboard_x, room_y1 + 18, whiteboard_x + room_width * 0.4, room_y1 + 27, fill="#F0F0F0", outline="#A0A0A0", tags="room_element")

        chair_width = max(44, min(48, room_width * 0.07))
        chair_height = chair_width * 0.55
        chair_start_x = room_x1 + room_width * 0.25
        chair_y = room_y1 + room_height * 0.18
        for row in range(6):
            for column in range(6):
                chair_x = chair_start_x + column * (chair_width * 1.7)
                chair_top = chair_y + row * (chair_height * 2.0)
                self.canvas.create_rectangle(chair_x, chair_top, chair_x + chair_width, chair_top + chair_height, fill="#8B5A2B", outline="#5A351A", tags="room_element")

        # Two AC units stay on the left wall and face inward toward the students.
        ac_x = room_x1 + 18
        ac_width = max(45, min(67, room_width * 0.049))
        ac_height = max(84, min(109, room_height * 0.098))
        ac_ids = room_data.get("ac_ids", [room_data.get("ac_id", "AC UNIT") + "-1", room_data.get("ac_id", "AC UNIT") + "-2"])
        for ac_index, fraction in enumerate((2 / 6, 4 / 6)):
            ac_y = room_y1 + room_height * fraction - 20
            ac_tag = f"interactive_ac_{ac_index}"
            self.canvas.create_rectangle(ac_x, ac_y, ac_x + ac_width, ac_y + ac_height, fill="#E0E0E0", outline="#2B2D42", width=2, tags=("interactive_ac", ac_tag, "ac_element"))
            self.canvas.create_line(ac_x + ac_width * 0.65, ac_y + 7, ac_x + ac_width * 0.65, ac_y + ac_height - 7, fill="#4A4E69", width=3, tags=("interactive_ac", ac_tag, "ac_element"))
            self.canvas.create_oval(ac_x + 7, ac_y + 8, ac_x + 15, ac_y + 17, fill="#00FF66", outline="", tags=("interactive_ac", ac_tag, "ac_element"))
            self.canvas.tag_bind(ac_tag, "<Button-1>", lambda e, index=ac_index: on_ac_click(index))

        # Bind click events exclusively to the AC unit
        self.canvas.tag_bind("interactive_ac", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("interactive_ac", "<Leave>", lambda e: self.canvas.config(cursor=""))

        # Back button sits in the navigation space just outside the room.
        back_x1 = max(10, room_x1 - 135)
        back_x2 = room_x1 - 15
        back_y1 = (room_y1 + room_y2 - 40) / 2
        back_y2 = back_y1 + 40
        self.canvas.create_rectangle(back_x1, back_y1, back_x2, back_y2, fill="#FF2A42", tags="back_btn")
        self.canvas.create_text((back_x1 + back_x2) / 2, (back_y1 + back_y2) / 2, text="< BACK TO MAP", fill="#FFFFFF", font=("Segoe UI", 10, "bold"), tags="back_btn")
        self.canvas.tag_bind("back_btn", "<Button-1>", lambda e: on_back_click())
        self.canvas.tag_bind("back_btn", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("back_btn", "<Leave>", lambda e: self.canvas.config(cursor=""))

    def draw_room_menu_overlay(self, room_data, back_callback):
        # Keep the public API used by Window.py while rendering the room view.
        self.draw_room_view(
            room_data,
            on_ac_click=lambda ac_index: self.show_ac_info(room_data, ac_index),
            on_back_click=back_callback,
        )

    def show_ac_info(self, room_data, ac_index=0):
        #darken back screen
        self.canvas.delete("ac_focus")
        self.canvas.create_rectangle(
            0, 0, self.canvas.winfo_width() or 1200, self.canvas.winfo_height() or 700,
            fill="#000000", stipple="gray50", outline="", tags="ac_focus"
        )

        panel_x, panel_y = 410, 205
        self.canvas.create_rectangle(
            panel_x, panel_y, 810, 490, fill="#101318", outline="#00ADB5", width=2,
            tags="ac_focus"
        )
        self.canvas.tag_bind("ac_focus", "<Button-1>", lambda e: self.canvas.delete("ac_focus"))
        self.canvas.tag_bind("ac_focus", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("ac_focus", "<Leave>", lambda e: self.canvas.config(cursor=""))

    def change_floor_slide(self, target_floor_data, target_floor_name, direction, hover_cb, click_cb, on_complete):
        # Executes directional floor transition slide animation (left or right).
        if self.is_animating:
            return
            
        self.is_animating = True
        
        # Tag active items to move them out
        for item in self.canvas.find_withtag("floor_items"):
            self.canvas.addtag_withtag("old_floor_items", item)
            self.canvas.dtag(item, "floor_items")

        # Determine slide direction:
        # Going UP a floor -> new floor slides in from Right (+1500 -> move left)
        # Going DOWN a floor -> new floor slides in from Left (-1500 -> move right)
        slide_distance = 1500 if direction == "up" else -1500
        
        self.draw_floor_items(target_floor_data, target_floor_name, hover_cb, click_cb, offset_x=slide_distance)
        self._animate_slide(0, slide_distance, direction, on_complete)

    def _animate_slide(self, current_moved, total_to_move, direction, on_complete):
        step_val = 100
        # Determine movement vector based on direction
        step = -step_val if direction == "up" else step_val
        abs_total = abs(total_to_move)

        if current_moved + step_val > abs_total:
            remaining = abs_total - current_moved
            step = -remaining if direction == "up" else remaining

        self.canvas.move("old_floor_items", step, 0)
        self.canvas.move("floor_items", step, 0)

        current_moved += step_val

        if current_moved < abs_total:
            self.root.after(16, lambda: self._animate_slide(current_moved, total_to_move, direction, on_complete))
        else:
            self.canvas.delete("old_floor_items")
            self.is_animating = False
            on_complete()