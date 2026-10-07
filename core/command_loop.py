"""
Collin Command Loop

Provides a lightweight interactive command loop for Collin V0.1.
"""

from core.logger import get_logger
from wake.manager import WakeManager


class CommandLoop:
    """Handles commands after Collin is activated."""

    def __init__(self, wake_manager: WakeManager | None = None) -> None:
        self.logger = get_logger("CommandLoop")
        self.wake_manager = wake_manager or WakeManager()
        self._running = False

    def start(self) -> None:
        """Start the interactive command loop."""

        self._running = True
        self.wake_manager.start()

        print("Collin command loop started.")
        print("Type 'Hi Colin' to wake Collin.")
        print("Type 'exit' to stop.")

        while self._running:
            try:
                text = input("You: ").strip()

                if not text:
                    continue

                if text.lower() == "exit":
                    self.stop()
                    break

                if not self.wake_manager.runtime.running:
                    if self.wake_manager.process_text(text):
                        print("Collin: Awake.")
                    else:
                        print("Collin: Sleeping.")
                    continue

                if text.lower() in {
                    "stop colin",
                    "sleep",
                    "go to sleep",
                }:
                    self.wake_manager.runtime.stop()
                    print("Collin: Sleeping.")
                    continue

                result = self.wake_manager.runtime.process_command(text)

                if result:
                    print("Collin: Done.")
                else:
                    print("Collin: I don't know how to do that yet.")

            except KeyboardInterrupt:
                self.stop()
                break

            except EOFError:
                self.stop()
                break

            except Exception:
                self.logger.exception("Command loop error.")
                print("Collin: An error occurred.")

    def stop(self) -> None:
        """Stop the command loop."""

        if not self._running:
            return

        self._running = False

        if self.wake_manager.runtime.running:
            self.wake_manager.runtime.stop()

        self.wake_manager.stop()

        print("Collin command loop stopped.")


def main() -> None:
    """Start Collin's text command loop."""

    loop = CommandLoop()
    loop.start()


if __name__ == "__main__":
    main()
