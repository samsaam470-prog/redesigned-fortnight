"""
Collin Teaching Session Manager
Learns compact semantic UI descriptions instead of permanently storing screenshots.
"""

import time
import threading
from pathlib import Path

from core.logger import get_logger
from knowledge.database import KnowledgeDatabase


class TeachingSessionManager:

    def __init__(self):
        self.logger = get_logger("TeachingSession")
        self.database = KnowledgeDatabase()

        self.active = False
        self.started_at = None
        self.instruction = ""
        self.events = []
        self.last_context = None
        self.last_saved_procedure = None

        self.mouse_listener = None
        self._listener_lock = threading.Lock()

    def indicator(self, mode):
        try:
            import subprocess
            import sys

            subprocess.Popen(
                [
                    sys.executable,
                    "-m",
                    "teaching.status_indicator",
                    mode,
                ],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except Exception:
            self.logger.exception(
                "Could not show teaching indicator."
            )

    def start(self):
        if self.active:
            return False

        self.active = True
        self.started_at = time.time()
        self.instruction = ""
        self.events = []
        self.last_context = None
        self.last_saved_procedure = None

        self.indicator("learning")
        self._start_mouse_recording()

        self.logger.info("COLLIN — LEARNING")

        return True

    def _start_mouse_recording(self):
        try:
            from pynput import mouse

            def on_click(x, y, button, pressed):
                if not self.active or not pressed:
                    return

                self._record_mouse_click(
                    x,
                    y,
                    str(button),
                )

            self.mouse_listener = mouse.Listener(
                on_click=on_click
            )

            self.mouse_listener.daemon = True
            self.mouse_listener.start()

            self.logger.info(
                "Semantic mouse demonstration recording started."
            )

        except Exception:
            self.logger.exception(
                "Could not start mouse recording."
            )

    def _stop_mouse_recording(self):
        listener = self.mouse_listener
        self.mouse_listener = None

        if listener is not None:
            try:
                listener.stop()
            except Exception:
                pass

    def _record_mouse_click(self, x, y, button):
        """
        Record a compact semantic description of the clicked UI element.

        Permanent screenshots are NOT created.
        Coordinates are retained only as supporting/fallback information.
        """

        try:
            import pyautogui

            screen = pyautogui.size()

            target = self._describe_ui_target(x, y)

            event = {
                "type": "ui_action",
                "action": "click",
                "button": button,

                "target": target,

                # Coordinates are supporting information only.
                "fallback_position": {
                    "x": int(x),
                    "y": int(y),
                },

                "screen": {
                    "width": int(screen.width),
                    "height": int(screen.height),
                },

                "timestamp": time.time(),
            }

            with self._listener_lock:
                self.events.append(event)

            self.last_context = target

            self.logger.info(
                "Semantic UI click learned: %s",
                target,
            )

        except Exception:
            self.logger.exception(
                "Could not learn semantic UI click."
            )

    def _describe_ui_target(self, x, y):
        """
        Try Windows UI Automation first.

        Learns:
        - visible text
        - control type
        - class name
        - button/control shape
        - approximate size
        - color description
        - nearby controls
        - supporting position

        No screenshot is saved.
        """

        description = {
            "visible_text": "",
            "control_type": "",
            "class_name": "",
            "shape": "unknown",
            "color": "unknown",
            "size": "unknown",
            "nearby_text": [],
        }

        try:
            from pywinauto import Desktop

            element = Desktop(
                backend="uia"
            ).from_point(
                int(x),
                int(y),
            )

            if element is None:
                return description

            try:
                description["visible_text"] = (
                    element.window_text() or ""
                ).strip()
            except Exception:
                pass

            try:
                description["control_type"] = (
                    element.element_info.control_type or ""
                )
            except Exception:
                pass

            try:
                description["class_name"] = (
                    element.element_info.class_name or ""
                )
            except Exception:
                pass

            try:
                rect = element.rectangle()

                width = max(
                    1,
                    rect.right - rect.left,
                )

                height = max(
                    1,
                    rect.bottom - rect.top,
                )

                description["size"] = self._size_description(
                    width,
                    height,
                )

                description["shape"] = self._shape_description(
                    width,
                    height,
                )

            except Exception:
                pass

            # Try nearby UI elements.
            try:
                parent = element.parent()

                nearby = []

                for child in parent.children():
                    try:
                        text = (
                            child.window_text() or ""
                        ).strip()

                        if text:
                            nearby.append(text)

                    except Exception:
                        pass

                    if len(nearby) >= 6:
                        break

                description["nearby_text"] = nearby

            except Exception:
                pass

        except Exception:
            # UI Automation may not be available for every application.
            pass

        # Sample the screen only in memory.
        # Nothing is written to disk.
        try:
            screenshot = pyautogui.screenshot()

            description["color"] = (
                self._sample_color_description(
                    screenshot,
                    int(x),
                    int(y),
                )
            )

        except Exception:
            pass

        return description

    @staticmethod
    def _size_description(width, height):
        area = width * height

        if area < 5000:
            return "small"

        if area < 30000:
            return "medium"

        return "large"

    @staticmethod
    def _shape_description(width, height):
        ratio = width / max(1, height)

        if 0.85 <= ratio <= 1.15:
            return "approximately_square_or_round"

        if ratio > 2.5:
            return "wide_rectangle"

        if ratio > 1.25:
            return "horizontal_rectangle"

        if ratio < 0.4:
            return "tall_rectangle"

        return "rectangle"

    @staticmethod
    def _sample_color_description(image, x, y):
        """
        Gets an approximate color from a tiny in-memory region.
        """

        try:
            radius = 5

            left = max(0, x - radius)
            top = max(0, y - radius)
            right = min(image.width, x + radius + 1)
            bottom = min(image.height, y + radius + 1)

            crop = image.crop(
                (left, top, right, bottom)
            ).convert("RGB")

            pixels = list(crop.getdata())

            if not pixels:
                return "unknown"

            r = sum(p[0] for p in pixels) / len(pixels)
            g = sum(p[1] for p in pixels) / len(pixels)
            b = sum(p[2] for p in pixels) / len(pixels)

            brightness = (r + g + b) / 3

            if brightness < 60:
                return "very_dark"

            if brightness < 120:
                return "dark"

            if brightness < 190:
                return "medium"

            return "light"

        except Exception:
            return "unknown"

    def add_instruction(self, text):
        if not self.active:
            return False

        text = str(text).strip()

        if not text:
            return False

        self.instruction = text

        self.events.append(
            {
                "type": "instruction",
                "text": text,
                "timestamp": time.time(),
            }
        )

        self.logger.info(
            "Teaching instruction recorded: %s",
            text,
        )

        return True

    def observe(self):
        """
        Capture only lightweight observation metadata.

        No permanent screenshot is saved.
        """

        if not self.active:
            return False

        try:
            import pyautogui

            position = pyautogui.position()
            screen = pyautogui.size()

            observation = {
                "cursor": {
                    "x": position.x,
                    "y": position.y,
                },
                "screen": {
                    "width": screen.width,
                    "height": screen.height,
                },
                "timestamp": time.time(),
            }

            self.events.append(
                {
                    "type": "observation",
                    "data": observation,
                }
            )

            self.last_context = observation

            self.logger.info(
                "Teaching observation recorded."
            )

            return True

        except Exception:
            self.logger.exception(
                "Could not capture observation."
            )
            return False

    def write_here(self):
        if not self.active:
            return False

        if not self.observe():
            return False

        self.events.append(
            {
                "type": "write_here",
                "context": self.last_context,
                "timestamp": time.time(),
            }
        )

        self.logger.info(
            "COLLIN — WRITE HERE location learned."
        )

        self.indicator("observing")

        return True

    def record_step(
        self,
        action,
        target=None,
        details=None,
    ):
        if not self.active:
            return False

        self.events.append(
            {
                "type": "step",
                "action": action,
                "target": target,
                "details": details or {},
                "timestamp": time.time(),
            }
        )

        return True

    def finish(
        self,
        name="learned_procedure",
    ):
        if not self.active:
            return False

        self._stop_mouse_recording()

        procedure = {
            "name": name,
            "instruction": self.instruction,
            "events": list(self.events),
            "last_context": self.last_context,
            "started_at": self.started_at,
            "finished_at": time.time(),
        }

        try:
            self.database.save_procedure(
                procedure,
                status="learned",
            )

        except Exception:
            self.logger.exception(
                "Could not save learned procedure."
            )
            return False

        self.active = False
        self.last_saved_procedure = procedure

        self.indicator("learned")

        self.logger.info(
            "COLLIN — LEARNED: %s",
            name,
        )

        return procedure
