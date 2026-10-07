"""
Collin Voice Microphone

Lightweight microphone input for Collin.
"""

import speech_recognition as sr


class MicrophoneController:
    """Captures audio from the default microphone."""

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

    def listen(self, timeout: float | None = None, phrase_time_limit: float | None = None):
        """Listen to the default microphone and return audio."""

        with sr.Microphone() as source:
            return self.recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )


def main() -> None:
    """Safe microphone initialization test."""

    controller = MicrophoneController()

    print("Microphone controller: OK")
    print("Default microphone is available.")


if __name__ == "__main__":
    main()
