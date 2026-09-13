import unittest

from src.gui.Window import ACStatFullScreenApp


class FloorChangeTests(unittest.TestCase):
    def test_change_floor_after_room_updates_selection_without_error(self):
        app = object.__new__(ACStatFullScreenApp)

        class DummyAnimator:
            isAnimating = False
            isInRoomMenu = False

            def changeFloorSlide(self, *args, **kwargs):
                pass

        app.animator = DummyAnimator()
        app.current_floor = "Floor 1"
        app.floorsData = {"Floor 1": [], "Floor 2": []}
        app.updateFloorSelection = lambda: None

        app.changeFloorAfterRoom("Floor 2")

        self.assertEqual(app.current_floor, "Floor 2")


if __name__ == "__main__":
    unittest.main()
