"""
Collin Gemini Caption Teaching

Lightweight screen/cursor teaching system for Gemini Live.
"""

import json
import time
from pathlib import Path

from computer.mouse import MouseController
from computer.screen import ScreenController
from knowledge.database import KnowledgeDatabase


class GeminiCaptionTeacher:
    """Learns where Gemini Live captions appear."""

    PROCEDURE_NAME = "gemini_live_captions"

    def __init__(self):
        self.mouse = MouseController()
        self.screen = ScreenController()
        self.database = KnowledgeDatabase()

    def observe(self):
        """Capture current screen and cursor position."""

        position = self.mouse.position()
        screenshot = self.screen.save_screenshot(
            folder="teaching"
        )

        observation = {
            "cursor": {
                "x": position[0],
                "y": position[1],
            },
            "screen": {
                "width": self.screen.size()[0],
                "height": self.screen.size()[1],
            },
            "screenshot": str(screenshot),
            "timestamp": time.time(),
        }

        return observation

    def learn_this(self):
        """Learn the area currently pointed at."""

        observation = self.observe()

        procedure = {
            "name": self.PROCEDURE_NAME,
            "description": (
                "Gemini Live caption area learned "
                "from user demonstration."
            ),
            "version": 1,
            "status": "learned",
            "target": "gemini_live_caption_area",
            "observation": observation,
        }

        self.database.save_procedure(
            name=self.PROCEDURE_NAME,
            description=procedure["description"],
            data=procedure,
            status="learned",
            version=1,
        )

        return procedure

    def see_this(self):
        """Observe the current screen without saving."""

        return self.observe()


def main():
    teacher = GeminiCaptionTeacher()

    print("Gemini Caption Teaching: OK")
    print("==========================")

    observation = teacher.see_this()

    print(
        "Screen:",
        observation["screen"]["width"],
        "x",
        observation["screen"]["height"],
    )

    print(
        "Cursor:",
        observation["cursor"]["x"],
        observation["cursor"]["y"],
    )

    print(
        "Screenshot:",
        observation["screenshot"],
    )

    print()
    print("Teaching commands available:")
    print("- Learn this")
    print("- See this")


if __name__ == "__main__":
    main()

