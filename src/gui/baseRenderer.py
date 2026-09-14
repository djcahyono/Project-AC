from abc import ABC, abstractmethod


# =====================================================================
# OOP Principle: Abstraction -- Shared Abstract Base for All Renderers
# =====================================================================
class BaseRenderer(ABC):
    # Abstract base class for canvas renderers.
    # Subclasses share canvas management and implement their own render method.

    def __init__(self, canvas):
        self._canvas = canvas  # Encapsulated via private attribute

    @property
    def canvas(self):
        # Encapsulated canvas getter.
        return self._canvas

    @canvas.setter
    def canvas(self, value):
        # Encapsulated canvas setter.
        self._canvas = value

    @abstractmethod
    def render(self, *args, **kwargs):
        # Polymorphic render entry point. CanvasAnimationManager draws a map;
        # RoomDesigner draws the detailed room interior.
        pass

    def clear(self):
        # Shared utility inherited by all renderers.
        self._canvas.delete("all")
