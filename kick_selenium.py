"""
============================================================
  KICK FOLLOW IMPORTER — undetected-chromedriver
============================================================
  Installation:
      pip install undetected-chromedriver selenium
  Usage:
      python kick_selenium_uc_en.py
============================================================
"""

import os
import re
import sys
import time
import random
import subprocess
from datetime import datetime

# ── Dependency check at startup ───────────────────────────
def check_dependencies():
    missing = []
    try:
        import undetected_chromedriver
    except ImportError:
        missing.append("undetected-chromedriver")
    try:
        import selenium
    except ImportError:
        missing.append("selenium")
    if missing:
        print(f"  ❌ Missing dependencies: {', '.join(missing)}")
        print(f"  Run: pip install {' '.join(missing)}")
        sys.exit(1)

check_dependencies()

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException,
    WebDriverException, ElementNotInteractableException
)

FOLLOWS_FILE = "kick_follows.txt"
DELAY_MIN    = 3.0
DELAY_MAX    = 6.0
BASE_URL     = "https://kick.com"

# ── Auto-detect installed Chrome version ─────────────────
def get_chrome_version() -> int:
    """Returns the major version of the installed Chrome browser."""
    if sys.platform == "win32":
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        ]
        for path in paths:
            if os.path.exists(path):
                try:
                    result = subprocess.run(
                        [path, "--version"], capture_output=True, text=True, timeout=5
                    )
                    match = re.search(r"(\d+)\.", result.stdout)
                    if match:
                        return int(match.group(1))
                except Exception:
                    continue
        # Fallback via Windows registry
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"Software\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
            return int(version.split(".")[0])
        except Exception:
            pass

    elif sys.platform == "darwin":
        path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(path):
            try:
                result = subprocess.run(
                    [path, "--version"], capture_output=True, text=True, timeout=5
                )
                match = re.search(r"(\d+)\.", result.stdout)
                if match:
                    return int(match.group(1))
            except Exception:
                pass

    else:  # Linux
        for cmd in ["google-chrome", "google-chrome-stable", "chromium-browser", "chromium"]:
            try:
                result = subprocess.run(
                    [cmd, "--version"], capture_output=True, text=True, timeout=5
                )
                match = re.search(r"(\d+)\.", result.stdout)
                if match:
                    return int(match.group(1))
            except Exception:
                continue

    return None

# ── Load channel slugs from file ─────────────────────────
def load_slugs(path: str) -> list:
    if not os.path.exists(path):
        print(f"  ✗ File not found: {path}")
        return []
    slugs = [
        l.strip() for l in open(path, encoding="utf-8")
        if l.strip() and not l.strip().startswith("#")
    ]
    print(f"  ✓ {len(slugs)} channels loaded from {path}")
    return slugs

# ── Initialize the Chrome driver ─────────────────────────
def setup_driver() -> uc.Chrome:
    opts = uc.ChromeOptions()
    opts.add_argument("--start-maximized")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")
    opts.add_argument("--disable-popup-blocking")
    # Optional: persistent profile to keep session across runs
    # opts.add_argument("--user-data-dir=C:/kick_chrome_profile")

    version = get_chrome_version()
    if version:
        print(f"  ✓ Chrome version detected: {version}")
        driver = uc.Chrome(options=opts, version_main=version)
    else:
        print("  ⚠ Could not detect Chrome version, trying automatically...")
        driver = uc.Chrome(options=opts)

    return driver

# ── Wait for manual login ─────────────────────────────────
def wait_for_login(driver: uc.Chrome) -> bool:
    print("\n  → Opening kick.com...")
    driver.get(BASE_URL)
    time.sleep(3)

    print("""
  ╔══════════════════════════════════════════════════╗
  ║  LOG IN TO KICK IN THE BROWSER WINDOW            ║
  ║  Then come back here and press ENTER             ║
  ╚══════════════════════════════════════════════════╝
""")
    input("  Press ENTER once logged in > ")

    try:
        driver.get(f"{BASE_URL}/following")
        time.sleep(2)
        print("  ✓ Session active, starting now!")
        return True
    except WebDriverException:
        print("  ✗ Could not reach kick.com/following")
        return False

# ── Follow a single channel ───────────────────────────────
def follow_channel(driver: uc.Chrome, slug: str) -> tuple:
    """
    Navigates to the channel page and clicks Follow.
    Returns (True, reason) or (False, reason).
    """
    url = f"{BASE_URL}/{slug}"
    try:
        driver.get(url)
        time.sleep(random.uniform(1.5, 2.5))

        # Check for 404 / non-existent channel
        if "404" in driver.title or "not found" in driver.title.lower():
            return False, "Channel not found (404)"

        # XPath selectors for the Follow button (most specific first)
        selectors = [
            "//*[@data-testid='follow-button']",
            "//button[normalize-space(text())='Follow']",
            "//button[normalize-space(text())='follow']",
            "//button[contains(@class,'follow') and not(contains(@class,'following')) and not(contains(@class,'unfollow'))]",
            "//button[contains(translate(normalize-space(text()),'FOLLOW','follow'),'follow') and not(contains(translate(normalize-space(text()),'FOLLOWING','following'),'following'))]",
        ]

        button = None
        for sel in selectors:
            try:
                els = driver.find_elements(By.XPATH, sel)
                for el in els:
                    if el.is_displayed() and el.is_enabled():
                        button = el
                        break
                if button:
                    break
            except WebDriverException:
                continue

        # No button found → maybe already following
        if not button:
            already_selectors = [
                "//*[@data-testid='unfollow-button']",
                "//button[contains(translate(normalize-space(text()),'FOLLOWING','following'),'following')]",
                "//button[contains(translate(normalize-space(text()),'UNFOLLOW','unfollow'),'unfollow')]",
            ]
            for sel in already_selectors:
                try:
                    els = driver.find_elements(By.XPATH, sel)
                    if any(el.is_displayed() for el in els):
                        return True, "Already following"
                except WebDriverException:
                    continue
            return False, "Follow button not found"

        # Scroll into view + click
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        time.sleep(0.4)
        try:
            button.click()
        except (WebDriverException, ElementNotInteractableException):
            driver.execute_script("arguments[0].click();", button)

        time.sleep(1.0)
        return True, "OK"

    except WebDriverException as e:
        err = str(e)[:100]
        if "no such window" in err.lower() or "target window already closed" in err.lower():
            return False, "WINDOW_CLOSED"
        if "net::ERR" in err:
            return False, "Network error"
        return False, f"Error: {err}"

# ── Main entry point ──────────────────────────────────────
def main():
    print("""
╔══════════════════════════════════════════════════╗
║   KICK FOLLOW IMPORTER — undetected-chromedriver ║
║   Stealth Chrome · real clicks · no token        ║
╚══════════════════════════════════════════════════╝
""")

    # Channel slugs file
    path = input(f"  File [{FOLLOWS_FILE}] (Enter = default): ").strip() or FOLLOWS_FILE
    slugs = load_slugs(path)
    if not slugs:
        sys.exit(1)

    # Launch Chrome
    print("\n  Launching Chrome (stealth mode)...")
    try:
        driver = setup_driver()
    except Exception as e:
        print(f"  ✗ Could not launch Chrome: {e}")
        sys.exit(1)

    # Manual login
    if not wait_for_login(driver):
        driver.quit()
        sys.exit(1)

    avg   = (DELAY_MIN + DELAY_MAX) / 2
    total = len(slugs)
    print(f"\n  ► {total} channels to follow")
    print(f"  ► Estimated time: ~{int(total * avg / 60)} min")
    print(f"  ► You can leave it running and come back\n")
    input("  Press ENTER to start > ")

    print(f"\n{'─'*52}\n  IMPORT IN PROGRESS\n{'─'*52}")
    success, already, failed = [], [], []

    for i, slug in enumerate(slugs, 1):
        prefix = f"[{i:>4}/{total}]"
        ok, reason = follow_channel(driver, slug)

        if reason == "WINDOW_CLOSED":
            print("  ✗ Chrome window closed — stopping.")
            break

        if ok:
            if "already" in reason.lower():
                print(f"  → {prefix} {slug:<30} Already following")
                already.append(slug)
            else:
                print(f"  ✓ {prefix} {slug:<30} OK")
                success.append(slug)
        else:
            print(f"  ✗ {prefix} {slug:<30} {reason}")
            failed.append({"slug": slug, "reason": reason})

        if i < total:
            time.sleep(round(random.uniform(DELAY_MIN, DELAY_MAX), 1))

    # Summary
    print(f"\n{'─'*52}\n  SUMMARY\n{'─'*52}")
    print(f"  ✓ Followed  : {len(success)}")
    print(f"  → Already   : {len(already)}")
    print(f"  ✗ Failed    : {len(failed)}")

    ts     = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = f"kick_report_{ts}.txt"
    with open(report, "w", encoding="utf-8") as f:
        f.write(f"KICK SELENIUM REPORT — {datetime.now()}\n")
        f.write(f"Followed: {len(success)} | Already: {len(already)} | Failed: {len(failed)}\n\n")
        if success:
            f.write("=== FOLLOWED ===\n")
            for s in success:
                f.write(f"{s}\n")
        if already:
            f.write("\n=== ALREADY FOLLOWING ===\n")
            for s in already:
                f.write(f"{s}\n")
        if failed:
            f.write("\n=== FAILED ===\n")
            for item in failed:
                f.write(f"{item['slug']} → {item['reason']}\n")
    print(f"  ✓ Report saved: {report}")

    input("\n  Press ENTER to close Chrome > ")
    try:
        driver.quit()
    except Exception:
        pass

if __name__ == "__main__":
    main()
