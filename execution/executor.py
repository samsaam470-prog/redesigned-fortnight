"""
Collin Execution Layer
"""

import pyautogui

from language.intent import Intent, IntentType
from computer.mouse import MouseController
from computer.keyboard import KeyboardController
from chrome.controller import ChromeController
from vscode.controller import VSCodeController
from windows.explorer import WindowsExplorerController


class Executor:
    """Executes Collin intents using computer controllers."""

    # Approximate pixels per centimetre.
    # This is intentionally configurable because Windows DPI scaling
    # and display density can differ between computers.
    PIXELS_PER_CM = 38

    def __init__(self) -> None:
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.chrome = ChromeController()
        self.vscode = VSCodeController()
        self.explorer = WindowsExplorerController()

    def execute(self, intent: Intent) -> bool:
        if not isinstance(intent, Intent):
            raise TypeError("intent must be an Intent instance.")

        intent_type = intent.type

        if intent_type == IntentType.OPEN_APPLICATION:
            return self._open_application(intent.target)

        if intent_type == IntentType.CLOSE_APPLICATION:
            return self._close_application(intent.target)

        if intent_type == IntentType.OPEN_URL:
            return self._open_url(intent.value or intent.target)

        if intent_type == IntentType.SEARCH:
            return self._search(intent.value)

        if intent_type == IntentType.CLICK:
            return self._click()

        if intent_type == IntentType.TYPE:
            return self._type(intent.value)

        if intent_type == IntentType.SCROLL:
            return self._scroll(intent.direction)

        if intent_type == IntentType.COPY:
            self.keyboard.copy()
            return True

        if intent_type == IntentType.PASTE:
            self.keyboard.paste()
            return True

        if intent_type == IntentType.CUT:
            self.keyboard.cut()
            return True

        if intent_type == IntentType.SAVE:
            self.keyboard.save()
            return True

        if intent_type == IntentType.UNDO:
            self.keyboard.undo()
            return True

        if intent_type == IntentType.SELECT_ALL:
            self.keyboard.hotkey("ctrl", "a")
            return True

        if intent_type == IntentType.SEND:
            self.keyboard.press("enter")
            return True

        if intent_type == IntentType.MOVE_CURSOR:
            return self._move_cursor(
                intent.direction,
                intent.amount,
            )

        if intent_type == IntentType.OPEN_NEW_TAB:
            self.keyboard.hotkey("ctrl", "t")
            return True

        if intent_type == IntentType.CLOSE_TAB:
            self.keyboard.hotkey("ctrl", "w")
            return True

        if intent_type == IntentType.CLOSE_OTHER_TABS:
            return self._close_other_tabs()

        if intent_type == IntentType.MINIMIZE:
            self.keyboard.hotkey("win", "down")
            return True

        if intent_type == IntentType.RESTORE:
            self.keyboard.hotkey("win", "up")
            return True

        if intent_type == IntentType.CLOSE_WINDOW:
            self.keyboard.hotkey("alt", "f4")
            return True

        if intent_type == IntentType.CLOSE_EVERYTHING:
            return self._close_everything()

        if intent_type == IntentType.WAIT:
            self.keyboard.wait()
            return True

        return False

    def _open_application(self, target: str | None) -> bool:
        if not target:
            return False

        application = target.lower().strip()

        if application in {"chrome", "google chrome", "browser"}:
            return self.chrome.open()

        if application in {
            "vscode",
            "vs code",
            "visual studio code",
            "visual studio",
            "vs",
        }:
            return self.vscode.open()

        if application in {"file explorer", "explorer"}:
            return self.explorer.open()

        return False

    def _close_application(self, target: str | None) -> bool:
        if not target:
            return False

        application = target.lower().strip()

        if application in {"chrome", "google chrome"}:
            return self.chrome.close()

        return False

    def _open_url(self, value: str | None) -> bool:
        if not value:
            return False

        return self.chrome.open_url(value)

    def _search(self, query: str | None) -> bool:
        if not query:
            return False

        return self.chrome.google_search(query)

    def _click(self) -> bool:
        self.mouse.click()
        return True

    def _type(self, value: str | None) -> bool:
        if value is None:
            return False

        self.keyboard.type_text(value)
        return True

    def _scroll(self, direction: str | None) -> bool:
        if direction == "up":
            self.mouse.scroll(5)
            return True

        if direction == "down":
            self.mouse.scroll(-5)
            return True

        return False

    def _move_cursor(
        self,
        direction: str | None,
        amount: float | None,
    ) -> bool:
        if direction not in {"up", "down", "left", "right"}:
            return False

        units = amount if amount is not None else 1
        pixels = round(units * 0.5 * self.PIXELS_PER_CM)

        dx = 0
        dy = 0

        if direction == "up":
            dy = -pixels
        elif direction == "down":
            dy = pixels
        elif direction == "left":
            dx = -pixels
        elif direction == "right":
            dx = pixels

        pyautogui.moveRel(dx, dy, duration=0.08)
        return True

    def _close_other_tabs(self) -> bool:
        # Chrome has no universal keyboard shortcut for
        # "Close other tabs", so use Chrome's tab context menu.
        # Right-click current tab and click the "Close other tabs"
        # menu item by image/UI position is not safe to guess.
        #
        # For now, report unsupported rather than closing the wrong tabs.
        print("Collin: Close other tabs requires Chrome UI observation.")
        return False

    def _close_everything(self) -> bool:
        # Safety rule: this command closes the active window only.
        # It never shuts down Windows.
        self.keyboard.hotkey("alt", "f4")
        return True


def main() -> None:
    executor = Executor()

    print("Executor: OK")

    print(
        "Search intent supported:",
        executor.execute(
            Intent(
                type=IntentType.SEARCH,
                value="Collin AI",
            )
        ),
    )


if __name__ == "__main__":
    main()
