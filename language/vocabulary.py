"""
Collin Language Vocabulary

Basic computer-control vocabulary for Collin V0.1.
"""

COMMAND_WORDS = {
    "open",
    "start",
    "launch",
    "close",
    "stop",
    "exit",
    "search",
    "find",
    "go",
    "visit",
    "click",
    "type",
    "write",
    "scroll",
    "copy",
    "paste",
    "cut",
    "save",
    "undo",
    "wait",
}

APPLICATIONS = {
    "chrome": "Chrome",
    "google chrome": "Chrome",
    "vscode": "VS Code",
    "vs code": "VS Code",
    "visual studio code": "VS Code",
    "explorer": "File Explorer",
    "file explorer": "File Explorer",
}

KEYWORDS = {
    "google",
    "website",
    "url",
    "page",
    "file",
    "folder",
    "up",
    "down",
    "left",
    "right",
}


def normalize_text(text: str) -> str:
    """Normalize user text for parsing."""

    if not isinstance(text, str):
        raise TypeError("text must be a string.")

    return " ".join(text.lower().strip().split())


def find_application(text: str) -> str | None:
    """Find a known application in text."""

    normalized = normalize_text(text)

    for name, application in APPLICATIONS.items():
        if name in normalized:
            return application

    return None


def main() -> None:
    """Safe vocabulary test."""

    print("Vocabulary: OK")
    print("Commands:", len(COMMAND_WORDS))
    print("Applications:", APPLICATIONS)

    print(
        "Found application:",
        find_application("Please open Google Chrome"),
    )


if __name__ == "__main__":
    main()
