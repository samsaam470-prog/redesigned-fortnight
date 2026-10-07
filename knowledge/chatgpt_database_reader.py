import re
import time
import webbrowser

from knowledge.collin_knowledge import CollinKnowledge


class ChatGPTDatabaseReader:
    DATABASE_URL = (
        "https://chatgpt.com/share/"
        "6abcdea0-8a04-83ee-8dc8-c4a3513b8e78"
    )

    def __init__(self):
        self.knowledge = CollinKnowledge()

    def open_database(self):
        webbrowser.open(self.DATABASE_URL)
        time.sleep(5)

    @staticmethod
    def _clean(text):
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _read_message_controls(self, window):
        """
        Read meaningful text controls from the ChatGPT UI.

        We deliberately ignore common Chrome/UI labels and
        collect longer conversational text.
        """
        controls = []

        try:
            controls = window.descendants()
        except Exception:
            return []

        messages = []
        seen = set()

        ignored = {
            "ask anything",
            "search",
            "new chat",
            "chatgpt",
            "copy",
            "edit",
            "more",
            "send",
            "stop generating",
            "share",
            "like",
            "dislike",
        }

        for control in controls:
            try:
                text = control.window_text()
            except Exception:
                continue

            text = self._clean(text)

            if not text:
                continue

            if text.lower() in ignored:
                continue

            # Ignore tiny UI fragments.
            if len(text) < 8:
                continue

            # Ignore obvious browser chrome.
            if text.startswith("http://"):
                continue

            if text.startswith("https://"):
                continue

            # Avoid duplicate UI nodes.
            if text in seen:
                continue

            seen.add(text)
            messages.append(text)

        return messages

    def read_conversation(self):
        try:
            from pywinauto import Desktop

            windows = Desktop(
                backend="uia"
            ).windows(
                title_re=".*Chrome.*"
            )

            if not windows:
                print(
                    "COLLIN DATABASE: Chrome window not found."
                )
                return ""

            # Prefer the largest Chrome window.
            window = max(
                windows,
                key=lambda item: len(
                    item.descendants()
                ),
            )

            messages = self._read_message_controls(
                window
            )

            if not messages:
                print(
                    "COLLIN DATABASE: no conversation "
                    "messages found."
                )
                return ""

            # Keep the conversation in the same order
            # returned by the accessibility tree.
            conversation = "\n".join(messages)

            return conversation

        except Exception as exc:
            print(
                f"COLLIN DATABASE: conversation read "
                f"error: {exc}"
            )
            return ""

    def check_for_changes(self):
        conversation = self.read_conversation()

        if not conversation:
            return False

        changed = self.knowledge.update(
            conversation
        )

        if changed:
            print(
                "COLLIN DATABASE: KNOWLEDGE CHANGED."
            )
            print(
                "COLLIN DATABASE: LOCAL CACHE UPDATED."
            )
        else:
            print(
                "COLLIN DATABASE: NO CHANGES."
            )

        return changed

    def sync(self):
        self.open_database()
        return self.check_for_changes()


if __name__ == "__main__":
    reader = ChatGPTDatabaseReader()
    reader.sync()
