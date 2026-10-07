from language.parser import CommandParser
from knowledge.collin_knowledge import CollinKnowledge
from knowledge.database_rules import DatabaseRules


class DatabaseAwareParser(CommandParser):
    """
    Normal Collin parser + dynamically learned Database rules.

    Database rules take priority over built-in aliases.
    """

    def __init__(self):
        super().__init__()

        self.knowledge = CollinKnowledge()
        self.database_rules = DatabaseRules(
            self.knowledge
        )

    def reload_database_rules(self):
        self.knowledge.load()
        self.database_rules.reload()

    def parse(self, text):
        self.reload_database_rules()

        rule = self.database_rules.resolve(text)

        if rule:
            return self._rule_to_intent(rule)

        return super().parse(text)

    @staticmethod
    def _rule_to_intent(rule):
        from language.intent import Intent, IntentType

        intent_name = rule.get("intent", "")
        target = rule.get("target")

        mapping = {
            "open_url": IntentType.OPEN_URL,
            "open_application": IntentType.OPEN_APPLICATION,
            "search": IntentType.SEARCH,
            "click": IntentType.CLICK,
            "type": IntentType.TYPE,
            "scroll": IntentType.SCROLL,
            "keyboard": IntentType.KEYBOARD,
        }

        intent_type = mapping.get(
            intent_name,
            IntentType.UNKNOWN,
        )

        return Intent(
            intent_type,
            target=target,
        )
