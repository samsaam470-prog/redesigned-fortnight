"""
Collin Voice Speech

Lightweight speech-to-text layer for Collin.
"""

import speech_recognition as sr

from voice.microphone import MicrophoneController


class SpeechRecognizer:
    """Converts microphone audio into text."""

    def __init__(self) -> None:
        self.microphone = MicrophoneController()
        self.recognizer = self.microphone.recognizer

    def recognize(
        self,
        timeout: float | None = None,
        phrase_time_limit: float | None = None,
    ) -> str | None:
        """Listen and convert speech to text."""

        try:
            audio = self.microphone.listen(
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )

            text = self.recognizer.recognize_google(audio)

            return text.strip()

        except sr.WaitTimeoutError:
            return None

        except sr.UnknownValueError:
            return None

        except sr.RequestError:
            return None


def main() -> None:
    """Test speech recognition."""

    speech = SpeechRecognizer()

    print("Speech recognizer: OK")
    print("Speech-to-text layer is ready.")
    print("Say something after the prompt.")
    print("Say 'test' or any short English phrase.")

    text = speech.recognize(
        timeout=10,
        phrase_time_limit=5,
    )

    if text:
        print("Recognized:", text)
    else:
        print("No speech recognized.")


if __name__ == "__main__":
    main()
