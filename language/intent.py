"""
Collin Intent Definitions
"""
from dataclasses import dataclass
from enum import Enum


class IntentType(Enum):
    OPEN_APPLICATION = "open_application"
    CLOSE_APPLICATION = "close_application"
    OPEN_URL = "open_url"
    SEARCH = "search"
    CLICK = "click"
    TYPE = "type"
    SCROLL = "scroll"
    KEYBOARD = "keyboard"
    COPY = "copy"
    PASTE = "paste"
    CUT = "cut"
    SAVE = "save"
    UNDO = "undo"
    WAIT = "wait"
    SELECT_ALL = "select_all"
    SEND = "send"
    MOVE_CURSOR = "move_cursor"
    OPEN_NEW_TAB = "open_new_tab"
    CLOSE_TAB = "close_tab"
    CLOSE_OTHER_TABS = "close_other_tabs"
    MINIMIZE = "minimize"
    RESTORE = "restore"
    CLOSE_WINDOW = "close_window"
    CLOSE_EVERYTHING = "close_everything"
    PASTE_LEARNED_PROCEDURE = "paste_learned_procedure"
    UNKNOWN = "unknown"


@dataclass
class Intent:
    type: IntentType
    target: str | None = None
    value: str | None = None
    direction: str | None = None
    amount: float | None = None
