"""
Collin V0.1 - VS Code Controller

Controls the real Microsoft Visual Studio Code application on Windows.

This module intentionally does NOT contain:
- natural-language parsing
- AI/LLM logic
- teaching logic
- database logic
- code generation logic

Those responsibilities belong to other Collin modules.
"""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Optional


class VSCodeController:
    """Lightweight controller for the installed Visual Studio Code."""

    def __init__(self, code_path: Optional[str] = None):
        self.code_path = code_path or self._find_vscode()

    # ------------------------------------------------------------------
    # VS Code discovery
    # ------------------------------------------------------------------

    def _find_vscode(self) -> Optional[str]:
        """Find the standard VS Code installation on Windows."""

        possible_paths = [
            os.path.expandvars(
                r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
            ),
            os.path.expandvars(
                r"%PROGRAMFILES%\Microsoft VS Code\Code.exe"
            ),
            os.path.expandvars(
                r"%PROGRAMFILES(X86)%\Microsoft VS Code\Code.exe"
            ),
        ]

        for path in possible_paths:
            if Path(path).is_file():
                return path

        return None

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def is_installed(self) -> bool:
        """Return True if VS Code can be found."""
        return self.code_path is not None

    def is_running(self) -> bool:
        """Return True if Code.exe is currently running."""

        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq Code.exe"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            return "code.exe" in result.stdout.lower()

        except Exception:
            return False

    # ------------------------------------------------------------------
    # Launch
    # ------------------------------------------------------------------

    def open(self) -> bool:
        """Open VS Code."""

        if not self.is_installed():
            raise FileNotFoundError(
                "Visual Studio Code was not found on this Windows computer."
            )

        try:
            subprocess.Popen(
                [self.code_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            time.sleep(1.5)
            return True

        except Exception as exc:
            raise RuntimeError(
                f"Could not start VS Code: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Open files and folders
    # ------------------------------------------------------------------

    def open_folder(self, folder_path: str) -> bool:
        """Open a folder in VS Code."""

        if not folder_path or not folder_path.strip():
            raise ValueError("Folder path cannot be empty.")

        path = Path(folder_path).expanduser().resolve()

        if not path.is_dir():
            raise FileNotFoundError(
                f"Folder does not exist: {path}"
            )

        return self._run_code_command(["--new-window", str(path)])

    def open_file(self, file_path: str) -> bool:
        """Open a file in VS Code."""

        if not file_path or not file_path.strip():
            raise ValueError("File path cannot be empty.")

        path = Path(file_path).expanduser().resolve()

        if not path.is_file():
            raise FileNotFoundError(
                f"File does not exist: {path}"
            )

        return self._run_code_command([str(path)])

    # ------------------------------------------------------------------
    # Terminal
    # ------------------------------------------------------------------

    def open_terminal(self) -> bool:
        """
        Open VS Code.

        The actual integrated-terminal keyboard/UI interaction will be
        handled later by the computer controller and teaching system.
        """

        if not self.is_installed():
            raise FileNotFoundError(
                "Visual Studio Code was not found."
            )

        # VS Code command-line interface cannot directly guarantee
        # opening the integrated terminal, so we leave that action to
        # the computer-control layer.
        return self.open()

    # ------------------------------------------------------------------
    # Internal command runner
    # ------------------------------------------------------------------

    def _run_code_command(self, arguments: list[str]) -> bool:
        """Run the VS Code executable with command-line arguments."""

        if not self.is_installed():
            raise FileNotFoundError(
                "Visual Studio Code was not found."
            )

        try:
            subprocess.Popen(
                [self.code_path, *arguments],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            time.sleep(1.0)
            return True

        except Exception as exc:
            raise RuntimeError(
                f"Could not execute VS Code command: {exc}"
            ) from exc


# ----------------------------------------------------------------------
# Simple standalone test
# ----------------------------------------------------------------------

def main() -> None:
    """Basic manual test for the VS Code controller."""

    vscode = VSCodeController()

    print("VS Code installed:", vscode.is_installed())
    print("VS Code running:", vscode.is_running())
    print("VS Code path:", vscode.code_path)


if __name__ == "__main__":
    main()
