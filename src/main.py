import sys
import tkinter as tk
from pathlib import Path

src_dir = Path(__file__).resolve().parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

try:
    from gui.Window import ACStatFullScreenApp
except ModuleNotFoundError:
    from src.gui.Window import ACStatFullScreenApp

if __name__ == "__main__":
    root = tk.Tk()
    ACStatFullScreenApp(root)
    root.mainloop()

