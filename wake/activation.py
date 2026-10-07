from wake.resolver import is_wake_phrase
from teaching.status_indicator import StatusIndicator
from teaching.session import TeachingSessionManager
import pyperclip
import pyautogui


class CollinActivation:

    SLEEP_PHRASES = {
        "sleep",
        "sleep colin",
        "sleep collin",
        "go to sleep",
        "go to sleep colin",
        "go to sleep collin",
    }

    LEARN_START = {
        "learn",
        "learn it",
        "learn this",
        "start learning",
        "begin learning",
        "start learn",
        "begin learn",
    }

    LEARN_STOP = {
        "stop learning",
        "finish learning",
        "end learning",
        "stop learn",
        "finish learn",
    }

    PASTE_LEARNED = {
        "paste it here",
        "paste here",
        "paste what i learned",
        "paste what i learnt",
        "paste what i learned here",
        "paste what i learnt here",
        "paste what you learned",
        "paste what you learnt",
        "paste what i have learned",
        "paste what i have learnt",
        "paste learned",
        "paste learnt",
        "paste learned procedure",
        "paste learnt procedure",
        "paste my learned procedure",
        "paste my learnt procedure",
        "paste the learned procedure",
        "paste the learnt procedure",
    }

    def __init__(self, runtime=None):
        self.runtime = runtime
        self.awake = False
        self.learning = False

        self.session = TeachingSessionManager()

        self.last_learning_session = None
        self.last_learned_text = ""

        self.indicator = StatusIndicator()

    def sleep(self):
        self.awake = False
        self.learning = False

        try:
            self.indicator.show("sleeping")
        except Exception:
            pass

        print("COLLIN: SLEEPING")

    def wake(self):
        self.awake = True

        try:
            self.indicator.show("awake")
        except Exception:
            pass

        print("COLLIN: AWAKE")

    def start_learning(self):
        if not self.awake:
            return True

        if self.learning:
            print("COLLIN: ALREADY LEARNING.")
            return True

        self.learning = True

        try:
            self.session.start()
        except Exception as exc:
            self.learning = False
            print(f"COLLIN: LEARNING ERROR: {exc}")
            return True

        try:
            self.indicator.show("learning")
        except Exception:
            pass

        print("COLLIN: LEARNING STARTED.")
        return True

    def stop_learning(self):
        if not self.learning:
            print("COLLIN: NOT CURRENTLY LEARNING.")
            return True

        try:
            procedure = self.session.finish(
                name="learned_procedure"
            )

            if not procedure:
                self.learning = False
                print("COLLIN: LEARNING SAVE FAILED.")
                return True

            self.last_learning_session = procedure

            learned_text = self._format_procedure(
                procedure
            )

            self.last_learned_text = learned_text

            pyperclip.copy(
                learned_text
            )

            self.learning = False

            print("COLLIN: LEARNING SAVED.")
            print("COLLIN: READY TO PASTE.")

            return True

        except Exception as exc:
            self.learning = False
            print(
                f"COLLIN: LEARNING SAVE ERROR: {exc}"
            )
            return True

    def paste_what_you_learned(self):
        try:
            if not self.last_learned_text:
                print("COLLIN: NOTHING LEARNED YET.")
                return True

            pyperclip.copy(
                self.last_learned_text
            )

            pyautogui.hotkey(
                "ctrl",
                "v"
            )

            print("COLLIN: PASTED.")

        except Exception as exc:
            print(
                f"COLLIN: PASTE ERROR: {exc}"
            )

        return True

    def process_text(self, text):
        if not isinstance(text, str):
            return False

        normalized = " ".join(
            text.strip().lower().split()
        )

        if not normalized:
            return False

        if is_wake_phrase(normalized):
            self.wake()
            return True

        if normalized in self.SLEEP_PHRASES:
            self.sleep()
            return True

        if normalized in self.LEARN_START:
            return self.start_learning()

        if normalized in self.LEARN_STOP:
            return self.stop_learning()

        if normalized in self.PASTE_LEARNED:
            return self.paste_what_you_learned()

        if self.learning:
            try:
                self.session.add_instruction(
                    normalized
                )

                self.session.observe()

            except Exception as exc:
                print(
                    f"COLLIN: LEARNING RECORD ERROR: {exc}"
                )

            return True

        return False

    @staticmethod
    def _format_procedure(procedure):
        lines = [
            "COLLIN LEARNED PROCEDURE",
            "",
        ]

        if isinstance(procedure, dict):

            name = procedure.get("name")
            instruction = procedure.get("instruction")

            if name:
                lines.append(
                    f"Name: {name}"
                )

            if instruction:
                lines.append(
                    f"Instruction: {instruction}"
                )

            events = procedure.get(
                "events",
                []
            )

            if events:
                lines.append("")
                lines.append("Learned events:")

                for index, event in enumerate(
                    events,
                    1
                ):
                    lines.append(
                        f"{index}. {event}"
                    )

        else:
            lines.append(
                str(procedure)
            )

        return "\n".join(lines)
