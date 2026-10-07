import time
import threading

from core.runtime import CollinRuntime
from wake.activation import CollinActivation
from wake.typed_listener import TypedActivationListener
from voice.speech import SpeechRecognizer


class CollinMain:

    def __init__(self):
        self.runtime = CollinRuntime()
        self.activation = CollinActivation(
            runtime=self.runtime
        )

        self.voice = None
        self.typed = None
        self.running = False
        self.voice_thread = None

    def log(self, message):
        print(f"[COLLIN] {message}")

    # ONE INPUT ROUTE FOR EVERYTHING
    def process_text(self, text, source="unknown"):
        if not isinstance(text, str):
            return

        text = " ".join(
            text.strip().split()
        )

        if not text:
            return

        self.log(f"{source}: {text}")

        # Voice, typing and future Gemini captions
        # all enter the same activation controller.
        result = self.activation.process_text(text)

        if result is True:
            return

        # Sleeping = ignore normal commands.
        if not self.activation.awake:
            return

        # Learning mode owns its input.
        if self.activation.learning:
            return

        # Normal computer command.
        try:
            result = self.runtime.process_command(text)

            if result is False:
                self.log(
                    f"Command not understood: {text}"
                )

        except Exception as exc:
            self.log(
                f"Command error: {exc}"
            )

    # GLOBAL TYPING
    def start_typed_listener(self):
        def callback(text):
            self.process_text(
                text,
                "typing"
            )

        self.typed = TypedActivationListener(
            callback=callback
        )

        self.typed.start()

        self.log(
            "Global typing listener started."
        )

    # VOICE
    def start_voice(self):
        try:
            self.voice = SpeechRecognizer()

        except Exception as exc:
            self.log(
                f"Voice initialization failed: {exc}"
            )
            return

        def voice_loop():
            self.log(
                "Voice listener started."
            )

            while self.running:
                try:
                    text = self.voice.recognize()

                    if text:
                        self.process_text(
                            text,
                            "voice"
                        )

                except Exception as exc:
                    self.log(
                        f"Voice error: {exc}"
                    )
                    time.sleep(0.5)

        self.voice_thread = threading.Thread(
            target=voice_loop,
            daemon=True,
            name="CollinVoice"
        )

        self.voice_thread.start()

    def start(self):
        if self.running:
            return

        self.running = True

        self.log(
            "Starting Collin..."
        )

        # Start the actual command runtime.
        try:
            self.runtime.start()
            self.log(
                "Collin command runtime started."
            )
        except Exception as exc:
            self.log(
                f"Runtime start error: {exc}"
            )

        # Start asleep.
        self.activation.sleep()

        # Both input systems start.
        self.start_typed_listener()
        self.start_voice()

        self.log(
            "Collin is running."
        )

        try:
            while self.running:
                time.sleep(1)

        except KeyboardInterrupt:
            self.log(
                "Stopping Collin."
            )

        finally:
            self.stop()

    def stop(self):
        if not self.running:
            return

        self.running = False

        if self.typed:
            try:
                self.typed.stop()
            except Exception:
                pass

        try:
            self.runtime.stop()
        except Exception:
            pass

        self.log(
            "Collin stopped."
        )


def main():
    CollinMain().start()


if __name__ == "__main__":
    main()
