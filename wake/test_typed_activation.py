from wake.resolver import is_wake_phrase


tests = {
    "Hi Colin": True,
    "Hey Colin": True,
    "Hello Colin": True,
    "Hi Collin": True,
    "Hi Calling": True,
    "Hi Callin": True,
    "Calling": True,
    "Callin": True,
    "Colin": True,
    "Collin": True,
    "Colin wake": True,
    "Colin wake up": True,
    "Collin wake up": True,
    "Wake up Colin": True,
    "Wake up Collin": True,
    "Hey Colin wake up": True,
    "Hi Colin can you listen": True,
    "Okay Colin wake up": True,
    "open chrome": False,
    "hello": False,
}

for text, expected in tests.items():
    result = is_wake_phrase(text)

    assert result == expected, (
        f"{text!r}: "
        f"expected {expected}, "
        f"got {result}"
    )

print("Collin wake resolver tests: OK")
