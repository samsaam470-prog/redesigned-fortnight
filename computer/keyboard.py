"""
Collin Computer Keyboard Controller

Low-level keyboard operations for Collin.
"""

import time

try:
    import pyautogui
except ImportError:
    pyautogui = None


class KeyboardController:
    """Controls the computer keyboard."""

    def __init__(self) -> None:
        if pyautogui is None:
            raise RuntimeError(
                "PyAutoGUI is not installed. "
                "Install it with: pip install pyautogui"
            )

        self.keyboard = pyautogui

    def type_text(
        self,
        text: str,
        interval: float = 0.01,
    ) -> None:
        """Type text."""

        if not isinstance(text, str):
            raise TypeError("text must be a string.")

        self.keyboard.write(
            text,
            interval=interval,
        )

    def press(self, key: str) -> None:
        """Press a single key."""

        self.keyboard.press(key)

    def hotkey(self, *keys: str) -> None:
        """Press a keyboard combination."""

        if not keys:
            raise ValueError("At least one key is required.")

        self.keyboard.hotkey(*keys)

    def copy(self) -> None:
        """Copy the current selection."""
        self.hotkey("ctrl", "c")

    def paste(self) -> None:
        """Paste clipboard contents."""
        self.hotkey("ctrl", "v")

    def cut(self) -> None:
        """Cut the current selection."""
        self.hotkey("ctrl", "x")

    def select_all(self) -> None:
        """Select everything in the active application."""
        self.hotkey("ctrl", "a")

    def save(self) -> None:
        """Save the current document/application."""
        self.hotkey("ctrl", "s")

    def undo(self) -> None:
        """Undo the previous action."""
        self.hotkey("ctrl", "z")

    def wait(self, seconds: float = 0.2) -> None:
        """Wait between keyboard actions."""
        time.sleep(seconds)


def main() -> None:
    """Safe keyboard controller test."""

    controller = KeyboardController()

    print("Keyboard controller: OK")
    print("Keyboard methods available:")
    print("- type_text")
    print("- press")
    print("- hotkey")
    print("- copy")
    print("- paste")
    print("- cut")
    print("- select_all")
    print("- save")
    print("- undo")


if __name__ == "__main__":
    main()
