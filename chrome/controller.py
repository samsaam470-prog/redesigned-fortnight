"""
Collin V0.1 - Chrome Controller

Controls the real Google Chrome application on Windows.

This module intentionally does NOT contain:
- natural-language parsing
- Gemini Live logic
- teaching logic
- database logic
- AI/LLM logic

Those responsibilities belong to other Collin modules.
"""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Optional


class ChromeController:
    """Lightweight controller for the installed Google Chrome browser."""

    def __init__(self, chrome_path: Optional[str] = None):
        self.chrome_path = chrome_path or self._find_chrome()

    # ------------------------------------------------------------------
    # Chrome discovery
    # ------------------------------------------------------------------

    def _find_chrome(self) -> Optional[str]:
        """Find the standard Chrome installation on Windows."""

        possible_paths = [
            os.path.expandvars(
                r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
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
        """Return True if Chrome can be found on this computer."""
        return self.chrome_path is not None

    def is_running(self) -> bool:
        """Return True if chrome.exe is currently running."""

        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq chrome.exe"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            return "chrome.exe" in result.stdout.lower()

        except Exception:
            return False

    # ------------------------------------------------------------------
    # Launch / focus
    # ------------------------------------------------------------------

    def open(self, url: Optional[str] = None) -> bool:
        """
        Open Chrome.

        If url is supplied, Chrome opens that URL.
        If Chrome is already running, a new tab may be opened.
        """

        if not self.is_installed():
            raise FileNotFoundError(
                "Google Chrome was not found on this Windows computer."
            )

        try:
            command = [self.chrome_path]

            if url:
                command.append(url)

            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            time.sleep(1.5)
            return True

        except Exception as exc:
            raise RuntimeError(f"Could not start Chrome: {exc}") from exc

    def open_new_tab(self) -> bool:
        """Open a new Chrome tab."""

        if not self.is_installed():
            raise FileNotFoundError(
                "Google Chrome was not found on this Windows computer."
            )

        try:
            subprocess.Popen(
                [self.chrome_path, "--new-tab"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            time.sleep(0.8)
            return True

        except Exception as exc:
            raise RuntimeError(
                f"Could not open a new Chrome tab: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def open_url(self, url: str) -> bool:
        """
        Open a specific URL in Chrome.

        URL validation is intentionally basic here.
        Higher-level command validation belongs to the language layer.
        """

        if not url or not url.strip():
            raise ValueError("URL cannot be empty.")

        url = url.strip()

        if not (
            url.startswith("http://")
            or url.startswith("https://")
            or url.startswith("file://")
        ):
            url = "https://" + url

        return self.open(url)

    def google_search(self, query: str) -> bool:
        """Open a Google search for the supplied query."""

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        from urllib.parse import quote_plus

        search_url = (
            "https://www.google.com/search?q="
            + quote_plus(query.strip())
        )

        return self.open_url(search_url)

    # ------------------------------------------------------------------
    # Close
    # ------------------------------------------------------------------

    def close(self) -> bool:
        """
        Close Chrome.

        This asks Chrome to terminate normally through taskkill.
        """

        try:
            result = subprocess.run(
                ["taskkill", "/IM", "chrome.exe"],
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            return result.returncode == 0

        except Exception as exc:
            raise RuntimeError(f"Could not close Chrome: {exc}") from exc


# ----------------------------------------------------------------------
# Simple standalone test
# ----------------------------------------------------------------------

def main() -> None:
    """Basic manual test for the Chrome controller."""

    chrome = ChromeController()

    print("Chrome installed:", chrome.is_installed())
    print("Chrome running:", chrome.is_running())

    if chrome.is_installed():
        print("Chrome path:", chrome.chrome_path)


if __name__ == "__main__":
    main()


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
