"""
Collin Wake Manager

Connects the wake listener to the Collin runtime.
"""

from core.logger import get_logger
from core.runtime import CollinRuntime
from wake.listener import WakeListener


class WakeManager:
    """Manages wake detection for Collin."""

    def __init__(self, runtime: CollinRuntime | None = None) -> None:
        self.logger = get_logger("WakeManager")
        self.runtime = runtime or CollinRuntime()
        self.listener = WakeListener()

    def start(self) -> None:
        """Start the wake listener."""

        self.listener.start()
        self.logger.info("Wake manager started.")

    def stop(self) -> None:
        """Stop the wake listener."""

        self.listener.stop()
        self.logger.info("Wake manager stopped.")

    def process_text(self, text: str) -> bool:
        """
        Process recognized text.

        If the wake phrase is detected, start Collin.
        """

        if not self.listener.process_text(text):
            return False

        if not self.runtime.running:
            self.runtime.start()

        self.logger.info("Collin activated by wake phrase.")

        return True


def main() -> None:
    """Safe wake manager test."""

    manager = WakeManager()

    manager.start()

    print("Wake manager: OK")
    print(
        "Before wake:",
        manager.runtime.running,
    )

    detected = manager.process_text("hello there")

    print(
        "Normal phrase detected:",
        detected,
    )

    detected = manager.process_text("Hi Colin")

    print(
        "Wake phrase detected:",
        detected,
    )

    print(
        "After wake:",
        manager.runtime.running,
    )

    manager.runtime.stop()
    manager.stop()


if __name__ == "__main__":
    main()
