from abc import ABC, abstractmethod


# =====================================================================
# OOP Principle: Abstraction -- Shared Abstract Base for All Renderers
# =====================================================================
class BaseRenderer(ABC):
    """
    Abstract Base Class for all canvas-based UI renderers in the facility system.
    Demonstrates:
    - Abstraction: @abstractmethod enforces a uniform render() interface.
    - Inheritance: CanvasAnimationManager and RoomDesigner both inherit this.
    - Polymorphism: Each subclass overrides render() with a distinct implementation.
    - Encapsulation: canvas is managed through this base, not duplicated per subclass.
    """

    def __init__(self, canvas):
        self._canvas = canvas  # Encapsulated via private attribute

    @property
    def canvas(self):
        """Encapsulated canvas getter."""
        return self._canvas

    @canvas.setter
    def canvas(self, value):
        """Encapsulated canvas setter -- allows subclasses to rebind the canvas."""
        self._canvas = value

    @abstractmethod
    def render(self, *args, **kwargs):
        """
        Polymorphic render entry point.
        - CanvasAnimationManager.render() draws a floor map with all rooms
        - RoomDesigner.render()           draws the detailed room interior view
        Each subclass implements this differently -- that IS polymorphism.
        """
        pass

    def clear(self):
        """
        Shared utility inherited by all renderers.
        Demonstrates how shared behavior lives in the base class (DRY principle).
        """
        self._canvas.delete("all")
