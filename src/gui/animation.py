import sys
import tkinter as tk
from pathlib import Path

src_dir = Path(__file__).resolve().parents[1]
for candidate in (str(src_dir), str(src_dir.parent)):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

try:
    from gui.roomDesign import RoomDesigner
except ModuleNotFoundError:
    from src.gui.roomDesign import RoomDesigner

class CanvasAnimationManager:
    """Handles canvas rendering, room hovering, zoom-to-menu transitions, and slide animations."""

    def __init__(self, canvas, root, themeGetter):
        self.canvas = canvas
        self.root = root
        self.getTheme = themeGetter

        self.isAnimating = False
        self.activeRoom = None
        self.isInRoomMenu = False
        self.roomDesigner = RoomDesigner(canvas)

    def drawFloorItems(self, floorData, floorName, hoverCallback, clickCallback, offsetX=0):
        # Draw background tactical grid accents if on main map
        if not self.isInRoomMenu:
            self._drawMapBackground(offsetX)

        for room in floorData:
            name = room["name"]
            x1, y1, x2, y2 = room["coords"]
            fillColor, outlineColor, accentColor = self.getRoomThemeColors(room)

            rectTag = f"{name}Rect"
            roomTag = name
            itemTags = (roomTag, "floorItems")

            # Main Room Box
            self.canvas.create_rectangle(
                x1 + offsetX, y1, x2 + offsetX, y2,
                fill=fillColor, outline=outlineColor, width=2,
                tags=(roomTag, rectTag, "floorItems")
            )

            # Special single large banner for "coming soon"
            if name.lower() == "coming soon":
                cx = (x1 + x2) / 2 + offsetX
                cy = (y1 + y2) / 2
                self.canvas.create_text(
                    cx, cy - 20,
                    text="SECTOR UNDER CONSTRUCTION // MARSUDIRINI LEVEL 4",
                    font=("Segoe UI", 16, "bold"), fill="#00D2FF",
                    tags=itemTags
                )
                self.canvas.create_text(
                    cx, cy + 15,
                    text="NO TELEMETRY AVAILABLE • ACCESS RESTRICTED TO SEES OPERATIVES",
                    font=("Segoe UI", 10, "italic"), fill="#94A3B8",
                    tags=itemTags
                )
                continue

            # Non-classroom facility tags (R. Data, R. TU, Ruang Guru, etc.)
            hasStats = room.get("hasStats", True)
            if not hasStats:
                cx = (x1 + x2) / 2 + offsetX
                cy = (y1 + y2) / 2
                self.canvas.create_text(
                    cx, cy - 8,
                    text=name, justify="center",
                    font=("Segoe UI", 11, "bold"), fill="#E2E8F0",
                    tags=itemTags
                )
                self.canvas.create_text(
                    cx, cy + 12,
                    text="FACILITY / STAFF", justify="center",
                    font=("Segoe UI", 8, "bold"), fill="#64748B",
                    tags=itemTags
                )
                continue

            # Classroom Rooms (Interactive)
            # 1. Corner accent brackets
            self._drawCornerBrackets(x1 + offsetX, y1, x2 + offsetX, y2, accentColor, f"{name}Bracket", roomTag)

            # 2. Room Code Title
            cx = (x1 + x2) / 2 + offsetX
            cy = (y1 + y2) / 2
            self.canvas.create_text(
                cx, cy - 10,
                text=name, justify="center",
                font=("Segoe UI", 13, "bold"), fill="#FFFFFF",
                tags=itemTags
            )

            # 3. Temperature & Power Telemetry Strip
            temp = room.get("temp")
            temp_text = f"{temp:.0f}°C" if temp is not None else "--°C"
            power = str(room.get("acPower", "ON")).upper()
            status_color = "#00FFCC" if power == "ON" else "#FF2A42"

            # Mini telemetry pill
            pill_y = cy + 16
            self.canvas.create_text(
                cx - 10, pill_y,
                text=temp_text, font=("Segoe UI", 9, "bold"),
                fill=accentColor, tags=itemTags
            )

            # Glowing status dot
            self.canvas.create_oval(
                cx + 18, pill_y - 4, cx + 26, pill_y + 4,
                fill=status_color, outline="", tags=itemTags
            )

            # Interaction bindings
            self.canvas.tag_bind(roomTag, "<Enter>", lambda e, r=room: hoverCallback(r, True))
            self.canvas.tag_bind(roomTag, "<Leave>", lambda e, r=room: hoverCallback(r, False))
            self.canvas.tag_bind(roomTag, "<Button-1>", lambda e, r=room: clickCallback(r))

    def _drawMapBackground(self, offsetX=0):
        w = self.canvas.winfo_width() or 1000
        h = self.canvas.winfo_height() or 600
        # Subtle cyber grid markers
        for gx in range(50, w, 120):
            for gy in range(50, h, 120):
                self.canvas.create_text(
                    gx + offsetX, gy, text="+",
                    fill="#111C2E", font=("Segoe UI", 8),
                    tags="floorItems"
                )

    def _drawCornerBrackets(self, x1, y1, x2, y2, color, tag, roomTag):
        blen = 8
        coords = [
            (x1, y1, x1 + blen, y1, x1, y1 + blen),
            (x2, y1, x2 - blen, y1, x2, y1 + blen),
            (x1, y2, x1 + blen, y2, x1, y2 - blen),
            (x2, y2, x2 - blen, y2, x2, y2 - blen),
        ]
        for bx, by, px, py, qx, qy in coords:
            self.canvas.create_line(bx, by, px, py, fill=color, width=2, tags=(roomTag, tag, "floorItems"))
            self.canvas.create_line(bx, by, qx, qy, fill=color, width=2, tags=(roomTag, tag, "floorItems"))

    @staticmethod
    def getRoomThemeColors(room):
        """Returns (fillColor, outlineColor, accentColor) in Persona 3 Dark Hour palette."""
        hasStats = room.get("hasStats", True)
        if not hasStats:
            return ("#0B111D", "#1E293B", "#64748B")

        power = str(room.get("acPower", "ON")).upper()
        if power == "OFF":
            return ("#131B29", "#334155", "#64748B")

        temp = room.get("temp")
        if temp is None:
            return ("#0E1726", "#1E293B", "#94A3B8")
        if temp >= 25:
            # Danger / Hot -> Persona Crimson
            return ("#2D0B14", "#FF2A42", "#FF4D6D")
        if temp >= 23:
            # Moderate -> Warm Amber
            return ("#221A08", "#F59E0B", "#FBBF24")
        # Cool / Optimal -> Electric Cyan
        return ("#061E34", "#00A2FF", "#00D2FF")

    def hoverZoom(self, roomData, entering):
        """Persona 3 targeting reticle and highlight expansion on hover."""
        if self.isAnimating or self.isInRoomMenu:
            return

        rectTag = f"{roomData['name']}Rect"
        bracketTag = f"{roomData['name']}Bracket"
        x1, y1, x2, y2 = roomData["coords"]

        if entering:
            zoom = 6
            self.canvas.coords(rectTag, x1 - zoom, y1 - zoom, x2 + zoom, y2 + zoom)
            self.canvas.itemconfig(rectTag, outline="#00FFFF", width=3)
            self.canvas.itemconfig(bracketTag, fill="#FFFFFF")
            self.canvas.config(cursor="hand2")
        else:
            self.canvas.coords(rectTag, x1, y1, x2, y2)
            fillColor, outlineColor, accentColor = self.getRoomThemeColors(roomData)
            self.canvas.itemconfig(rectTag, outline=outlineColor, width=2)
            self.canvas.itemconfig(bracketTag, fill=accentColor)
            self.canvas.config(cursor="")

    def zoomIntoRoom(self, roomData, onCompleteCallback, step=0, totalSteps=16):
        """Animates canvas scaling centered on the clicked room object."""
        if step == 0:
            if self.isAnimating:
                return
            self.isAnimating = True
            self.isInRoomMenu = True

        tag = roomData["name"]
        bbox = self.canvas.bbox(tag)
        if not bbox:
            self.isAnimating = False
            return

        canvasWidth = self.canvas.winfo_width() or 900
        canvasHeight = self.canvas.winfo_height() or 500
        screenCx, screenCy = canvasWidth / 2, canvasHeight / 2
        objectCx, objectCy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2

        scaleFactor = 1.14
        dx = (screenCx - objectCx) * 0.32
        dy = (screenCy - objectCy) * 0.32

        self.canvas.move("all", dx, dy)
        self.canvas.scale("all", screenCx, screenCy, scaleFactor, scaleFactor)

        if step < totalSteps:
            self.root.after(16, lambda: self.zoomIntoRoom(roomData, onCompleteCallback, step + 1, totalSteps))
        else:
            self.isAnimating = False
            onCompleteCallback(roomData)

    def zoomOutOfRoom(self, onCompleteCallback, step=0, totalSteps=16):
        if step == 0:
            if self.isAnimating:
                return
            self.isAnimating = True

        scaleFactor = 1 / 1.14
        canvasWidth = self.canvas.winfo_width() or 900
        canvasHeight = self.canvas.winfo_height() or 500
        screenCx, screenCy = canvasWidth / 2, canvasHeight / 2

        self.canvas.scale("all", screenCx, screenCy, scaleFactor, scaleFactor)

        if step < totalSteps:
            self.root.after(16, lambda: self.zoomOutOfRoom(onCompleteCallback, step + 1, totalSteps))
        else:
            self.isAnimating = False
            self.isInRoomMenu = False
            onCompleteCallback()

    def zoomOutRoomView(self, onCompleteCallback, step=0, totalSteps=12):
        if step == 0:
            if self.isAnimating:
                return
            self.isAnimating = True
            self.canvas.delete("ac_focus")

        canvasWidth = self.canvas.winfo_width() or 1200
        canvasHeight = self.canvas.winfo_height() or 700
        self.canvas.scale("all", canvasWidth / 2, canvasHeight / 2, 0.88, 0.88)
        if step < totalSteps:
            self.root.after(16, lambda: self.zoomOutRoomView(onCompleteCallback, step + 1, totalSteps))
        else:
            self.isAnimating = False
            self.isInRoomMenu = False
            self.canvas.delete("all")
            onCompleteCallback()

    def drawRoomView(self, roomData, onAcClick, onBackClick, onEditClick=None, onReportClick=None):
        self.isInRoomMenu = True
        self.activeRoom = roomData
        self.roomDesigner.drawRoomView(roomData, onAcClick, onBackClick, onEditClick, onReportClick)

    def drawRoomMenuOverlay(self, roomData, backCallback, editCallback=None, reportCallback=None):
        self.drawRoomView(
            roomData,
            onAcClick=lambda acIndex: self.showAcInfo(roomData, acIndex, reportCallback),
            onBackClick=backCallback,
            onEditClick=editCallback,
            onReportClick=reportCallback,
        )

    def showAcInfo(self, roomData, acIndex=0, reportCallback=None):
        self.roomDesigner.showAcInfo(roomData, acIndex, onReportClick=reportCallback)

    def changeFloorSlide(self, targetFloorData, targetFloorName, direction, hoverCallback, clickCallback, onComplete):
        if self.isAnimating:
            return

        self.isAnimating = True

        for item in self.canvas.find_withtag("floorItems"):
            self.canvas.addtag_withtag("oldFloorItems", item)
            self.canvas.dtag(item, "floorItems")

        slideDistance = 1500 if direction == "up" else -1500

        self.drawFloorItems(targetFloorData, targetFloorName, hoverCallback, clickCallback, offsetX=slideDistance)
        self.animateSlide(0, slideDistance, direction, onComplete)

    def animateSlide(self, currentMoved, totalToMove, direction, onComplete):
        stepValue = 100
        step = -stepValue if direction == "up" else stepValue
        absTotal = abs(totalToMove)

        if currentMoved + stepValue > absTotal:
            remaining = absTotal - currentMoved
            step = -remaining if direction == "up" else remaining

        self.canvas.move("oldFloorItems", step, 0)
        self.canvas.move("floorItems", step, 0)

        currentMoved += stepValue

        if currentMoved < absTotal:
            self.root.after(16, lambda: self.animateSlide(currentMoved, totalToMove, direction, onComplete))
        else:
            self.canvas.delete("oldFloorItems")
            self.isAnimating = False
            onComplete()