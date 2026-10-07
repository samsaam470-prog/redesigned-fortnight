"""
Collin V0.1 - File Explorer / Filesystem Controller

Provides lightweight filesystem operations for Collin.

This module works with the Windows filesystem directly.
It does NOT contain:
- natural-language parsing
- AI/LLM logic
- teaching logic
- database logic
- VS Code logic
- Chrome logic
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any


class FileExplorer:
    """Lightweight controller for files and folders."""

    def _path(self, path: str) -> Path:
        """Convert a user-provided path into an absolute Path."""
        if not path or not path.strip():
            raise ValueError("Path cannot be empty.")

        return Path(path).expanduser().resolve()

    # ---------------------------------------------------------------
    # Check
    # ---------------------------------------------------------------

    def exists(self, path: str) -> bool:
        """Return True if a file or folder exists."""
        return self._path(path).exists()

    def is_file(self, path: str) -> bool:
        """Return True if the path is a file."""
        return self._path(path).is_file()

    def is_folder(self, path: str) -> bool:
        """Return True if the path is a folder."""
        return self._path(path).is_dir()

    # ---------------------------------------------------------------
    # Folders
    # ---------------------------------------------------------------

    def create_folder(self, path: str) -> Path:
        """Create a folder and any missing parent folders."""
        target = self._path(path)
        target.mkdir(parents=True, exist_ok=True)
        return target

    def list_folder(self, path: str) -> list[dict[str, Any]]:
        """List files and folders inside a directory."""
        target = self._path(path)

        if not target.is_dir():
            raise NotADirectoryError(
                f"Not a directory: {target}"
            )

        items = []

        for item in sorted(target.iterdir(), key=lambda p: p.name.lower()):
            items.append(
                {
                    "name": item.name,
                    "path": str(item),
                    "type": "folder" if item.is_dir() else "file",
                }
            )

        return items

    # ---------------------------------------------------------------
    # Files
    # ---------------------------------------------------------------

    def create_file(
        self,
        path: str,
        content: str = "",
    ) -> Path:
        """Create a file with optional text content."""

        target = self._path(path)

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

        return target

    def read_file(self, path: str) -> str:
        """Read a UTF-8 text file."""
        target = self._path(path)

        if not target.is_file():
            raise FileNotFoundError(
                f"File does not exist: {target}"
            )

        return target.read_text(encoding="utf-8")

    def write_file(
        self,
        path: str,
        content: str,
    ) -> Path:
        """Replace the contents of a text file."""

        target = self._path(path)

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

        return target

    def append_file(
        self,
        path: str,
        content: str,
    ) -> Path:
        """Append text to a file."""

        target = self._path(path)

        target.parent.mkdir(parents=True, exist_ok=True)

        with target.open("a", encoding="utf-8") as file:
            file.write(content)

        return target

    # ---------------------------------------------------------------
    # Rename / Move / Copy
    # ---------------------------------------------------------------

    def rename(self, path: str, new_name: str) -> Path:
        """Rename a file or folder."""

        if not new_name or not new_name.strip():
            raise ValueError("New name cannot be empty.")

        source = self._path(path)

        if not source.exists():
            raise FileNotFoundError(
                f"Path does not exist: {source}"
            )

        destination = source.parent / new_name.strip()
        source.rename(destination)

        return destination

    def move(self, source: str, destination: str) -> Path:
        """Move a file or folder."""

        source_path = self._path(source)
        destination_path = self._path(destination)

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: {source_path}"
            )

        destination_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        result = shutil.move(
            str(source_path),
            str(destination_path),
        )

        return Path(result)

    def copy(self, source: str, destination: str) -> Path:
        """Copy a file or folder."""

        source_path = self._path(source)
        destination_path = self._path(destination)

        if not source_path.exists():
            raise FileNotFoundError(
                f"Source does not exist: {source_path}"
            )

        if source_path.is_dir():
            result = shutil.copytree(
                source_path,
                destination_path,
                dirs_exist_ok=True,
            )
        else:
            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            result = shutil.copy2(
                source_path,
                destination_path,
            )

        return Path(result)

    # ---------------------------------------------------------------
    # Delete
    # ---------------------------------------------------------------

    def delete(self, path: str) -> bool:
        """
        Delete a file or folder.

        This is intentionally a direct operation.
        Higher-level Collin logic should request confirmation
        before destructive actions.
        """

        target = self._path(path)

        if not target.exists():
            return False

        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()

        return True


# -------------------------------------------------------------------
# Basic standalone test
# -------------------------------------------------------------------

def main() -> None:
    """Run a safe read-only test."""

    explorer = FileExplorer()

    current = Path.cwd()

    print("Filesystem controller: OK")
    print("Current directory:", current)
    print("Exists:", explorer.exists(str(current)))
    print("Is folder:", explorer.is_folder(str(current)))

    print("\nContents:")

    for item in explorer.list_folder(str(current)):
        print(f"  [{item['type']}] {item['name']}")


if __name__ == "__main__":
    main()
