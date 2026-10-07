import os, sys

print("=== CHECKING SCRAPERS EXIST OR NOT ===\n")
files_to_check = [
    "chrome/controller.py",
    "knowledge/chatgpt_database_reader.py",
    "knowledge/chatgpt_database.py",
    "teaching/gemini_captions.py",
    "execution/executor.py",
    "file/explorer.py"
]
for f in files_to_check:
    exists = os.path.exists(f)
    print(f"{'EXISTS' if exists else 'MISSING'} -> {f}")

print("\n=== FIXING EVERYTHING FOR 4GB LIGHTWEIGHT MODE ===\n")

# 1. Fix chrome/controller.py to add background mode
os.makedirs("chrome", exist_ok=True)
chrome_path = "chrome/controller.py"
if os.path.exists(chrome_path):
    with open(chrome_path, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    if "open_in_background" not in content:
        with open(chrome_path, 'a', encoding='utf-8') as fp:
            fp.write("""

# --- COLLIN LIGHTWEIGHT FIX: Background open, never in front ---
    def open_in_background(self, url):
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            opts = Options()
            opts.add_argument("--start-minimized")
            opts.add_argument("--window-position=-32000,-32000")
            opts.add_argument("--no-focus")
            opts.add_experimental_option("excludeSwitches", ["enable-automation"])
            driver = webdriver.Chrome(options=opts)
            driver.get(url)
            time.sleep(3)
            src = driver.page_source
            # don't close, keep in background
            return src
        except Exception as e:
            print(f"[COLLIN] Background open failed: {e}")
            return ""

    def scrape_gemini_caption(self):
        try:
            # Gemini Live caption divs are usually [data-captions] or aria-live
            captions = self.driver.find_elements("css selector", "[aria-live='polite'],.caption,.live-caption")
            return " ".join([c.text for c in captions if c.text]) if captions else ""
        except:
            return ""
""")
        print("FIXED -> chrome/controller.py added open_in_background()")

# 2. Rewrite chatgpt_database_reader.py for ChatGPT as DB + profile switching
os.makedirs("knowledge", exist_ok=True)
with open("knowledge/chatgpt_database_reader.py", "w", encoding="utf-8") as f:
    f.write("""import sqlite3, time

class ChatGPTDatabaseReader:
    def __init__(self, db_path="data/collin.db"):
        self.db_path = db_path

    def get_active_link(self):
        import sqlite3
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("SELECT database_url FROM profiles WHERE active=1 LIMIT 1")
        row = cur.fetchone()
        con.close()
        return row[0] if row else None

    def read_as_database(self, background=True):
        link = self.get_active_link()
        if not link:
            print("[COLLIN] No active profile link in collin.db")
            return None
        print(f"[COLLIN] Reading ChatGPT as DB from: {link} (background={background})")
        # Uses chrome controller background method
        try:
            from chrome.controller import ChromeController
            ctrl = ChromeController()
            if hasattr(ctrl, 'open_in_background') and background:
                html = ctrl.open_in_background(link)
            else:
                html = ctrl.open_url(link) if hasattr(ctrl, 'open_url') else ""
            return html
        except Exception as e:
            print(f"[COLLIN] DB read failed, will try profile switch: {e}")
            return None

    def get_last_instruction(self):
        html = self.read_as_database()
        if not html:
            return None
        # Simple: last user instruction is in the HTML
        # You can teach: "tell collin to open xyz in background" inside ChatGPT
        return html[-2000:] # last 2000 chars = your latest teaching
""")
print("FIXED -> knowledge/chatgpt_database_reader.py rewrote as ChatGPT-as-DB")

# 3. Create background executor for your "open xyz in background" requirement
os.makedirs("execution", exist_ok=True)
with open("execution/background_executor.py", "w", encoding="utf-8") as f:
    f.write("""import os
# COLLIN: Executes anything in background, never brings to front
def execute_in_background(task, url=None):
    print(f"[COLLIN] Executing in BACKGROUND: {task}")
    if url or "http" in task:
        from knowledge.chatgpt_database_reader import ChatGPTDatabaseReader
        from chrome.controller import ChromeController
        ctrl = ChromeController()
        target = url if url else task.split()[-1]
        if not target.startswith("http"):
            target = "https://" + target
        if hasattr(ctrl, 'open_in_background'):
            return ctrl.open_in_background(target)
    return f"Background task done: {task}"
""")
print("CREATED -> execution/background_executor.py")

# 4. Fix gemini captions keeper
with open("teaching/gemini_captions.py", "w", encoding="utf-8") as f:
    f.write("""import time

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
""")
print("FIXED -> teaching/gemini_captions.py rewrote as keeper")

print("\n=== ALL FIXED ===")
print("Your system is now: collin.db stays (tiny), ChatGPT chat is big DB, Gemini Live is ears, everything opens in background")
