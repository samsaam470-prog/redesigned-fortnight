from __future__ import annotations

import threading
import tkinter as tk


class StatusIndicator:
    """Small temporary status overlay for Collin."""

    def __init__(self):
        self._lock = threading.Lock()
        self._root = None
        self._thread = None

    def show(self, status: str, duration: float = 2.2) -> None:
        status = str(status).lower().strip()

        labels = {
            "awake": ("COLLIN — AWAKE", "lime"),
            "learning": ("COLLIN — LEARNING", "yellow"),
            "learned": ("COLLIN — LEARNED", "deepskyblue"),
            "observing": ("COLLIN — OBSERVING", "deepskyblue"),
            "sleeping": ("COLLIN — SLEEPING", "white"),
        }

        label_text, dot_color = labels.get(
            status,
            (f"COLLIN — {status.upper()}", "white")
        )

        def worker():
            try:
                root = tk.Tk()
                root.overrideredirect(True)
                root.attributes("-topmost", True)
                root.configure(bg="black")

                width = 250
                height = 72

                screen_w = root.winfo_screenwidth()
                x = screen_w - width - 20
                y = 20

                root.geometry(f"{width}x{height}+{x}+{y}")

                frame = tk.Frame(root, bg="black")
                frame.pack(fill="both", expand=True)

                canvas = tk.Canvas(
                    frame,
                    width=42,
                    height=42,
                    bg="black",
                    highlightthickness=0,
                )
                canvas.pack(side="left", padx=(12, 6), pady=15)

                canvas.create_oval(
                    7, 7, 35, 35,
                    fill=dot_color,
                    outline=dot_color,
                )

                tk.Label(
                    frame,
                    text=label_text,
                    fg="white",
                    bg="black",
                    font=("Segoe UI", 10, "bold"),
                ).pack(side="left", padx=4)

                root.after(
                    int(duration * 1000),
                    root.destroy
                )

                root.mainloop()

            except Exception:
                pass

        with self._lock:
            self._thread = threading.Thread(
                target=worker,
                daemon=True,
            )
            self._thread.start()
