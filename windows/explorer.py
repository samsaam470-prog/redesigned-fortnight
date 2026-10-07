"""
Collin V0.1 - Windows Explorer UI Controller

Controls the actual Windows File Explorer application and
Windows file-selection dialogs.

This module is intentionally separate from file/explorer.py.

file/explorer.py:
    Direct filesystem operations.

windows/explorer.py:
    Visual Windows Explorer / file-dialog operations.

Low-level mouse, keyboard, and screen operations will eventually
be provided by Collin's computer/ module.
"""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Optional


class WindowsExplorerController:
    """Lightweight controller for Windows File Explorer."""

    def __init__(self):
        self.explorer_process = "explorer.exe"

    # ------------------------------------------------------------------
    # Open Windows File Explorer
    # ------------------------------------------------------------------

    def open(self, path: Optional[str] = None) -> bool:
        """
        Open Windows File Explorer.

        If path is supplied, Explorer opens at that location.
        """

        try:
            if path:
                target = Path(path).expanduser().resolve()

                if not target.exists():
                    raise FileNotFoundError(
                        f"Path does not exist: {target}"
                    )

                subprocess.Popen(
                    ["explorer.exe", str(target)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
            else:
                subprocess.Popen(
                    ["explorer.exe"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )

            time.sleep(1.0)
            return True

        except FileNotFoundError:
            raise

        except Exception as exc:
            raise RuntimeError(
                f"Could not open Windows File Explorer: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Open a folder
    # ------------------------------------------------------------------

    def open_folder(self, folder_path: str) -> bool:
        """Open a specific folder in Windows File Explorer."""

        if not folder_path or not folder_path.strip():
            raise ValueError("Folder path cannot be empty.")

        path = Path(folder_path).expanduser().resolve()

        if not path.is_dir():
            raise NotADirectoryError(
                f"Folder does not exist: {path}"
            )

        return self.open(str(path))

    # ------------------------------------------------------------------
    # Open a file's containing folder
    # ------------------------------------------------------------------

    def show_file(self, file_path: str) -> bool:
        """
        Open the containing folder and select a file when possible.

        Windows Explorer supports selecting a file using:
        explorer.exe /select,<path>
        """

        if not file_path or not file_path.strip():
            raise ValueError("File path cannot be empty.")

        path = Path(file_path).expanduser().resolve()

        if not path.is_file():
            raise FileNotFoundError(
                f"File does not exist: {path}"
            )

        try:
            subprocess.Popen(
                ["explorer.exe", f"/select,{path}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            time.sleep(1.0)
            return True

        except Exception as exc:
            raise RuntimeError(
                f"Could not show file in Explorer: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Open a file using its default Windows application
    # ------------------------------------------------------------------

    def open_file(self, file_path: str) -> bool:
        """Open a file using its normal Windows application."""

        if not file_path or not file_path.strip():
            raise ValueError("File path cannot be empty.")

        path = Path(file_path).expanduser().resolve()

        if not path.is_file():
            raise FileNotFoundError(
                f"File does not exist: {path}"
            )

        try:
            os.startfile(str(path))
            return True

        except Exception as exc:
            raise RuntimeError(
                f"Could not open file: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Open a Windows file-selection dialog
    # ------------------------------------------------------------------

    def open_file_dialog(self) -> bool:
        """
        Placeholder for opening a Windows file-selection dialog.

        The actual dialog interaction will later be performed by
        computer/mouse.py, computer/keyboard.py, and computer/screen.py.

        This method intentionally does not fake a dialog.
        """

        raise NotImplementedError(
            "File-dialog UI control will be implemented through "
            "Collin's computer-control layer."
        )

    # ------------------------------------------------------------------
    # Basic status
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """Return True when running on Windows."""

        return os.name == "nt"


# ----------------------------------------------------------------------
# Safe standalone test
# ----------------------------------------------------------------------

def main() -> None:
    """Run a safe read-only test."""

    explorer = WindowsExplorerController()

    print("Windows Explorer controller: OK")
    print("Windows platform:", explorer.is_available())
    print("Explorer executable:", explorer.explorer_process)


if __name__ == "__main__":
    main()
