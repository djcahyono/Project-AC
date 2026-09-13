class RoomDesigner:
    def __init__(self, canvas):
        self.canvas = canvas

    def drawRoomView(self, roomData, onAcClick, onBackClick):
        self.canvas.delete("all")

        canvasWidth = self.canvas.winfo_width() or 900
        canvasHeight = self.canvas.winfo_height() or 560
        roomX1 = max(140, min(180, canvasWidth * 0.18))
        roomY1 = 55
        roomX2, roomY2 = canvasWidth - 40, canvasHeight - 45
        roomWidth = roomX2 - roomX1
        roomHeight = roomY2 - roomY1

        self.canvas.create_rectangle(
            roomX1, roomY1, roomX2, roomY2,
            fill="#1E1E24", outline="#FF2A42", width=3, tags="room_element"
        )
        whiteboardX = roomX1 + roomWidth * 0.325
        self.canvas.create_rectangle(
            whiteboardX, roomY1 + 18,
            whiteboardX + roomWidth * 0.4, roomY1 + 27,
            fill="#F0F0F0", outline="#A0A0A0", tags="room_element"
        )

        chairWidth = max(44, min(48, roomWidth * 0.07))
        chairHeight = chairWidth * 0.55
        chairStartX = roomX1 + roomWidth * 0.25
        chairY = roomY1 + roomHeight * 0.18
        for row in range(6):
            for column in range(6):
                chairX = chairStartX + column * (chairWidth * 1.7)
                chairTop = chairY + row * (chairHeight * 2.0)
                self.canvas.create_rectangle(
                    chairX, chairTop,
                    chairX + chairWidth, chairTop + chairHeight,
                    fill="#8B5A2B", outline="#5A351A", tags="room_element"
                )

        acX = roomX1 + 18
        acWidth = max(45, min(67, roomWidth * 0.049))
        acHeight = max(84, min(109, roomHeight * 0.098))
        acIds = roomData.get(
            "acIds",
            [
                roomData.get("acId", "AC UNIT") + "-1",
                roomData.get("acId", "AC UNIT") + "-2",
            ],
        )
        for ac_index, fraction in enumerate((2 / 6, 4 / 6)):
            acY = roomY1 + roomHeight * fraction - 20
            acTag = f"interactiveAc{ac_index}"
            self.canvas.create_rectangle(
                acX, acY, acX + acWidth, acY + acHeight,
                fill="#E0E0E0", outline="#2B2D42", width=2,
                tags=("interactiveAc", acTag, "acElement")
            )
            self.canvas.create_line(
                acX + acWidth * 0.65, acY + 7,
                acX + acWidth * 0.65, acY + acHeight - 7,
                fill="#4A4E69", width=3,
                tags=("interactiveAc", acTag, "acElement")
            )
            self.canvas.create_oval(
                acX + 7, acY + 8, acX + 15, acY + 17,
                fill="#00FF66", outline="",
                tags=("interactiveAc", acTag, "acElement")
            )
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

        backX1 = max(10, roomX1 - 135)
        backX2 = roomX1 - 15
        backY1 = (roomY1 + roomY2 - 40) / 2
        backY2 = backY1 + 40
        self.canvas.create_rectangle(
            backX1, backY1, backX2, backY2,
            fill="#FF2A42", tags="backBtn"
        )
        self.canvas.create_text(
            (backX1 + backX2) / 2, (backY1 + backY2) / 2,
            text="< BACK TO MAP", fill="#FFFFFF",
            font=("Segoe UI", 10, "bold"), tags="backBtn"
        )
        self.canvas.tag_bind("backBtn", "<Button-1>", lambda e: onBackClick())
        self.canvas.tag_bind(
            "backBtn", "<Enter>",
            lambda e: self.canvas.config(cursor="hand2")
        )
        self.canvas.tag_bind(
            "backBtn", "<Leave>",
            lambda e: self.canvas.config(cursor="")
        )

    def showAcInfo(self, roomData, acIndex=0):
        self.canvas.delete("ac_focus")
        self.canvas.create_rectangle(
            0, 0,
            self.canvas.winfo_width() or 1200,
            self.canvas.winfo_height() or 700,
            fill="#000000", stipple="gray50", outline="", tags="ac_focus"
        )

        panel_x, panel_y = 300, 100
        self.canvas.create_rectangle(
            panel_x, panel_y, 650, 470,
            fill="#101318", outline="#00ADB5", width=2,
            tags="ac_focus"
        )
        acIds = roomData.get("acIds", [])
        selectedAc = acIds[acIndex] if acIndex < len(acIds) else roomData.get("acId", "AC UNIT")

        def display(value):
            return "-" if value is None or value == "" else str(value)

        details = (
            f"Room: {display(roomData.get('name'))}\n"
            f"AC: {display(selectedAc)}\n"
            f"Power: {display(roomData.get('acPower'))}\n"
            f"Temperature: {display(roomData.get('temp'))}\n"
            f"AC units: {display(roomData.get('jumlahAc'))}\n"
            f"AC brand: {display(roomData.get('merkAc'))}\n"
            f"Remotes: {display(roomData.get('remoteCount'))}\n"
            f"Remote brand: {display(roomData.get('remoteBrand'))}\n"
            f"Condition: {display(roomData.get('acCondition'))}"
        )
        self.canvas.create_text(
            panel_x + 24, panel_y + 28,
            anchor="nw", text=details,
            fill="#FFFFFF", font=("Segoe UI", 12),
            tags="ac_focus"
        )
        self.canvas.tag_bind(
            "ac_focus", "<Button-1>",
            lambda e: self.canvas.delete("ac_focus")
        )
        self.canvas.tag_bind(
            "ac_focus", "<Enter>",
            lambda e: self.canvas.config(cursor="hand2")
        )
        self.canvas.tag_bind(
            "ac_focus", "<Leave>",
            lambda e: self.canvas.config(cursor="")
        )
