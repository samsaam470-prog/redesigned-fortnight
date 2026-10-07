"""
Collin Command Engine

Connects English commands to the parser and execution layer.
"""

from language.parser import CommandParser
from execution.executor import Executor


class CommandEngine:
    """Processes a text command and executes the resulting intent."""

    def __init__(self) -> None:
        self.parser = CommandParser()
        self.executor = Executor()

    def process(self, command: str) -> bool:
        """Parse and execute a command."""

        if not isinstance(command, str):
            raise TypeError("command must be a string.")

        intent = self.parser.parse(command)

        if intent.type.value == "unknown":
            return False

        return self.executor.execute(intent)


def main() -> None:
    """Safe command engine test."""

    engine = CommandEngine()

    result = engine.process("wait")

    print("Command engine: OK")
    print("Test result:", result)


if __name__ == "__main__":
    main()
