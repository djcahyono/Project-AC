import sys
import tkinter as tk
from pathlib import Path

src_dir = Path(__file__).resolve().parent
project_root = src_dir.parent

for candidate in (str(src_dir), str(project_root)):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)

try:
    from gui.Window import ACStatFullScreenApp
except ImportError as e:
    try:
        from src.gui.Window import ACStatFullScreenApp
    except ImportError:
        raise e

if __name__ == "__main__":
    root = tk.Tk()
    ACStatFullScreenApp(root)
    root.mainloop()
