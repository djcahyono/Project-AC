import tkinter as tk
from roomDesign import RoomDesigner

class CanvasAnimationManager:
    #Handles canvas rendering, room hovering, zoom-to-menu transitions, and slide animations.
    
    def __init__(self, canvas, root, themeGetter):
        self.canvas = canvas
        self.root = root
        self.getTheme = themeGetter
        
        self.isAnimating = False
        self.activeRoom = None
        self.isInRoomMenu = False
        self.roomDesigner = RoomDesigner(canvas)

    def drawFloorItems(self, floorData, floorName, hoverCallback, clickCallback, offsetX=0):
        for room in floorData:
            name = room["name"]
            x1, y1, x2, y2 = room["coords"]
            fillColor = self.getTemperatureColor(room)
            
            rectTag = f"{name}Rect"

            # Draw Room Box
            self.canvas.create_rectangle(
                x1 + offsetX, y1, x2 + offsetX, y2,
                fill=fillColor, outline="#690000", width=2,
                tags=(name, rectTag, "floorItems")
            )

            # Draw Room Label
            self.canvas.create_text(
                (x1 + x2) / 2 + offsetX, (y1 + y2) / 2,
                text=name, justify="center",
                font=("Segoe UI", 11, "bold"), fill="#FFFFFF",
                tags=(name, "floorItems")
            )

            # Only classroom rooms open the interactive room view.
            if room.get("hasStats", True):
                self.canvas.tag_bind(name, "<Enter>", lambda e, r=room: hoverCallback(r, True))
                self.canvas.tag_bind(name, "<Leave>", lambda e, r=room: hoverCallback(r, False))
                self.canvas.tag_bind(name, "<Button-1>", lambda e, r=room: clickCallback(r))
    #color determination based on temperature and AC power state
    @staticmethod
    def getTemperatureColor(room):
        if room.get("acPower") == "OFF":
            return "#616161"

        temperature = room.get("temp")
        if temperature is None:
            return "#757575"
        if temperature >= 75:
            return "#FF5722"
        if temperature >= 73:
            return "#FFC107"
        return "#00ADB5"

    def hoverZoom(self, roomData, entering):
        # Expands room bounds slightly on mouse hover.
        if self.isAnimating or self.isInRoomMenu:
            return

        rectTag = f"{roomData['name']}Rect"
        x1, y1, x2, y2 = roomData["coords"]

        if entering:
            zoom = 8
            self.canvas.coords(rectTag, x1 - zoom, y1 - zoom, x2 + zoom, y2 + zoom)
            self.canvas.itemconfig(rectTag, outline="#FFFFFF", width=3)
        else:
            self.canvas.coords(rectTag, x1, y1, x2, y2)
            self.canvas.itemconfig(rectTag, outline="#1254A0", width=2)

    def zoomIntoRoom(self, roomData, onCompleteCallback, step=0, totalSteps=18):
        # Animates canvas scaling centered on the clicked room object.
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

        # Target center calculation
        canvasWidth = self.canvas.winfo_width() or 900
        canvasHeight = self.canvas.winfo_height() or 500
        screenCx, screenCy = canvasWidth / 2, canvasHeight / 2
        objectCx, objectCy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2

        scaleFactor = 1.12
        dx = (screenCx - objectCx) * 0.3
        dy = (screenCy - objectCy) * 0.3

        self.canvas.move("all", dx, dy)
        self.canvas.scale("all", screenCx, screenCy, scaleFactor, scaleFactor)

        if step < totalSteps:
            self.root.after(16, lambda: self.zoomIntoRoom(roomData, onCompleteCallback, step + 1, totalSteps))
        else:
            self.isAnimating = False
            onCompleteCallback(roomData)

    def zoomOutOfRoom(self, onCompleteCallback, step=0, totalSteps=18):
        # Reverses the zoom-in animation to return to the original canvas view.
        if step == 0:
            if self.isAnimating:
                return
            self.isAnimating = True

        scaleFactor = 1 / 1.12
        canvasWidth = self.canvas.winfo_width() or 900
        canvasHeight = self.canvas.winfo_height() or 500
        screenCx, screenCy = canvasWidth / 2, canvasHeight / 2

        self.canvas.scale("all", screenCx, screenCy, scaleFactor, scaleFactor)
        self.canvas.move("all", -((screenCx - screenCx) * 0.3), -((screenCy - screenCy) * 0.3))

        if step < totalSteps:
            self.root.after(16, lambda: self.zoomOutOfRoom(onCompleteCallback, step + 1, totalSteps))
        else:
            self.isAnimating = False
            self.isInRoomMenu = False
            onCompleteCallback()

    def zoomOutRoomView(self, onCompleteCallback, step=0, totalSteps=12):
        # Animates the room scene away before returning to the floor map.
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

    def drawRoomView(self, roomData, onAcClick, onBackClick):
        self.isInRoomMenu = True
        self.activeRoom = roomData
        self.roomDesigner.drawRoomView(roomData, onAcClick, onBackClick)

    def drawRoomMenuOverlay(self, roomData, backCallback):
        # Keep the public API used by Window.py while rendering the room view.
        self.drawRoomView(
            roomData,
            onAcClick=lambda acIndex: self.showAcInfo(roomData, acIndex),
            onBackClick=backCallback,
        )

    def showAcInfo(self, roomData, acIndex=0):
        self.roomDesigner.showAcInfo(roomData, acIndex)

    def changeFloorSlide(self, targetFloorData, targetFloorName, direction, hoverCallback, clickCallback, onComplete):
        # Executes directional floor transition slide animation (left or right).
        if self.isAnimating:
            return
            
        self.isAnimating = True
        
        # Tag active items to move them out
        for item in self.canvas.find_withtag("floorItems"):
            self.canvas.addtag_withtag("oldFloorItems", item)
            self.canvas.dtag(item, "floorItems")

        # Determine slide direction:
        # Going UP a floor -> new floor slides in from Right (+1500 -> move left)
        # Going DOWN a floor -> new floor slides in from Left (-1500 -> move right)
        slideDistance = 1500 if direction == "up" else -1500
        
        self.drawFloorItems(targetFloorData, targetFloorName, hoverCallback, clickCallback, offsetX=slideDistance)
        self.animateSlide(0, slideDistance, direction, onComplete)

    def animateSlide(self, currentMoved, totalToMove, direction, onComplete):
        stepValue = 100
        # Determine movement vector based on direction
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

    def backgroundAnimation():
        pass