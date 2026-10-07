
import threading
import time

from wake.resolver import is_wake_phrase


class TypedActivationListener:
    def __init__(self, callback=None, idle_seconds=0.55):
        self.callback = callback
        self.idle_seconds = idle_seconds
        self.running = False
        self._buffer = ""
        self._lock = threading.Lock()
        self._last_input = 0.0
        self._timer = None

    def _normalize(self, text):
        return " ".join(text.strip().lower().split())

    def _emit(self, text):
        text = self._normalize(text)
        if not text:
            return

        print(f"COLLIN TYPED DETECTED: '{text}'")

        if self.callback:
            try:
                self.callback(text)
            except Exception as exc:
                print(f"COLLIN: TYPED CALLBACK ERROR: {exc}")

    def _flush(self):
        with self._lock:
            if not self.running:
                return

            text = self._normalize(self._buffer)
            elapsed = time.monotonic() - self._last_input

            if not text or elapsed < self.idle_seconds:
                return

            self._buffer = ""

        # Single-word commands remain supported.
        single_words = {
            "sleep",
            "colin",
            "collin",
            "calling",
            "callin",
        }

        # Multi-word phrases are checked as complete phrases.
        if text in single_words or len(text.split()) >= 2:
            self._emit(text)

    def _schedule_flush(self):
        if self._timer:
            try:
                self._timer.cancel()
            except Exception:
                pass

        self._timer = threading.Timer(self.idle_seconds, self._flush)
        self._timer.daemon = True
        self._timer.start()

    def feed_text(self, text):
        if not isinstance(text, str):
            return

        with self._lock:
            if not self.running:
                return

            self._buffer += text
            self._last_input = time.monotonic()

        self._schedule_flush()

    def process_text(self, text):
        self.feed_text(text)

    def start(self):
        if self.running:
            return

        self.running = True
        print("COLLIN: GLOBAL TYPING LISTENER STARTED")

    def stop(self):
        self.running = False

        if self._timer:
            try:
                self._timer.cancel()
            except Exception:
                pass

        with self._lock:
            self._buffer = ""

        print("COLLIN: GLOBAL TYPING LISTENER STOPPED")
