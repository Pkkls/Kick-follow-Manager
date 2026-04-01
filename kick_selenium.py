"""
============================================================
  KICK FOLLOW IMPORTER — undetected-chromedriver
============================================================
  Installation:
      pip install undetected-chromedriver selenium
  Usage:
      python kick_follow_importer.py
============================================================
"""

import os
import re
import sys
import time
import random
import subprocess
from datetime import datetime

# ╔══════════════════════════════════════════════════════╗
# ║                   LANGUAGE SYSTEM                    ║
# ╚══════════════════════════════════════════════════════╝

TRANSLATIONS = {
    "en": {
        "title":            "KICK FOLLOW IMPORTER — undetected-chromedriver",
        "subtitle":         "Stealth Chrome · real clicks · no token needed",
        "select_lang":      "Select language / 言語を選択してください  [1] English  [2] 日本語 > ",
        "missing_deps":     "Missing dependencies: {}",
        "install_cmd":      "Run: pip install {}",
        "file_prompt":      "Channel list file [{}] (Enter = default): ",
        "file_not_found":   "File not found: {}",
        "slugs_loaded":     "{} channels loaded from {}",
        "slugs_after_clean":"After cleaning: {} unique valid channels ({} removed)",
        "no_slugs":         "No valid channels found. Aborting.",
        "launching":        "Launching Chrome (stealth mode)...",
        "chrome_detected":  "Chrome version detected: {}",
        "chrome_unknown":   "Could not detect Chrome version, trying automatically...",
        "chrome_failed":    "Could not launch Chrome: {}",
        "opening_kick":     "Opening kick.com...",
        "login_box": """\
  ╔══════════════════════════════════════════════════╗
  ║  LOG IN TO KICK IN THE BROWSER WINDOW            ║
  ║  Then come back here and press ENTER             ║
  ╚══════════════════════════════════════════════════╝""",
        "login_prompt":     "Press ENTER once logged in > ",
        "session_ok":       "Session active, starting now!",
        "session_fail":     "Could not reach kick.com/following",
        "channels_count":   "{} channels to follow",
        "estimated_time":   "Estimated time: ~{} min",
        "leave_running":    "You can leave it running and come back",
        "start_prompt":     "Press ENTER to start > ",
        "import_header":    "IMPORT IN PROGRESS",
        "already":          "Already following",
        "window_closed":    "Chrome window closed — stopping.",
        "already_label":    "Already following",
        "summary_header":   "SUMMARY",
        "followed":         "Followed  : {}",
        "already_sum":      "Already   : {}",
        "failed_sum":       "Failed    : {}",
        "report_saved":     "Report saved: {}",
        "close_prompt":     "Press ENTER to close Chrome > ",
        "not_found":        "Channel not found (404)",
        "no_button":        "Follow button not found",
        "network_err":      "Network error",
        "error":            "Error: {}",
        "window_err":       "WINDOW_CLOSED",
    },
    "ja": {
        "title":            "KICK フォローインポーター — undetected-chromedriver",
        "subtitle":         "ステルスChrome · 実クリック · トークン不要",
        "select_lang":      "Select language / 言語を選択してください  [1] English  [2] 日本語 > ",
        "missing_deps":     "不足しているパッケージ: {}",
        "install_cmd":      "次を実行してください: pip install {}",
        "file_prompt":      "チャンネルリストファイル [{}] (Enterでデフォルト): ",
        "file_not_found":   "ファイルが見つかりません: {}",
        "slugs_loaded":     "{} チャンネルを {} から読み込みました",
        "slugs_after_clean":"{} 件の有効なチャンネル（{} 件を削除）",
        "no_slugs":         "有効なチャンネルが見つかりませんでした。終了します。",
        "launching":        "Chrome（ステルスモード）を起動しています...",
        "chrome_detected":  "Chromeバージョンを検出しました: {}",
        "chrome_unknown":   "Chromeバージョンを検出できませんでした。自動で試みます...",
        "chrome_failed":    "Chromeを起動できませんでした: {}",
        "opening_kick":     "kick.com を開いています...",
        "login_box": """\
  ╔══════════════════════════════════════════════════╗
  ║  ブラウザでKICKにログインしてください            ║
  ║  完了したらEnterキーを押してください             ║
  ╚══════════════════════════════════════════════════╝""",
        "login_prompt":     "ログイン後、Enterキーを押してください > ",
        "session_ok":       "セッションが有効です。開始します！",
        "session_fail":     "kick.com/following にアクセスできませんでした",
        "channels_count":   "フォローするチャンネル数: {}",
        "estimated_time":   "推定所要時間: 約{}分",
        "leave_running":    "そのまま放置して後で確認することも可能です",
        "start_prompt":     "Enterキーを押して開始 > ",
        "import_header":    "インポート中",
        "already":          "フォロー済み",
        "window_closed":    "Chromeウィンドウが閉じられました — 停止します。",
        "already_label":    "フォロー済み",
        "summary_header":   "結果",
        "followed":         "フォロー完了 : {}",
        "already_sum":      "フォロー済み : {}",
        "failed_sum":       "失敗         : {}",
        "report_saved":     "レポートを保存しました: {}",
        "close_prompt":     "Enterキーを押してChromeを閉じる > ",
        "not_found":        "チャンネルが見つかりません (404)",
        "no_button":        "フォローボタンが見つかりません",
        "network_err":      "ネットワークエラー",
        "error":            "エラー: {}",
        "window_err":       "WINDOW_CLOSED",
    }
}

T = {}  # active translation dict, set in select_language()

def t(key, *args):
    """Return translated string, formatted with args if provided."""
    s = T.get(key, key)
    return s.format(*args) if args else s

def select_language():
    global T
    choice = input(TRANSLATIONS["en"]["select_lang"]).strip()
    T = TRANSLATIONS["ja"] if choice == "2" else TRANSLATIONS["en"]

# ╔══════════════════════════════════════════════════════╗
# ║               DEPENDENCY CHECK                       ║
# ╚══════════════════════════════════════════════════════╝

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
        print(f"  ❌ {t('missing_deps', ', '.join(missing))}")
        print(f"  {t('install_cmd', ' '.join(missing))}")
        sys.exit(1)

# ╔══════════════════════════════════════════════════════╗
# ║                  SLUG PARSER                         ║
# ╚══════════════════════════════════════════════════════╝

def parse_slugs(lines: list) -> list:
    """
    Robust parser that handles:
      - Standard format:  one slug per line
      - Artifact format:  SlugLIVE / Slug / Slug / Slug (pairs with LIVE prefix)
      - Duplicates        (case-insensitive dedup, preserves original casing)
      - Comment lines     (# …)
      - Empty lines
      - Slugs with spaces (e.g. "Ice Poseidon" → skipped, Kick doesn't support spaces)
      - Header lines      ("Followed Channels", "# …")
    """
    seen   = set()
    result = []

    # Noise: lines that are known UI artefacts or headers
    NOISE_PATTERNS = [
        r"^followed\s+channels?$",
        r"^#",
        r"^-+$",
        r"^\s*$",
    ]

    for raw in lines:
        line = raw.strip()

        # Skip empty / comment / known headers
        if not line:
            continue
        if any(re.match(p, line, re.IGNORECASE) for p in NOISE_PATTERNS):
            continue

        # Strip trailing "LIVE" suffix (artifact format)
        cleaned = re.sub(r"LIVE$", "", line).strip()

        # Skip if empty after cleaning
        if not cleaned:
            continue

        # Skip slugs with spaces (invalid Kick URLs)
        if " " in cleaned:
            continue

        # Case-insensitive dedup, keep first occurrence
        key = cleaned.lower()
        if key not in seen:
            seen.add(key)
            result.append(cleaned)

    return result

def load_slugs(path: str) -> list:
    if not os.path.exists(path):
        print(f"  ✗ {t('file_not_found', path)}")
        return []

    raw_lines = open(path, encoding="utf-8").readlines()
    raw_count = sum(1 for l in raw_lines if l.strip() and not l.strip().startswith("#"))

    slugs   = parse_slugs(raw_lines)
    removed = raw_count - len(slugs)

    print(f"  ✓ {t('slugs_loaded', len(raw_lines), path)}")
    print(f"  ✓ {t('slugs_after_clean', len(slugs), removed)}")
    return slugs

# ╔══════════════════════════════════════════════════════╗
# ║              CHROME AUTO-DETECTION                   ║
# ╚══════════════════════════════════════════════════════╝

def get_chrome_version() -> int:
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

# ╔══════════════════════════════════════════════════════╗
# ║                 DRIVER SETUP                         ║
# ╚══════════════════════════════════════════════════════╝

def setup_driver():
    import undetected_chromedriver as uc

    opts = uc.ChromeOptions()
    opts.add_argument("--start-maximized")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")
    opts.add_argument("--disable-popup-blocking")
    # Uncomment to keep session between runs:
    # opts.add_argument("--user-data-dir=C:/kick_chrome_profile")

    version = get_chrome_version()
    if version:
        print(f"  ✓ {t('chrome_detected', version)}")
        driver = uc.Chrome(options=opts, version_main=version)
    else:
        print(f"  ⚠ {t('chrome_unknown')}")
        driver = uc.Chrome(options=opts)

    return driver

# ╔══════════════════════════════════════════════════════╗
# ║                 LOGIN WAIT                           ║
# ╚══════════════════════════════════════════════════════╝

def wait_for_login(driver) -> bool:
    from selenium.common.exceptions import WebDriverException

    print(f"\n  → {t('opening_kick')}")
    driver.get("https://kick.com")
    time.sleep(3)

    print(f"\n{t('login_box')}\n")
    input(f"  {t('login_prompt')}")

    try:
        driver.get("https://kick.com/following")
        time.sleep(2)
        print(f"  ✓ {t('session_ok')}")
        return True
    except WebDriverException:
        print(f"  ✗ {t('session_fail')}")
        return False

# ╔══════════════════════════════════════════════════════╗
# ║                FOLLOW CHANNEL                        ║
# ╚══════════════════════════════════════════════════════╝

def follow_channel(driver, slug: str) -> tuple:
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import WebDriverException, ElementNotInteractableException

    url = f"https://kick.com/{slug}"
    try:
        driver.get(url)
        time.sleep(random.uniform(1.5, 2.5))

        if "404" in driver.title or "not found" in driver.title.lower():
            return False, t("not_found")

        # Follow button selectors — most specific first
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

        # No follow button → check if already following
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
                        return True, t("already")
                except WebDriverException:
                    continue
            return False, t("no_button")

        # Scroll + click
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        time.sleep(0.4)
        try:
            button.click()
        except (WebDriverException, ElementNotInteractableException):
            driver.execute_script("arguments[0].click();", button)

        time.sleep(1.0)
        return True, "OK"

    except Exception as e:
        err = str(e)[:100]
        if "no such window" in err.lower() or "target window already closed" in err.lower():
            return False, t("window_err")
        if "net::ERR" in err:
            return False, t("network_err")
        return False, t("error", err)

# ╔══════════════════════════════════════════════════════╗
# ║                    MAIN                              ║
# ╚══════════════════════════════════════════════════════╝

FOLLOWS_FILE = "kick_follows.txt"
DELAY_MIN    = 3.0
DELAY_MAX    = 6.0

def main():
    # Language selection
    select_language()

    print(f"""
╔══════════════════════════════════════════════════╗
║  {t('title'):<48}  ║
║  {t('subtitle'):<48}  ║
╚══════════════════════════════════════════════════╝
""")

    # Dependency check
    check_dependencies()

    # Load slugs
    path  = input(f"  {t('file_prompt', FOLLOWS_FILE)}").strip() or FOLLOWS_FILE
    slugs = load_slugs(path)
    if not slugs:
        print(f"  ✗ {t('no_slugs')}")
        sys.exit(1)

    # Launch Chrome
    print(f"\n  {t('launching')}")
    try:
        driver = setup_driver()
    except Exception as e:
        print(f"  ✗ {t('chrome_failed', e)}")
        sys.exit(1)

    # Login
    if not wait_for_login(driver):
        driver.quit()
        sys.exit(1)

    avg   = (DELAY_MIN + DELAY_MAX) / 2
    total = len(slugs)
    print(f"\n  ► {t('channels_count', total)}")
    print(f"  ► {t('estimated_time', int(total * avg / 60))}")
    print(f"  ► {t('leave_running')}\n")
    input(f"  {t('start_prompt')}")

    print(f"\n{'─'*52}\n  {t('import_header')}\n{'─'*52}")
    success, already, failed = [], [], []

    for i, slug in enumerate(slugs, 1):
        prefix = f"[{i:>4}/{total}]"
        ok, reason = follow_channel(driver, slug)

        if reason == t("window_err"):
            print(f"  ✗ {t('window_closed')}")
            break

        if ok:
            if reason != "OK":
                print(f"  → {prefix} {slug:<30} {t('already_label')}")
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
    print(f"\n{'─'*52}\n  {t('summary_header')}\n{'─'*52}")
    print(f"  ✓ {t('followed', len(success))}")
    print(f"  → {t('already_sum', len(already))}")
    print(f"  ✗ {t('failed_sum', len(failed))}")

    ts     = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = f"kick_report_{ts}.txt"
    with open(report, "w", encoding="utf-8") as f:
        f.write(f"KICK REPORT — {datetime.now()}\n")
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

    print(f"  ✓ {t('report_saved', report)}")
    input(f"\n  {t('close_prompt')}")
    try:
        driver.quit()
    except Exception:
        pass

if __name__ == "__main__":
    main()
