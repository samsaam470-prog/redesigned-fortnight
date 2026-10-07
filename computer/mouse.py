"""
Collin Computer Mouse Controller

Low-level mouse operations for Collin.
"""

import time

try:
    import pyautogui
except ImportError:
    pyautogui = None


class MouseController:
    """Controls the computer mouse."""

    def __init__(self) -> None:
        if pyautogui is None:
            raise RuntimeError(
                "PyAutoGUI is not installed. "
                "Install it with: pip install pyautogui"
            )

        self.mouse = pyautogui

    def position(self) -> tuple[int, int]:
        """Return the current mouse position."""
        x, y = self.mouse.position()
        return int(x), int(y)

    def move_to(
        self,
        x: int,
        y: int,
        duration: float = 0.2,
    ) -> None:
        """Move the mouse to a screen position."""

        self.mouse.moveTo(
            x,
            y,
            duration=duration,
        )

    def click(
        self,
        x: int | None = None,
        y: int | None = None,
        button: str = "left",
        clicks: int = 1,
    ) -> None:
        """Click at the current or specified position."""

        if x is not None and y is not None:
            self.move_to(x, y)

        self.mouse.click(
            button=button,
            clicks=clicks,
        )

    def double_click(
        self,
        x: int | None = None,
        y: int | None = None,
    ) -> None:
        """Perform a double click."""

        if x is not None and y is not None:
            self.move_to(x, y)

        self.mouse.doubleClick()

    def right_click(
        self,
        x: int | None = None,
        y: int | None = None,
    ) -> None:
        """Perform a right click."""

        if x is not None and y is not None:
            self.move_to(x, y)

        self.mouse.rightClick()

    def scroll(self, amount: int) -> None:
        """Scroll vertically."""

        self.mouse.scroll(amount)

    def drag_to(
        self,
        x: int,
        y: int,
        duration: float = 0.5,
        button: str = "left",
    ) -> None:
        """Drag the mouse to a position."""

        self.mouse.dragTo(
            x,
            y,
            duration=duration,
            button=button,
        )

    def pause(self, seconds: float = 0.2) -> None:
        """Pause between computer actions."""

        time.sleep(seconds)


def main() -> None:
    """Safe mouse controller test."""

    controller = MouseController()

    print("Mouse controller: OK")
    print("Current position:", controller.position())


if __name__ == "__main__":
    main()
