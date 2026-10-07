import re


class DatabaseRules:
    """
    Converts natural-language rules stored in the Collin Database
    into lightweight executable rules.

    The Database may contain blocks such as:

    USER:
    When I say open IG, search Insta, or search Instagram,
    I want Collin to open Instagram.

    COLLIN_RULE:
    INTENT=open_url
    TARGET=https://instagram.com
    PHRASES=open ig|search insta|search instagram

    Collin primarily consumes COLLIN_RULE blocks.
    """

    def __init__(self, knowledge=None):
        self.knowledge = knowledge
        self.rules = []
        self.reload()

    def reload(self):
        self.rules = []

        if not self.knowledge:
            return

        text = self.knowledge.get_instructions()

        if not text:
            return

        self._parse_rules(text)

    def _parse_rules(self, text):
        blocks = re.split(
            r"(?=COLLIN_RULE\s*:)",
            text,
            flags=re.IGNORECASE,
        )

        for block in blocks:
            if not re.search(
                r"COLLIN_RULE\s*:",
                block,
                re.IGNORECASE,
            ):
                continue

            intent = self._field(
                block,
                "INTENT",
            )

            target = self._field(
                block,
                "TARGET",
            )

            phrases = self._field(
                block,
                "PHRASES",
            )

            if not intent:
                continue

            phrase_list = []

            if phrases:
                phrase_list = [
                    self._normalize(item)
                    for item in phrases.split("|")
                    if item.strip()
                ]

            self.rules.append(
                {
                    "intent": intent.strip().lower(),
                    "target": target.strip()
                    if target
                    else None,
                    "phrases": phrase_list,
                }
            )

    @staticmethod
    def _field(block, name):
        match = re.search(
            rf"^{name}\s*=\s*(.+)$",
            block,
            re.IGNORECASE | re.MULTILINE,
        )

        if not match:
            return None

        return match.group(1).strip()

    @staticmethod
    def _normalize(text):
        return " ".join(
            text.lower().strip().split()
        )

    def resolve(self, command):
        normalized = self._normalize(command)

        for rule in self.rules:
            if normalized in rule["phrases"]:
                return rule

        return None

    def resolve_open(self, command):
        rule = self.resolve(command)

        if not rule:
            return None

        if rule["intent"] != "open_url":
            return None

        return rule.get("target")

    def get_rules(self):
        return list(self.rules)
