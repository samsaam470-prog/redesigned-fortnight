"""
Collin Core Runtime

Central lightweight runtime/orchestrator for Collin V0.1.
"""

import time

from core.logger import get_logger
from core.state import CollinState, StateManager
from core.command_engine import CommandEngine


class CollinRuntime:
    """Main lightweight runtime for Collin."""

    def __init__(self) -> None:
        self.logger = get_logger("CollinRuntime")
        self.state = StateManager()
        self.command_engine = CommandEngine()
        self._running = False
        self._stop_requested = False

    @property
    def running(self) -> bool:
        """Return True when Collin is running."""
        return self._running

    def start(self) -> None:
        """Start Collin."""

        if self._running:
            self.logger.warning("Runtime is already running.")
            return

        self.logger.info("Collin starting...")

        self.state.set_state(CollinState.STARTING)
        self._stop_requested = False
        self._running = True
        self.state.set_state(CollinState.RUNNING)

        self.logger.info("Collin is running.")

    def stop(self) -> None:
        """Stop Collin gracefully."""

        if not self._running:
            self.state.set_state(CollinState.STOPPED)
            self.logger.info("Collin is already stopped.")
            return

        self.logger.info("Collin stopping...")

        self.state.set_state(CollinState.STOPPING)
        self._stop_requested = True
        self._running = False
        self.state.set_state(CollinState.STOPPED)

        self.logger.info("Collin stopped.")

    def pause(self) -> None:
        """Pause Collin."""

        if not self._running:
            self.logger.warning(
                "Cannot pause because Collin is not running."
            )
            return

        self.state.set_state(CollinState.PAUSED)
        self.logger.info("Collin paused.")

    def resume(self) -> None:
        """Resume Collin."""

        if not self._running:
            self.logger.warning(
                "Cannot resume because Collin is not running."
            )
            return

        self.state.set_state(CollinState.RUNNING)
        self.logger.info("Collin resumed.")

    def request_stop(self) -> None:
        """Request that the runtime loop stop."""

        self._stop_requested = True
        self.logger.info("Stop requested.")

    def process_command(self, command: str) -> bool:
        """Process a command through the command engine."""

        if not self._running:
            self.logger.warning(
                "Cannot process command because Collin is not running."
            )
            return False

        self.logger.info(
            "Processing command: %s",
            command,
        )

        result = self.command_engine.process(command)

        if result:
            self.logger.info("Command executed successfully.")
        else:
            self.logger.warning("Command was not executed.")

        return result

    def run_once(self) -> None:
        """Run one runtime cycle."""

        if not self._running:
            return

        if self._stop_requested:
            self.stop()
            return

    def run(self, interval: float = 0.1) -> None:
        """Run Collin's lightweight background loop."""

        if not self._running:
            self.start()

        self.logger.info("Runtime loop started.")

        try:
            while self._running and not self._stop_requested:
                self.run_once()
                time.sleep(interval)

        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received.")

        except Exception:
            self.state.set_state(CollinState.ERROR)
            self.logger.exception("Unexpected runtime error.")

        finally:
            if self._running:
                self.stop()

            self.logger.info("Runtime loop ended.")


def main() -> None:
    """Safe runtime test."""

    runtime = CollinRuntime()

    runtime.start()

    print("Collin runtime: OK")
    print("Running:", runtime.running)
    print(
        "Command result:",
        runtime.process_command("wait"),
    )

    runtime.stop()

    print("Final state:", runtime.state.state.value)


if __name__ == "__main__":
    main()
