import tkinter as tk

def toggle_fullscreen(event=None):
    is_fullscreen = root.attributes("-fullscreen")
    root.attributes("-fullscreen", not is_fullscreen)

def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)
# window
root = tk.Tk()
root.title("AC stat")

# Dark Color
BG_DARK = "#121212"
CARD_BG = "#1E1E1E"
TEXT_MAIN = "#FFFFFF"
TEXT_MUTED = "#888888"
# Apply Dark Background to Root
root.configure(bg=BG_DARK)
# Enable Fullscreen by Default (anjay ada autonya co)
root.size = (800, 600)
# Keyboard Shortcuts
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", exit_fullscreen)

# Main Container
container = tk.Frame(root, bg=BG_DARK)
container.pack(expand=True, fill="both", padx=40, pady=40)

# Title Label
title_label = tk.Label(
    container,
    text="AC Stat",
    font=("Segoe UI", 32, "bold"),
    fg=TEXT_MAIN,
    bg=BG_DARK
)
title_label.pack(anchor="w", pady=(0, 20))

# Status Display Card
status_card = tk.Frame(container, bg=CARD_BG, width=300, height=150)
status_card.pack_propagate(False)  # Retains exact dimensions
status_card.pack(anchor="w")

card_title = tk.Label(
    status_card, 
    text="System Status", 
    font=("Segoe UI", 12), 
    fg=TEXT_MUTED, 
    bg=CARD_BG
)
card_title.pack(anchor="w", padx=20, pady=(15, 0))
# will be replaced with Denah SMA, dan clickable stuff, probably would use that on another thing tho
# also should add a dashboard for other stuff and animation (HOPEFULLY DOABLE ON LIKE WEEKEND, MARSUD BE NICE)
card_val = tk.Label(
    status_card, 
    text="Placeholder", 
    font=("Segoe UI", 28, "bold"), 
    fg="#00ADB5", 
    bg=CARD_BG
)
card_val.pack(anchor="w", padx=20)

hint_label = tk.Label(
    container,
    text="Press [ESC] to exit fullscreen | [F11] to toggle fullscreen",
    font=("Segoe UI", 10),
    fg=TEXT_MUTED,
    bg=BG_DARK
)
hint_label.pack(side="bottom", anchor="w")

root.mainloop()