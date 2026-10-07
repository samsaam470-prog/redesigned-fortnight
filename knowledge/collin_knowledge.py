import hashlib
import json
import os
import time


class CollinKnowledge:
    """
    Local cache for Collin's external ChatGPT Database knowledge.

    ChatGPT Database is the human-maintained source.
    Collin keeps a lightweight local snapshot so the runtime
    does not need a large local AI model.
    """

    CACHE_FILE = os.path.join(
        "knowledge",
        "collin_database_cache.json",
    )

    def __init__(self):
        self.instructions = ""
        self.version_hash = ""
        self.updated_at = None
        self.load()

    def load(self):
        try:
            if not os.path.exists(self.CACHE_FILE):
                return False

            with open(
                self.CACHE_FILE,
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            self.instructions = data.get(
                "instructions",
                "",
            )

            self.version_hash = data.get(
                "version_hash",
                "",
            )

            self.updated_at = data.get(
                "updated_at",
            )

            return True

        except Exception as exc:
            print(
                f"COLLIN KNOWLEDGE: cache load error: {exc}"
            )
            return False

    def update(self, instructions):
        if not isinstance(instructions, str):
            return False

        instructions = instructions.strip()

        if not instructions:
            return False

        new_hash = hashlib.sha256(
            instructions.encode("utf-8")
        ).hexdigest()

        changed = new_hash != self.version_hash

        if not changed:
            return False

        self.instructions = instructions
        self.version_hash = new_hash
        self.updated_at = time.time()

        os.makedirs(
            os.path.dirname(self.CACHE_FILE),
            exist_ok=True,
        )

        with open(
            self.CACHE_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                {
                    "instructions": self.instructions,
                    "version_hash": self.version_hash,
                    "updated_at": self.updated_at,
                },
                file,
                indent=2,
                ensure_ascii=False,
            )

        print(
            "COLLIN KNOWLEDGE: database instructions changed."
        )

        return True

    def get_instructions(self):
        return self.instructions

    def has_knowledge(self):
        return bool(self.instructions)

    def changed(self, instructions):
        if not isinstance(instructions, str):
            return False

        new_hash = hashlib.sha256(
            instructions.strip().encode("utf-8")
        ).hexdigest()

        return new_hash != self.version_hash
