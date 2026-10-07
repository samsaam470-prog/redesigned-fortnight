"""
Collin Teaching Mode

Controls Collin's teaching/learning state.
"""

from core.logger import get_logger
from core.state import CollinState, StateManager


class TeachingMode:
    """Manages Collin's teaching mode."""

    def __init__(self, state_manager: StateManager | None = None) -> None:
        self.logger = get_logger("TeachingMode")
        self.state_manager = state_manager or StateManager()
        self._active = False

    @property
    def active(self) -> bool:
        """Return whether teaching mode is active."""
        return self._active

    def start(self) -> None:
        """Start teaching mode."""

        if self._active:
            self.logger.warning("Teaching mode is already active.")
            return

        self._active = True
        self.state_manager.set_state(CollinState.TEACHING)
        self.logger.info("Teaching mode started.")

    def stop(self) -> None:
        """Stop teaching mode."""

        if not self._active:
            return

        self._active = False
        self.state_manager.set_state(CollinState.RUNNING)
        self.logger.info("Teaching mode stopped.")

    def toggle(self) -> bool:
        """Toggle teaching mode and return its new state."""

        if self._active:
            self.stop()
        else:
            self.start()

        return self._active


def main() -> None:
    """Safe teaching mode test."""

    teaching = TeachingMode()

    print("Teaching mode: OK")
    print("Initial active:", teaching.active)

    teaching.start()
    print("After start:", teaching.active)
    print("State:", teaching.state_manager.state.value)

    teaching.stop()
    print("After stop:", teaching.active)
    print("State:", teaching.state_manager.state.value)


if __name__ == "__main__":
    main()
