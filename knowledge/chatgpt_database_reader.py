import sqlite3, time

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
