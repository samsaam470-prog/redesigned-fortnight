"""
Collin Computer Screen Controller

Screen observation and screenshot functions for Collin.
"""

from pathlib import Path
from datetime import datetime

try:
    import pyautogui
except ImportError:
    pyautogui = None


class ScreenController:
    """Provides basic screen observation."""

    def __init__(self) -> None:
        if pyautogui is None:
            raise RuntimeError(
                "PyAutoGUI is not installed. "
                "Install it with: pip install pyautogui"
            )

        self.screen = pyautogui

    def size(self) -> tuple[int, int]:
        """Return the screen size."""

        width, height = self.screen.size()

        return int(width), int(height)

    def screenshot(self, path: str | None = None):
        """
        Capture a screenshot.

        If path is provided, save the screenshot there.
        Otherwise return the screenshot object.
        """

        image = self.screen.screenshot()

        if path:
            output = Path(path).expanduser().resolve()
            output.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            image.save(output)
            return str(output)

        return image

    def save_screenshot(
        self,
        folder: str = "screenshots",
    ) -> str:
        """Save a timestamped screenshot."""

        directory = Path(folder).expanduser().resolve()
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output = directory / f"screen_{timestamp}.png"

        self.screenshot(str(output))

        return str(output)

    def pixel(
        self,
        x: int,
        y: int,
    ) -> tuple[int, int, int]:
        """Return the RGB value of a screen pixel."""

        return tuple(self.screen.pixel(x, y))


def main() -> None:
    """Safe screen controller test."""

    controller = ScreenController()

    print("Screen controller: OK")
    print("Screen size:", controller.size())


if __name__ == "__main__":
    main()
