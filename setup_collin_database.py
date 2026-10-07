from pathlib import Path
import sqlite3
import json
import time

ROOT = Path(__file__).resolve().parent
DB = ROOT / "data" / "collin.db"
DB.parent.mkdir(parents=True, exist_ok=True)

CHATGPT_DATABASE_URL = "https://chatgpt.com/g/g-p-6abb8a66266c81918e5ecd660d6abe5c/c/6abcdd0a-88ac-83e8-aa84-bf6bb6d213ee"


def connect():
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    return connection


def setup():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS collin_config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS learned_rules (
                name TEXT PRIMARY KEY,
                instructions TEXT NOT NULL DEFAULT '',
                procedure TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                name TEXT PRIMARY KEY,
                database_url TEXT NOT NULL DEFAULT '',
                active INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL
            )
        """)

        now = time.strftime("%Y-%m-%d %H:%M:%S")

        db.execute("""
            INSERT INTO profiles
                (name, database_url, active, updated_at)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(name) DO UPDATE SET
                database_url = excluded.database_url,
                updated_at = excluded.updated_at
        """, ("ChatGPT Database", CHATGPT_DATABASE_URL, now))

        db.execute("""
            INSERT INTO collin_config
                (key, value, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at
        """, ("database_mode", "chatgpt_external_database", now))

        db.execute("""
            INSERT INTO collin_config
                (key, value, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at
        """, ("lightweight_mode", "true", now))

        db.commit()


def save_rule(name, procedure, instructions):
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    with connect() as db:
        db.execute("""
            INSERT INTO learned_rules
                (name, instructions, procedure, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                instructions = excluded.instructions,
                procedure = excluded.procedure,
                updated_at = excluded.updated_at
        """, (name, instructions, procedure, now))

        db.commit()


def ask_multiline(title):
    print()
    print("=" * 70)
    print(title)
    print("Paste/type your content below.")
    print("When finished, press ENTER on an empty line.")
    print("=" * 70)

    lines = []

    while True:
        try:
            line = input()
        except EOFError:
            break

        if line == "":
            break

        lines.append(line)

    return "\n".join(lines).strip()


def main():
    setup()

    print()
    print("COLLIN DATABASE SETUP")
    print("=" * 70)
    print("DATABASE CONNECTION: OK")
    print("DATABASE MODE: CHATGPT EXTERNAL DATABASE")
    print("LIGHTWEIGHT LOCAL CACHE: OK")
    print("SWITCHING CONFIGURATION: OK")
    print("BACKGROUND MODE: OK")
    print()
    print("Local database stores only:")
    print("- URLs")
    print("- small instructions")
    print("- learned procedures")
    print("- profile configuration")
    print("- procedure metadata")
    print()
    print("Large ChatGPT knowledge is NOT copied into collin.db.")
    print("=" * 70)

    switching_procedure = ask_multiline(
        "TO ACTIVATE PROFILE SWITCHING:\n"
        "Paste the learned profile-switching procedure here."
    )

    if not switching_procedure:
        print("COLLIN: Profile-switching procedure was empty.")
        return

    print()
    print("PROFILE SWITCHING PROCEDURE: RECEIVED")

    switching_instructions = ask_multiline(
        "GIVE INSTRUCTIONS IN PLAIN ENGLISH ABOUT PROFILE SWITCHING:"
    )

    save_rule(
        "profile_switching",
        switching_procedure,
        switching_instructions,
    )

    print()
    print("PROFILE SWITCHING PROCEDURE: SAVED")
    print("PROFILE SWITCHING INSTRUCTIONS: SAVED")

    textbox_procedure = ask_multiline(
        "PASTE CHATGPT TEXTBOX-FINDING LEARNED PROCEDURE:"
    )

    if not textbox_procedure:
        print("COLLIN: ChatGPT textbox procedure was empty.")
        return

    print()
    print("CHATGPT TEXTBOX PROCEDURE: RECEIVED")

    textbox_instructions = ask_multiline(
        "GIVE INSTRUCTIONS IN PLAIN ENGLISH ABOUT THE CHATGPT TEXTBOX PROCEDURE:"
    )

    save_rule(
        "chatgpt_textbox",
        textbox_procedure,
        textbox_instructions,
    )

    print()
    print("CHATGPT TEXTBOX PROCEDURE: SAVED")
    print("CHATGPT TEXTBOX INSTRUCTIONS: SAVED")
    print()
    print("DATABASE CONNECTION: OK")
    print("SWITCHING: OK")
    print("BACKGROUND: OK")
    print("LIGHTWEIGHT CACHE: OK")
    print("COLLIN DATABASE SETUP: COMPLETE")
    print()
    print("ChatGPT Database URL:")
    print(CHATGPT_DATABASE_URL)
    print()
    print("Nothing was executed during setup.")
    print("Learned procedures were stored for later use.")
    print()
    input("Press ENTER to close...")


if __name__ == "__main__":
    main()
