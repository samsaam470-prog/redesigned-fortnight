"""
Collin Wake Phrase Resolver

One semantic wake system for:
- voice transcription
- typed text
- Gemini Live captions
- other visible text sources

Collin/Colin/Callin/Calling are treated as name variants.
"""

import re


NAME_VARIANTS = {
    "colin",
    "collin",
    "callin",
    "calling",
}

GREETING_VARIANTS = {
    "hi",
    "hey",
    "hello",
    "high",
    "hai",
    "my",
}

WAKE_ACTIONS = {
    "wake",
    "wakeup",
    "wake up",
    "awake",
    "get up",
}


def normalize_text(text: str) -> str:
    """Normalize text while preserving word boundaries."""
    if not isinstance(text, str):
        return ""

    text = text.lower()

    text = text.replace("’", "'")

    # Remove punctuation but preserve spaces.
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Collapse whitespace.
    return " ".join(text.split())


def contains_name_variant(text: str) -> bool:
    words = normalize_text(text).split()

    return any(
        word in NAME_VARIANTS
        for word in words
    )


def is_wake_phrase(text: str) -> bool:
    """
    Return True when text semantically calls Collin.

    Examples:
        Hi Colin
        Hey Colin
        Hello Collin
        Wake up Colin
        Colin wake up
        Hi Calling
        Hi Callin
        Calling
        Callin
        Colin
        Collin
    """

    normalized = normalize_text(text)

    if not normalized:
        return False

    words = normalized.split()

    # Direct name call:
    # "Colin"
    # "Collin"
    # "Calling"
    # "Callin"
    if len(words) == 1:
        return words[0] in NAME_VARIANTS

    # Greeting + name:
    # "Hi Colin"
    # "Hey Collin"
    # "Hello Calling"
    if len(words) == 2:
        if (
            words[0] in GREETING_VARIANTS
            and words[1] in NAME_VARIANTS
        ):
            return True

        # Name + wake instruction:
        # "Colin wake"
        # "Colin wake up"
        if (
            words[0] in NAME_VARIANTS
            and words[1] in {"wake", "awake"}
        ):
            return True

    # "Colin wake up"
    if (
        len(words) == 3
        and words[0] in NAME_VARIANTS
        and words[1] == "wake"
        and words[2] == "up"
    ):
        return True

    # "Wake up Colin"
    if (
        len(words) == 3
        and words[0] == "wake"
        and words[1] == "up"
        and words[2] in NAME_VARIANTS
    ):
        return True

    # "Hey Colin wake up"
    if (
        len(words) == 4
        and words[0] in GREETING_VARIANTS
        and words[1] in NAME_VARIANTS
        and words[2] == "wake"
        and words[3] == "up"
    ):
        return True

    # Caption text may contain other words:
    #
    # "Hey Colin, wake up"
    # "Okay Colin wake up"
    # "Hi Colin can you listen"
    #
    # For caption detection, a name variant plus a clear
    # greeting/wake signal is enough.
    has_name = contains_name_variant(normalized)

    if not has_name:
        return False

    if any(greeting in words for greeting in GREETING_VARIANTS):
        return True

    if "wake" in words and "up" in words:
        return True

    return False


def is_name_only(text: str) -> bool:
    """Detect a direct name call."""
    normalized = normalize_text(text)
    return normalized in NAME_VARIANTS


if __name__ == "__main__":
    tests = [
        "Hi Colin",
        "Hey Colin",
        "Hello Colin",
        "Hi Collin",
        "Hi Callin",
        "Hi Calling",
        "Calling",
        "Callin",
        "Colin",
        "Collin",
        "Colin wake",
        "Colin wake up",
        "Collin wake up",
        "Wake up Colin",
        "Wake up Collin",
        "Hey Colin wake up",
        "Hi Colin can you listen",
        "Okay Colin wake up",
        "open chrome",
        "hello",
    ]

    print("Collin Wake Resolver")
    print("====================")

    for text in tests:
        print(
            f"{text!r} -> "
            f"{is_wake_phrase(text)}"
        )
