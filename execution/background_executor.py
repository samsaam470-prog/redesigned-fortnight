import os
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
