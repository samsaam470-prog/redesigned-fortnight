"""
Collin Teaching Recorder

Records structured events during a teaching session.
"""

from datetime import datetime
from typing import Any

from core.logger import get_logger


class TeachingRecorder:
    """Records reusable teaching events."""

    def __init__(self) -> None:
        self.logger = get_logger("TeachingRecorder")
        self._recording = False
        self._events: list[dict[str, Any]] = []

    @property
    def recording(self) -> bool:
        """Return whether recording is active."""
        return self._recording

    @property
    def events(self) -> list[dict[str, Any]]:
        """Return recorded events."""
        return list(self._events)

    def start(self) -> None:
        """Start recording teaching events."""

        self._events.clear()
        self._recording = True
        self.logger.info("Teaching recorder started.")

    def stop(self) -> list[dict[str, Any]]:
        """Stop recording and return recorded events."""

        self._recording = False
        self.logger.info(
            "Teaching recorder stopped. Events: %d",
            len(self._events),
        )

        return self.events

    def record(
        self,
        action: str,
        target: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Record one structured teaching event."""

        if not self._recording:
            return

        event = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "action": action,
            "target": target,
            "details": details or {},
        }

        self._events.append(event)

        self.logger.debug(
            "Recorded teaching event: %s",
            event,
        )

    def clear(self) -> None:
        """Clear recorded events."""

        self._events.clear()


def main() -> None:
    """Safe recorder test."""

    recorder = TeachingRecorder()

    print("Teaching recorder: OK")

    recorder.start()

    recorder.record(
        action="open_application",
        target="Chrome",
    )

    recorder.record(
        action="click",
        target="Gemini",
        details={"description": "Gemini button"},
    )

    events = recorder.stop()

    print("Recorded events:", len(events))

    for event in events:
        print(event)


if __name__ == "__main__":
    main()
