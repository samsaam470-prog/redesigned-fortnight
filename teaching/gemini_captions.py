import time

class GeminiCaptionKeeper:
    def __init__(self):
        self.wake_words = ["hi collin", "hi calling", "hey collin", "collin"]

    def keep_alive_loop(self):
        print("[COLLIN] Gemini Live keeper started (background, lightweight)")
        while True:
            try:
                from chrome.controller import ChromeController
                ctrl = ChromeController()
                cap = ctrl.scrape_gemini_caption() if hasattr(ctrl, 'scrape_gemini_caption') else ""
                if not cap:
                    print("[COLLIN] Caption stopped, reopening Gemini Live in background...")
                    if hasattr(ctrl, 'open_in_background'):
                        ctrl.open_in_background("https://gemini.google.com/app")
                time.sleep(10)
            except Exception as e:
                print(f"[Keeper] error {e}")
                time.sleep(10)

    def listen(self):
        print("[COLLIN] Listening for wake word via Gemini Live captions...")
        while True:
            try:
                from chrome.controller import ChromeController
                ctrl = ChromeController()
                cap = ctrl.scrape_gemini_caption() if hasattr(ctrl, 'scrape_gemini_caption') else ""
                if cap:
                    low = cap.lower()
                    for w in self.wake_words:
                        if w in low:
                            print(f"[WAKE] Heard: {cap}")
                            return cap
                time.sleep(0.5)
            except:
                time.sleep(0.5)
