from abc import ABC, abstractmethod
import tkinter as tk


class BasePersonaModal(ABC):
    """
    Abstract Base Class for Persona 3 Reload styled Modals & Dialogs.
    Demonstrates:
    - Abstraction: Uses abc.ABC and @abstractmethod to enforce uniform interface.
    - Template Method Pattern: Defines the initialization lifecycle (header, body, footer).
    - Inheritance & Polymorphism: Specific dialogs inherit from this base class and
      polymorphically implement setup_body() with unique UI layouts and interactions.
    """

    def __init__(self, parent_root, title, theme=None, geometry="520x440"):
        self.root = parent_root
        self.title_text = title
        self.theme = theme or {
            "card_bg": "#0A0F1D",
            "top_bg": "#00A2FF",
            "top_fg": "#000000",
            "text": "#FFFFFF",
            "muted": "#38BDF8",
            "accent": "#00D2FF",
            "danger": "#FF2A42",
            "btn_bg": "#0F172A",
            "btn_fg": "#FFFFFF",
        }

        self.window = tk.Toplevel(self.root)
        self.window.title(self.title_text)
        self.window.geometry(geometry)
        self.window.transient(self.root)
        self.window.grab_set()
        self.window.configure(bg=self.theme["card_bg"])

        self.setup_header()
        self.setup_body()
        self.setup_footer()

    def setup_header(self):
        """Reusable Persona 3 electric cyan header banner."""
        self.header_frame = tk.Frame(self.window, bg=self.theme["top_bg"], height=38)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)

        tk.Label(
            self.header_frame, text=f"✦ {self.title_text}",
            font=("Segoe UI", 11, "bold"), bg=self.theme["top_bg"], fg=self.theme["top_fg"]
        ).pack(side="left", padx=16, pady=8)

    @abstractmethod
    def setup_body(self):
        """Abstract method implemented polymorphically by child modals."""
        pass

    def setup_footer(self):
        """Optional hook for custom modal footers."""
        pass

    def close(self):
        """Encapsulated window termination."""
        self.window.destroy()
