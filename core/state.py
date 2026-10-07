"""
Collin Core State
Defines the runtime states used by Collin.
"""

from enum import Enum


class CollinState(str, Enum):
    """Main runtime states for Collin."""

    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    TEACHING = "teaching"
    EXECUTING = "executing"
    ERROR = "error"
    STOPPING = "stopping"


class StateManager:
    """Lightweight manager for Collin's current state."""

    def __init__(self) -> None:
        self._state = CollinState.STOPPED

    @property
    def state(self) -> CollinState:
        """Return the current state."""
        return self._state

    def set_state(self, state: CollinState) -> None:
        """Change the current state."""

        if not isinstance(state, CollinState):
            raise ValueError(
                "state must be an instance of CollinState."
            )

        self._state = state

    def is_state(self, state: CollinState) -> bool:
        """Check whether Collin is in a specific state."""
        return self._state == state

    def __str__(self) -> str:
        return self._state.value


if __name__ == "__main__":
    manager = StateManager()

    print("Initial state:", manager.state.value)

    manager.set_state(CollinState.STARTING)
    print("Changed state:", manager.state.value)

    manager.set_state(CollinState.RUNNING)
    print("Changed state:", manager.state.value)
