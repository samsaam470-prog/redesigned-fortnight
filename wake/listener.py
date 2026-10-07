"""
Collin Wake Listener

Lightweight tolerant wake-word listener.
"""

import re
import time

from core.logger import get_logger


class WakeListener:
    """Detects natural speech variations of 'Hi Colin'."""

    WAKE_PHRASE = "hi colin"

    def __init__(self) -> None:
        self.logger = get_logger("WakeListener")
        self._listening = False

    @property
    def listening(self) -> bool:
        return self._listening

    def start(self) -> None:
        if self._listening:
            return

        self._listening = True

        self.logger.info(
            "Wake listener started. Wake phrase: '%s'",
            self.WAKE_PHRASE,
        )

    def stop(self) -> None:
        self._listening = False
        self.logger.info("Wake listener stopped.")

    @staticmethod
    def _clean(text: str) -> str:
        """Normalize speech-recognition output."""

        text = text.lower().strip()

        # Remove punctuation.
        text = re.sub(r"[^a-z\s]", " ", text)

        # Join spaced letters such as:
        # c o l i n -> colin
        words = text.split()
        rebuilt = []

        i = 0
        while i < len(words):
            if (
                i + 3 < len(words)
                and all(len(word) == 1 for word in words[i:i + 4])
            ):
                rebuilt.append("".join(words[i:i + 4]))
                i += 4
            else:
                rebuilt.append(words[i])
                i += 1

        return " ".join(rebuilt)

    def check_phrase(self, text: str) -> bool:
        """Return True when speech resembles 'Hi Colin'."""

        if not isinstance(text, str):
            return False

        normalized = self._clean(text)

        words = normalized.split()

        if not words:
            return False

        # Direct match.
        if "hi colin" in normalized:
            return True

        # Common speech-recognition variants.
        greeting_words = {
            "hi",
            "hey",
            "hello",
            "high",
            "my",
            "hai",
        }

        colin_words = {
            "colin",
            "calling",
            "callin",
            "colin.",
            "colin!",
            "colin?",
        }

        for index, word in enumerate(words):
            if word not in greeting_words:
                continue

            following = words[index + 1:index + 3]

            if any(item in colin_words for item in following):
                return True

        # Handle shortened/spaced recognition:
        # "hi c o l i" / "hi c o l"
        if words and words[0] in greeting_words:
            tail = "".join(words[1:])

            if tail.startswith(("colin", "coli", "col")):
                return True

        return False

    def process_text(self, text: str) -> bool:
        if not self._listening:
            return False

        if self.check_phrase(text):
            self.logger.info(
                "Wake phrase detected: %s",
                text,
            )
            return True

        return False

    def wait(self, seconds: float = 0.1) -> None:
        time.sleep(seconds)


def main() -> None:
    listener = WakeListener()

    tests = [
        "hi colin",
        "hi calling",
        "my calling",
        "high Colin",
        "hi c o l i",
        "hi c o l",
        "hello colin",
        "hello",
        "open chrome",
    ]

    listener.start()

    print("Wake listener test")
    print("==================")

    for text in tests:
        result = listener.process_text(text)
        print(f"{text!r} -> {result}")

    listener.stop()


if __name__ == "__main__":
    main()
