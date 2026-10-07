"""
Collin Procedure Builder

Builds reusable procedures from teaching events.
"""

from typing import Any

from core.logger import get_logger


class ProcedureBuilder:
    """Builds reusable procedures for Collin."""

    def __init__(self) -> None:
        self.logger = get_logger("ProcedureBuilder")

    def build(
        self,
        name: str,
        description: str,
        events: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Build a reusable procedure.

        The procedure stores semantic actions rather than
        relying on fixed screen coordinates.
        """

        if not name.strip():
            raise ValueError("Procedure name cannot be empty.")

        if not isinstance(events, list):
            raise TypeError("events must be a list.")

        procedure = {
            "name": name.strip(),
            "description": description.strip(),
            "version": 1,
            "steps": list(events),
        }

        self.logger.info(
            "Procedure built: %s (%d steps)",
            procedure["name"],
            len(procedure["steps"]),
        )

        return procedure

    def add_step(
        self,
        procedure: dict[str, Any],
        action: str,
        target: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Add a semantic step to an existing procedure."""

        step = {
            "action": action,
            "target": target,
            "details": details or {},
        }

        procedure.setdefault("steps", []).append(step)

        return procedure

    def validate(
        self,
        procedure: dict[str, Any],
    ) -> bool:
        """Perform basic procedure validation."""

        required = {
            "name",
            "description",
            "version",
            "steps",
        }

        if not required.issubset(procedure):
            return False

        if not isinstance(procedure["steps"], list):
            return False

        return True


def main() -> None:
    """Safe procedure builder test."""

    builder = ProcedureBuilder()

    events = [
        {
            "action": "open_application",
            "target": "Chrome",
            "details": {},
        },
        {
            "action": "click",
            "target": "Gemini",
            "details": {
                "description": "Gemini button",
            },
        },
    ]

    procedure = builder.build(
        name="open_gemini",
        description="Open Gemini through Chrome.",
        events=events,
    )

    print("Procedure builder: OK")
    print("Procedure valid:", builder.validate(procedure))
    print("Procedure:", procedure)


if __name__ == "__main__":
    main()
