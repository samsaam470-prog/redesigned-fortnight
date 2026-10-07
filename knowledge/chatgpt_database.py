import time
import pyautogui
import pyperclip
from pywinauto import Desktop

DATABASE_URL = "https://chatgpt.com/share/6abcdea0-8a04-83ee-8dc8-c4a3513b8e78"


class ChatGPTDatabaseUploader:

    INPUT_NAMES = (
        "ask anything",
        "message chatgpt",
        "message chatgpt...",
        "type here",
        "type a message",
        "send a message",
        "ask chatgpt",
        "prompt",
    )

    def __init__(self):
        self.url = DATABASE_URL

    def format_learning(self, session):
        lines = [
            "COLLIN LEARNED PROCEDURE",
            "",
            f"Instruction: {session.instruction or 'No instruction recorded.'}",
            "",
            "Learned events:",
        ]

        for index, event in enumerate(session.events, 1):
            lines.append(
                f"{index}. {event.get('type', 'unknown')}: {event}"
            )

        return "\n".join(lines)

    def open_database_chat(self):
        try:
            from chrome.controller import ChromeController

            chrome = ChromeController()
            chrome.open_url(self.url)
            time.sleep(4)
            return True

        except Exception as exc:
            print(f"COLLIN DATABASE OPEN ERROR: {exc}")
            return False

    def _text(self, control):
        try:
            info = control.element_info

            values = [
                control.window_text(),
                getattr(info, "name", ""),
                getattr(info, "automation_id", ""),
                getattr(info, "class_name", ""),
            ]

            return " ".join(
                str(x or "").strip().lower()
                for x in values
            )

        except Exception:
            return ""

    def find_input(self, timeout=20):
        deadline = time.time() + timeout

        while time.time() < deadline:
            try:
                windows = Desktop(
                    backend="uia"
                ).windows(
                    title_re=".*Chrome.*"
                )

                # Pass 1:
                # Look for known ChatGPT input names.
                for window in windows:
                    try:
                        controls = window.descendants()
                    except Exception:
                        continue

                    for control in controls:
                        text = self._text(control)

                        if any(
                            name in text
                            for name in self.INPUT_NAMES
                        ):
                            print(
                                "COLLIN DATABASE: Input found by label."
                            )
                            return control

                # Pass 2:
                # Look for an editable control.
                for window in windows:
                    try:
                        controls = window.descendants()
                    except Exception:
                        continue

                    edits = []

                    for control in controls:
                        try:
                            info = control.element_info
                            control_type = (
                                info.control_type or ""
                            ).lower()

                            if control_type == "edit":
                                edits.append(control)

                        except Exception:
                            continue

                    # Prefer the largest/most likely message editor.
                    if edits:
                        for control in edits:
                            text = self._text(control)

                            if any(
                                word in text
                                for word in (
                                    "chatgpt",
                                    "message",
                                    "ask",
                                    "prompt",
                                    "type",
                                )
                            ):
                                print(
                                    "COLLIN DATABASE: Input found by textbox."
                                )
                                return control

                        # Last UIA textbox fallback.
                        if len(edits) == 1:
                            print(
                                "COLLIN DATABASE: Single textbox found."
                            )
                            return edits[0]

            except Exception:
                pass

            time.sleep(0.5)

        return None

    def upload_text(self, text):
        if not text:
            print(
                "COLLIN DATABASE: Nothing to paste."
            )
            return False

        if not self.open_database_chat():
            return False

        print(
            "COLLIN DATABASE: Finding ChatGPT message box..."
        )

        box = self.find_input()

        if box is None:
            print(
                "COLLIN DATABASE: Could not find message box."
            )
            return False

        try:
            # Exactly one click.
            box.click_input()
            time.sleep(0.4)

            pyperclip.copy(text)

            pyautogui.hotkey(
                "ctrl",
                "v",
            )

            time.sleep(0.5)

            pyautogui.press(
                "enter"
            )

            print(
                "COLLIN DATABASE: Pasted learned procedure and pressed Enter."
            )

            return True

        except Exception as exc:
            print(
                f"COLLIN DATABASE: Paste failed: {exc}"
            )
            return False

    def upload(self, session):
        return self.upload_text(
            self.format_learning(session)
        )

    def upload_last_saved(self):
        try:
            from knowledge.database import KnowledgeDatabase

            database = KnowledgeDatabase()

            # Try common retrieval methods without changing
            # the database structure.
            procedure = None

            for method_name in (
                "get_latest_procedure",
                "latest_procedure",
                "get_latest",
            ):
                method = getattr(
                    database,
                    method_name,
                    None,
                )

                if callable(method):
                    try:
                        procedure = method()
                        if procedure:
                            break
                    except Exception:
                        pass

            if not procedure:
                print(
                    "COLLIN DATABASE: No latest procedure retrieval method available."
                )
                return False

            if isinstance(procedure, dict):
                lines = [
                    "COLLIN LEARNED PROCEDURE",
                    "",
                    str(procedure),
                ]
                text = "\n".join(lines)
            else:
                text = str(procedure)

            return self.upload_text(text)

        except Exception as exc:
            print(
                f"COLLIN DATABASE LAST PROCEDURE ERROR: {exc}"
            )
            return False
