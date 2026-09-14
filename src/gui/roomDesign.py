import sys
import tkinter as tk
from pathlib import Path

src_dir = Path(__file__).resolve().parents[1]
for candidate in (str(src_dir), str(src_dir.parent)):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

try:
    from gui.baseRenderer import BaseRenderer
except ModuleNotFoundError:
    from src.gui.baseRenderer import BaseRenderer


class RoomDesigner(BaseRenderer):
    # Renders the interactive room interior and AC detail modal.

    def __init__(self, canvas):
        super().__init__(canvas)  # Calls BaseRenderer.__init__ — Inheritance

    def render(self, roomData=None, onAcClick=None, onBackClick=None, onEditClick=None, onReportClick=None):
        # Polymorphic render method for the room interior view.
        if roomData:
            self.drawRoomView(roomData, onAcClick, onBackClick, onEditClick, onReportClick)


    def drawRoomView(self, roomData, onAcClick, onBackClick, onEditClick=None, onReportClick=None):
        self.canvas.delete("all")

        canvasWidth = self.canvas.winfo_width() or 950
        canvasHeight = self.canvas.winfo_height() or 580

        # Background grid / Dark Hour floor
        self.canvas.create_rectangle(0, 0, canvasWidth, canvasHeight, fill="#070A12", outline="")

        # Subtle tactical grid markers (+)
        for gx in range(50, canvasWidth, 100):
            for gy in range(50, canvasHeight, 100):
                self.canvas.create_text(gx, gy, text="+", fill="#162035", font=("Segoe UI", 9))

        # Room boundary
        roomX1 = max(160, min(200, canvasWidth * 0.18))
        roomY1 = 70
        roomX2, roomY2 = canvasWidth - 40, canvasHeight - 40
        roomWidth = roomX2 - roomX1
        roomHeight = roomY2 - roomY1

        # Tactical Room Floor
        self.canvas.create_rectangle(
            roomX1, roomY1, roomX2, roomY2,
            fill="#0D1322", outline="#00A2FF", width=2, tags="room_element"
        )
        # Inner accent border
        self.canvas.create_rectangle(
            roomX1 + 4, roomY1 + 4, roomX2 - 4, roomY2 - 4,
            fill="", outline="#162A45", width=1, tags="room_element"
        )

        # Corner brackets on room
        bracket_len = 16
        for bx, by, dx, dy in [
            (roomX1, roomY1, 1, 1),
            (roomX2, roomY1, -1, 1),
            (roomX1, roomY2, 1, -1),
            (roomX2, roomY2, -1, -1)
        ]:
            self.canvas.create_line(bx, by, bx + dx * bracket_len, by, fill="#00D2FF", width=3, tags="room_element")
            self.canvas.create_line(bx, by, bx, by + dy * bracket_len, fill="#00D2FF", width=3, tags="room_element")

        # Top Room HUD Ribbon
        room_name = roomData.get("name", "ROOM")
        power_state = str(roomData.get("acPower", "ON")).upper()
        temp_val = roomData.get("temp")
        temp_str = f"{temp_val}°C" if temp_val is not None else "--°C"

        self.canvas.create_rectangle(
            roomX1, roomY1 - 42, roomX2, roomY1 - 8,
            fill="#0A1628", outline="#00A2FF", width=1, tags="room_element"
        )
        self.canvas.create_rectangle(
            roomX1, roomY1 - 42, roomX1 + 8, roomY1 - 8,
            fill="#00D2FF", outline="", tags="room_element"
        )
        self.canvas.create_text(
            roomX1 + 20, roomY1 - 25,
            anchor="w", text=f"MARSUDIRINI FACILITY // {room_name}",
            fill="#FFFFFF", font=("Segoe UI", 12, "bold"), tags="room_element"
        )
        self.canvas.create_text(
            roomX2 - 180, roomY1 - 25,
            anchor="w", text=f"POWER: {power_state}  |  TEMP: {temp_str}",
            fill="#00D2FF", font=("Segoe UI", 10, "bold"), tags="room_element"
        )

        # Teacher's Whiteboard
        whiteboardX = roomX1 + roomWidth * 0.30
        self.canvas.create_rectangle(
            whiteboardX, roomY1 + 18,
            whiteboardX + roomWidth * 0.44, roomY1 + 28,
            fill="#E2E8F0", outline="#00D2FF", width=1, tags="room_element"
        )
        self.canvas.create_text(
            whiteboardX + (roomWidth * 0.44) / 2, roomY1 + 23,
            text="─── FRONT OF CLASSROOM / TEACHER BOARD ───",
            fill="#334155", font=("Segoe UI", 7, "bold"), tags="room_element"
        )

        # Classroom Desks & Chairs (tactical layout)
        chairWidth = max(42, min(50, roomWidth * 0.075))
        chairHeight = chairWidth * 0.52
        chairStartX = roomX1 + roomWidth * 0.22
        chairY = roomY1 + roomHeight * 0.18
        for row in range(5):
            for column in range(5):
                chairX = chairStartX + column * (chairWidth * 1.85)
                chairTop = chairY + row * (chairHeight * 2.1)
                # Desk box
                self.canvas.create_rectangle(
                    chairX, chairTop,
                    chairX + chairWidth, chairTop + chairHeight,
                    fill="#1A253A", outline="#293B58", tags="room_element"
                )
                self.canvas.create_text(
                    chairX + chairWidth / 2, chairTop + chairHeight / 2,
                    text=f"{row+1}-{column+1}", fill="#475569", font=("Segoe UI", 7),
                    tags="room_element"
                )

        # AC Units on Left Wall
        acX = roomX1 + 18
        acWidth = max(55, min(80, roomWidth * 0.08))
        acHeight = max(80, min(100, roomHeight * 0.14))
        acIds = roomData.get(
            "acIds",
            [
                f"{roomData.get('name', 'AC')}-UNIT-1",
                f"{roomData.get('name', 'AC')}-UNIT-2",
            ],
        )

        is_power_on = power_state == "ON"
        led_color = "#00FFCC" if is_power_on else "#FF2A42"

        for ac_index, fraction in enumerate((0.32, 0.68)):
            acY = roomY1 + roomHeight * fraction - (acHeight / 2)
            acTag = f"interactiveAc{ac_index}"

            # Outer AC housing
            self.canvas.create_rectangle(
                acX, acY, acX + acWidth, acY + acHeight,
                fill="#0F1B2E", outline="#00D2FF", width=2,
                tags=("interactiveAc", acTag, "acElement")
            )
            # AC Header line
            self.canvas.create_rectangle(
                acX, acY, acX + acWidth, acY + 16,
                fill="#1E2E48", outline="#00D2FF", width=1,
                tags=("interactiveAc", acTag, "acElement")
            )
            self.canvas.create_text(
                acX + acWidth / 2, acY + 8,
                text=f"AC #{ac_index + 1}", fill="#00D2FF",
                font=("Segoe UI", 8, "bold"), tags=("interactiveAc", acTag, "acElement")
            )

            # Airflow ventilation grilles
            for gy in range(int(acY + 24), int(acY + acHeight - 16), 8):
                self.canvas.create_line(
                    acX + 8, gy, acX + acWidth - 8, gy,
                    fill="#38BDF8" if is_power_on else "#475569", width=2,
                    tags=("interactiveAc", acTag, "acElement")
                )

            # Status LED indicator
            self.canvas.create_oval(
                acX + 8, acY + acHeight - 12,
                acX + 16, acY + acHeight - 4,
                fill=led_color, outline="",
                tags=("interactiveAc", acTag, "acElement")
            )
            self.canvas.create_text(
                acX + 22, acY + acHeight - 8,
                anchor="w", text="RUNNING" if is_power_on else "STANDBY",
                fill=led_color, font=("Segoe UI", 7, "bold"),
                tags=("interactiveAc", acTag, "acElement")
            )

            # Click binding
            self.canvas.tag_bind(
                acTag, "<Button-1>",
                lambda e, index=ac_index: onAcClick(index)
            )

        self.canvas.tag_bind(
            "interactiveAc", "<Enter>",
            lambda e: self.canvas.config(cursor="hand2")
        )
        self.canvas.tag_bind(
            "interactiveAc", "<Leave>",
            lambda e: self.canvas.config(cursor="")
        )

        # Left Action Panel (Navigation & Controls)
        action_width = 135
        btn_x1 = max(15, roomX1 - action_width - 15)
        btn_x2 = roomX1 - 15

        # 1. Return to Map Button (Persona 3 Crimson Action)
        back_y1 = roomY1 + 10
        back_y2 = back_y1 + 42
        self.canvas.create_rectangle(
            btn_x1, back_y1, btn_x2, back_y2,
            fill="#FF2A42", outline="#FFFFFF", width=1, tags="backBtn"
        )
        self.canvas.create_polygon(
            btn_x1, back_y1, btn_x1 + 10, back_y1, btn_x1, back_y1 + 10,
            fill="#FFFFFF", outline="", tags="backBtn"
        )
        self.canvas.create_text(
            (btn_x1 + btn_x2) / 2, (back_y1 + back_y2) / 2,
            text="◀ MAP VIEW", fill="#FFFFFF",
            font=("Segoe UI", 10, "bold"), tags="backBtn"
        )
        self.canvas.tag_bind("backBtn", "<Button-1>", lambda e: onBackClick())
        self.canvas.tag_bind("backBtn", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("backBtn", "<Leave>", lambda e: self.canvas.config(cursor=""))

        # 2. Edit Room Button (Persona 3 Electric Cyan Action)
        edit_y1 = back_y2 + 12
        edit_y2 = edit_y1 + 42
        self.canvas.create_rectangle(
            btn_x1, edit_y1, btn_x2, edit_y2,
            fill="#00A2FF", outline="#FFFFFF", width=1, tags="editBtn"
        )
        self.canvas.create_polygon(
            btn_x1, edit_y1, btn_x1 + 10, edit_y1, btn_x1, edit_y1 + 10,
            fill="#000000", outline="", tags="editBtn"
        )
        self.canvas.create_text(
            (btn_x1 + btn_x2) / 2, (edit_y1 + edit_y2) / 2,
            text="⚙ EDIT ROOM", fill="#000000",
            font=("Segoe UI", 10, "bold"), tags="editBtn"
        )
        if onEditClick:
            self.canvas.tag_bind("editBtn", "<Button-1>", lambda e: onEditClick())
            self.canvas.tag_bind("editBtn", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind("editBtn", "<Leave>", lambda e: self.canvas.config(cursor=""))

        # 3. Report Issue Button (Persona 3 Amber Warning Action)
        rep_y1 = edit_y2 + 12
        rep_y2 = rep_y1 + 42
        self.canvas.create_rectangle(
            btn_x1, rep_y1, btn_x2, rep_y2,
            fill="#F59E0B", outline="#FFFFFF", width=1, tags="reportBtn"
        )
        self.canvas.create_polygon(
            btn_x1, rep_y1, btn_x1 + 10, rep_y1, btn_x1, rep_y1 + 10,
            fill="#000000", outline="", tags="reportBtn"
        )
        self.canvas.create_text(
            (btn_x1 + btn_x2) / 2, (rep_y1 + rep_y2) / 2,
            text="⚠ REPORT ISSUE", fill="#000000",
            font=("Segoe UI", 9, "bold"), tags="reportBtn"
        )
        if onReportClick:
            self.canvas.tag_bind("reportBtn", "<Button-1>", lambda e: onReportClick(roomData))
            self.canvas.tag_bind("reportBtn", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind("reportBtn", "<Leave>", lambda e: self.canvas.config(cursor=""))

        # Japanese motif on side panel
        info_y = rep_y2 + 16
        self.canvas.create_text(
            btn_x1 + 5, info_y,
            anchor="nw", text="MARSUDIRINI AC\n遊びは終わりだ\nCLIMATE MONITOR",
            fill="#38BDF8", font=("Segoe UI", 8, "italic")
        )

    def showAcInfo(self, roomData, acIndex=0, onReportClick=None):
        # Display the selected AC's status and reporting modal.
        self.canvas.delete("ac_focus")

        canvasWidth = self.canvas.winfo_width() or 950
        canvasHeight = self.canvas.winfo_height() or 580

        # Semi-transparent dark overlay
        self.canvas.create_rectangle(
            0, 0, canvasWidth, canvasHeight,
            fill="#000000", stipple="gray50", outline="", tags="ac_focus"
        )

        modalW, modalH = 480, 430
        px1 = (canvasWidth - modalW) / 2
        py1 = (canvasHeight - modalH) / 2
        px2 = px1 + modalW
        py2 = py1 + modalH

        # Modal outer border & background
        self.canvas.create_rectangle(
            px1, py1, px2, py2,
            fill="#070D18", outline="#00D2FF", width=3, tags="ac_focus"
        )
        # Inner fine line
        self.canvas.create_rectangle(
            px1 + 4, py1 + 4, px2 - 4, py2 - 4,
            fill="", outline="#1E3A5F", width=1, tags="ac_focus"
        )

        # Corner cuts / geometric accents
        corner_sz = 14
        self.canvas.create_polygon(
            px1, py1, px1 + corner_sz, py1, px1, py1 + corner_sz,
            fill="#00D2FF", outline="", tags="ac_focus"
        )
        self.canvas.create_polygon(
            px2, py2, px2 - corner_sz, py2, px2, py2 - corner_sz,
            fill="#00D2FF", outline="", tags="ac_focus"
        )

        # Modal Header Bar
        self.canvas.create_rectangle(
            px1 + 4, py1 + 4, px2 - 4, py1 + 50,
            fill="#00A2FF", outline="", tags="ac_focus"
        )
        self.canvas.create_text(
            px1 + 20, py1 + 20,
            anchor="w", text="✦ EQUIPMENT TELEMETRY // AC STATUS",
            fill="#000000", font=("Segoe UI", 12, "bold"), tags="ac_focus"
        )
        self.canvas.create_text(
            px1 + 20, py1 + 38,
            anchor="w", text="MARSUDIRINI PROTOCOL • DEATH ARCANA STATUS",
            fill="#082F49", font=("Segoe UI", 8, "bold"), tags="ac_focus"
        )

        # Extract values
        acIds = roomData.get("acIds", [])
        selectedAc = acIds[acIndex] if acIndex < len(acIds) else f"{roomData.get('name', 'ROOM')}-AC-{acIndex+1}"

        def display(val):
            return "-" if val is None or val == "" else str(val)

        power_val = display(roomData.get("acPower", "ON")).upper()
        power_color = "#00FFCC" if power_val == "ON" else "#FF2A42"

        fields = [
            ("LOCATION / ROOM", display(roomData.get("name"))),
            ("HARDWARE IDENTIFIER", selectedAc),
            ("POWER STATUS", power_val),
            ("WALL TEMPERATURE", f"{display(roomData.get('temp'))} °C"),
            ("TOTAL AC UNITS", display(roomData.get("jumlahAc"))),
            ("AC BRAND / MODEL", display(roomData.get("merkAc"))),
            ("REMOTE CONTROLS", f"{display(roomData.get('remoteCount'))} Units"),
            ("REMOTE BRAND", display(roomData.get("remoteBrand"))),
            ("HEALTH CONDITION", display(roomData.get("acCondition") or "OPERATIONAL")),
        ]

        # Draw Field Rows
        row_y = py1 + 72
        for idx, (label, value) in enumerate(fields):
            if idx % 2 == 0:
                self.canvas.create_rectangle(
                    px1 + 16, row_y - 3, px2 - 16, row_y + 23,
                    fill="#0E1A2E", outline="", tags="ac_focus"
                )

            self.canvas.create_text(
                px1 + 25, row_y + 10,
                anchor="w", text=label,
                fill="#38BDF8", font=("Segoe UI", 9, "bold"), tags="ac_focus"
            )

            val_fill = power_color if label == "POWER STATUS" else "#FFFFFF"
            self.canvas.create_text(
                px2 - 25, row_y + 10,
                anchor="e", text=value,
                fill=val_fill, font=("Segoe UI", 10, "bold"), tags="ac_focus"
            )
            row_y += 28

        # Bottom Buttons Bar: Report Issue + Close
        btn_y = py2 - 32

        # 1. Report Issue Button
        r_w, r_h = 175, 36
        r_x = px1 + 120
        self.canvas.create_rectangle(
            r_x - r_w / 2, btn_y - r_h / 2,
            r_x + r_w / 2, btn_y + r_h / 2,
            fill="#F59E0B", outline="#FFFFFF", width=1, tags=("ac_focus", "reportAcBtn")
        )
        self.canvas.create_text(
            r_x, btn_y,
            text="⚠ REPORT THIS AC", fill="#000000",
            font=("Segoe UI", 9, "bold"), tags=("ac_focus", "reportAcBtn")
        )

        def handle_report_click():
            self.canvas.delete("ac_focus")
            if onReportClick:
                onReportClick(roomData, selectedAc)

        self.canvas.tag_bind("reportAcBtn", "<Button-1>", lambda e: handle_report_click())
        self.canvas.tag_bind("reportAcBtn", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("reportAcBtn", "<Leave>", lambda e: self.canvas.config(cursor=""))

        # 2. Close Button
        c_w, c_h = 135, 36
        c_x = px2 - 95
        self.canvas.create_rectangle(
            c_x - c_w / 2, btn_y - c_h / 2,
            c_x + c_w / 2, btn_y + c_h / 2,
            fill="#FF2A42", outline="#FFFFFF", width=1, tags=("ac_focus", "closeAcBtn")
        )
        self.canvas.create_text(
            c_x, btn_y,
            text="✕ CLOSE", fill="#FFFFFF",
            font=("Segoe UI", 9, "bold"), tags=("ac_focus", "closeAcBtn")
        )

        self.canvas.tag_bind("closeAcBtn", "<Button-1>", lambda e: self.canvas.delete("ac_focus"))
        self.canvas.tag_bind("closeAcBtn", "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("closeAcBtn", "<Leave>", lambda e: self.canvas.config(cursor=""))
