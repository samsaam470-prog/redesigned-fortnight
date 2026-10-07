import os
import sqlite3

root = "."
ignore_dirs = {'.git', '__pycache__', '.vscode', 'logs', '.venv', 'venv'}

print("=== FILE LIST + LINE COUNT ===\n")
total_lines = 0
file_list = []
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
    for f in filenames:
        if f.endswith(('.db', '.pyc', '.log', '.txt')):
            continue
        fp = os.path.join(dirpath, f)
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
                lines = len(file.readlines())
                print(f"{fp} -> {lines} lines")
                file_list.append(f"{fp} -> {lines}")
                total_lines += lines
        except:
            print(f"{fp} -> [binary]")

print(f"\nTOTAL LINES: {total_lines}\n")

print("\n=== CONTENT OF collin.db AT END ===\n")
db_path = "data/collin.db"
if not os.path.exists(db_path):
    print(f"DB not found at {db_path}")
    # try find db anywhere
    for r, d, fs in os.walk("."):
        for ff in fs:
            if ff.endswith(".db"):
                print(f"Found DB at: {os.path.join(r, ff)}")
else:
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    print(f"Tables: {tables}\n")
    for t in tables:
        tn = t[0]
        print(f"--- TABLE: {tn} ---")
        cur.execute(f"SELECT * FROM {tn}")
        rows = cur.fetchall()
        cols = [x[0] for x in cur.description]
        print(f"Columns: {cols}")
        for row in rows[:50]:
            print(row)
        print("")
    con.close()
