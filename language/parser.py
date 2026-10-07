"""
Collin Language Parser
"""

import re

from language.intent import Intent, IntentType
from language.vocabulary import find_application, normalize_text


NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}


class CommandParser:
    """Parses basic English computer commands."""

    def parse(self, text: str) -> Intent:
        normalized = normalize_text(text)

        if not normalized:
            return Intent(IntentType.UNKNOWN)

        # Paste the procedure learned in the previous learning session.
        if normalized in {
            "paste here what you learned",
            "paste here what you learned in the previous session",
            "paste what you learned here",
            "paste what you learned from the previous session",
            "paste previous learning",
            "paste previous session learning",
            "write here what you learned",
            "write here what you learned in the previous session",
            "in the previous learning session you learned this now paste here in text form",
        }:
            return Intent(IntentType.PASTE_LEARNED_PROCEDURE)

        # Simple keyboard commands
        if normalized in {"copy", "copy it"}:
            return Intent(IntentType.COPY)

        if normalized in {"paste", "paste it"}:
            return Intent(IntentType.PASTE)

        if normalized in {"cut", "cut it"}:
            return Intent(IntentType.CUT)

        if normalized in {"save", "save it"}:
            return Intent(IntentType.SAVE)

        if normalized in {"undo", "undo it"}:
            return Intent(IntentType.UNDO)

        if normalized in {"select all", "select everything"}:
            return Intent(IntentType.SELECT_ALL)

        if normalized in {"send", "send it", "press enter"}:
            return Intent(IntentType.SEND)

        # Chrome tab commands
        if normalized in {"open new tab", "new tab", "open a new tab"}:
            return Intent(IntentType.OPEN_NEW_TAB)

        if normalized in {
            "close this tab",
            "close tab",
            "close current tab",
        }:
            return Intent(IntentType.CLOSE_TAB)

        if normalized in {
            "close all other tabs",
            "close all other tabs except this one",
            "close other tabs",
        }:
            return Intent(IntentType.CLOSE_OTHER_TABS)

        # Window commands
        if normalized in {"minimize chrome", "minimize window"}:
            return Intent(IntentType.MINIMIZE)

        if normalized in {
            "restore down",
            "restore window",
            "restore",
        }:
            return Intent(IntentType.RESTORE)

        if normalized in {"close", "close window", "close this window"}:
            return Intent(IntentType.CLOSE_WINDOW)

        if normalized in {"close everything", "close all windows"}:
            return Intent(IntentType.CLOSE_EVERYTHING)

        # ChatGPT always opens ChatGPT directly.
        if normalized in {
            "chatgpt",
            "open chatgpt",
            "search chatgpt",
            "open chat gpt",
            "search chat gpt",
        }:
            return Intent(
                IntentType.OPEN_URL,
                target="https://chatgpt.com",
            )

        # Applications
        application = find_application(normalized)

        if normalized.startswith(("open ", "start ", "launch ")):
            if application:
                return Intent(
                    IntentType.OPEN_APPLICATION,
                    target=application,
                )

            url = self._extract_url(normalized)
            if url:
                return Intent(
                    IntentType.OPEN_URL,
                    target=url,
                )

        # Explicit VS aliases.
        if normalized in {
            "open vs",
            "open vs code",
            "open visual studio",
        }:
            return Intent(
                IntentType.OPEN_APPLICATION,
                target="vscode",
            )

        if normalized in {"open browser", "open chrome"}:
            return Intent(
                IntentType.OPEN_APPLICATION,
                target="chrome",
            )

        if normalized.startswith(("close ", "stop ", "exit ")):
            if application:
                return Intent(
                    IntentType.CLOSE_APPLICATION,
                    target=application,
                )

        # Search Google
        if normalized.startswith(("search ", "find ")):
            query = self._extract_search_query(normalized)

            return Intent(
                IntentType.SEARCH,
                target="Google",
                value=query,
            )

        if normalized.startswith("search google "):
            query = re.sub(
                r"^search\s+google\s+",
                "",
                normalized,
                count=1,
            ).strip()

            return Intent(
                IntentType.SEARCH,
                target="Google",
                value=query,
            )

        if normalized.startswith(("go to ", "visit ")):
            target = normalized.split(" ", 2)[-1]

            return Intent(
                IntentType.OPEN_URL,
                target=target,
            )

        # Mouse click
        if normalized in {"click it", "click"}:
            return Intent(IntentType.CLICK)

        if normalized.startswith("click "):
            return Intent(
                IntentType.CLICK,
                target=normalized[6:].strip(),
            )

        # Cursor movement: one unit = 0.5 cm.
        move_match = re.match(
            r"^move cursor\s+(up|down|left|right)(?:\s+(.+))?$",
            normalized,
        )

        if move_match:
            direction = move_match.group(1)
            amount_text = move_match.group(2) or "1"

            try:
                amount = float(amount_text)
            except ValueError:
                amount = NUMBER_WORDS.get(amount_text, 1)

            return Intent(
                IntentType.MOVE_CURSOR,
                direction=direction,
                amount=amount,
            )

        # Type / write
        if normalized.startswith(("type ", "write ")):
            value = re.sub(
                r"^(type|write)\s+",
                "",
                normalized,
                count=1,
            )

            return Intent(
                IntentType.TYPE,
                value=value,
            )

        # Scroll
        if normalized.startswith("scroll"):
            direction = "down"

            if "up" in normalized:
                direction = "up"

            return Intent(
                IntentType.SCROLL,
                direction=direction,
            )

        # Wait
        if normalized.startswith("wait"):
            value = normalized.replace(
                "wait",
                "",
                1,
            ).strip()

            return Intent(
                IntentType.WAIT,
                value=value or "1",
            )

        return Intent(IntentType.UNKNOWN)

    @staticmethod
    def _extract_url(text: str) -> str | None:
        match = re.search(r"https?://\S+", text)

        if match:
            return match.group(0)

        return None

    @staticmethod
    def _extract_search_query(text: str) -> str:
        query = re.sub(
            r"^(search|find)\s+",
            "",
            text,
            count=1,
        )

        query = re.sub(
            r"^google\s+for\s+",
            "",
            query,
            count=1,
        )

        query = re.sub(
            r"^google\s+",
            "",
            query,
            count=1,
        )

        query = re.sub(
            r"^for\s+",
            "",
            query,
            count=1,
        )

        return query.strip()


def main() -> None:
    parser = CommandParser()

    tests = [
        "Open Chrome",
        "Open browser",
        "Open VS",
        "Open VS Code",
        "Open Visual Studio",
        "Open ChatGPT",
        "Search ChatGPT",
        "ChatGPT",
        "Search Google for cats",
        "Click it",
        "Type hello world",
        "Write hello",
        "Scroll down",
        "Copy it",
        "Paste it",
        "Select all",
        "Send",
        "Undo",
        "Save",
        "Open new tab",
        "Close this tab",
        "Close all other tabs",
        "Move cursor up",
        "Move cursor up 3",
        "Move cursor down three",
        "Move cursor left 2",
        "Move cursor right",
        "Minimize Chrome",
        "Restore down",
        "Close",
        "Close everything",
    ]

    print("Command parser: OK")

    for command in tests:
        intent = parser.parse(command)
        print(f"{command!r} -> {intent}")


if __name__ == "__main__":
    main()
