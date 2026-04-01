"""
============================================================
  KICK FOLLOW IMPORTER — undetected-chromedriver
============================================================
  Installation :
      pip install undetected-chromedriver selenium
  Lancement :
      python kick_selenium_uc.py
============================================================
"""

import os
import re
import sys
import time
import random
import subprocess
from datetime import datetime

# ── Vérification des dépendances au démarrage ────────────
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
        print(f"  ❌ Dépendances manquantes : {', '.join(missing)}")
        print(f"  Lance : pip install {' '.join(missing)}")
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

# ── Détection automatique de la version Chrome ───────────
def get_chrome_version() -> int:
    """Détecte la version majeure de Chrome installée sur le système."""
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
        # Fallback registre Windows
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

# ── Chargement de la liste des slugs ─────────────────────
def load_slugs(path: str) -> list:
    if not os.path.exists(path):
        print(f"  ✗ Fichier introuvable : {path}")
        return []
    slugs = [
        l.strip() for l in open(path, encoding="utf-8")
        if l.strip() and not l.strip().startswith("#")
    ]
    print(f"  ✓ {len(slugs)} chaînes chargées depuis {path}")
    return slugs

# ── Initialisation du driver ─────────────────────────────
def setup_driver() -> uc.Chrome:
    opts = uc.ChromeOptions()
    opts.add_argument("--start-maximized")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")
    opts.add_argument("--disable-popup-blocking")
    # Optionnel : profil persistant (décommenter pour garder la session)
    # opts.add_argument("--user-data-dir=C:/kick_chrome_profile")

    version = get_chrome_version()
    if version:
        print(f"  ✓ Chrome version détectée : {version}")
        driver = uc.Chrome(options=opts, version_main=version)
    else:
        print("  ⚠ Version Chrome non détectée, tentative automatique...")
        driver = uc.Chrome(options=opts)

    return driver

# ── Attente de connexion manuelle ─────────────────────────
def wait_for_login(driver: uc.Chrome) -> bool:
    print("\n  → Ouverture de kick.com...")
    driver.get(BASE_URL)
    time.sleep(3)

    print("""
  ╔══════════════════════════════════════════════════╗
  ║  CONNECTE-TOI À KICK DANS LE NAVIGATEUR          ║
  ║  Puis reviens ici et appuie sur ENTRÉE            ║
  ╚══════════════════════════════════════════════════╝
""")
    input("  Appuie sur ENTRÉE une fois connecté > ")

    try:
        driver.get(f"{BASE_URL}/following")
        time.sleep(2)
        print("  ✓ Session active, on commence !")
        return True
    except WebDriverException:
        print("  ✗ Impossible d'accéder à kick.com/following")
        return False

# ── Follow d'un channel ───────────────────────────────────
def follow_channel(driver: uc.Chrome, slug: str) -> tuple:
    """
    Navigue sur la page du channel et clique sur Follow.
    Retourne (True, raison) ou (False, raison).
    """
    url = f"{BASE_URL}/{slug}"
    try:
        driver.get(url)
        time.sleep(random.uniform(1.5, 2.5))

        # Vérification 404 / chaîne inexistante
        if "404" in driver.title or "not found" in driver.title.lower():
            return False, "Chaîne introuvable (404)"

        # Sélecteurs XPath du bouton Follow (du plus précis au plus large)
        selectors = [
            "//*[@data-testid='follow-button']",
            "//button[normalize-space(text())='Follow']",
            "//button[normalize-space(text())='follow']",
            "//button[normalize-space(text())='Suivre']",
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

        # Pas de bouton → peut-être déjà followé
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
                        return True, "Déjà followé"
                except WebDriverException:
                    continue
            return False, "Bouton Follow introuvable"

        # Scroll + clic
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
            return False, "FENETRE_FERMEE"
        if "net::ERR" in err:
            return False, "Erreur réseau"
        return False, f"Erreur: {err}"

# ── Point d'entrée ────────────────────────────────────────
def main():
    print("""
╔══════════════════════════════════════════════════╗
║   KICK FOLLOW IMPORTER — undetected-chromedriver ║
║   Chrome furtif · vrais clics · zéro token       ║
╚══════════════════════════════════════════════════╝
""")

    # Fichier de slugs
    path = input(f"  Fichier [{FOLLOWS_FILE}] (Entrée = défaut) : ").strip() or FOLLOWS_FILE
    slugs = load_slugs(path)
    if not slugs:
        sys.exit(1)

    # Lancement Chrome
    print("\n  Lancement de Chrome (furtif)...")
    try:
        driver = setup_driver()
    except Exception as e:
        print(f"  ✗ Impossible de lancer Chrome : {e}")
        sys.exit(1)

    # Connexion manuelle
    if not wait_for_login(driver):
        driver.quit()
        sys.exit(1)

    avg   = (DELAY_MIN + DELAY_MAX) / 2
    total = len(slugs)
    print(f"\n  ► {total} chaînes à follow")
    print(f"  ► Durée estimée : ~{int(total * avg / 60)} min")
    print(f"  ► Tu peux laisser tourner et revenir\n")
    input("  Appuie sur ENTRÉE pour démarrer > ")

    print(f"\n{'─'*52}\n  IMPORT EN COURS\n{'─'*52}")
    success, already, failed = [], [], []

    for i, slug in enumerate(slugs, 1):
        prefix = f"[{i:>4}/{total}]"
        ok, reason = follow_channel(driver, slug)

        if reason == "FENETRE_FERMEE":
            print("  ✗ Fenêtre Chrome fermée — arrêt.")
            break

        if ok:
            if "déjà" in reason.lower():
                print(f"  → {prefix} {slug:<30} Déjà followé")
                already.append(slug)
            else:
                print(f"  ✓ {prefix} {slug:<30} OK")
                success.append(slug)
        else:
            print(f"  ✗ {prefix} {slug:<30} {reason}")
            failed.append({"slug": slug, "reason": reason})

        if i < total:
            time.sleep(round(random.uniform(DELAY_MIN, DELAY_MAX), 1))

    # Résumé
    print(f"\n{'─'*52}\n  RÉSUMÉ\n{'─'*52}")
    print(f"  ✓ Followés : {len(success)}")
    print(f"  → Déjà     : {len(already)}")
    print(f"  ✗ Échecs   : {len(failed)}")

    ts     = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = f"kick_report_{ts}.txt"
    with open(report, "w", encoding="utf-8") as f:
        f.write(f"KICK SELENIUM REPORT — {datetime.now()}\n")
        f.write(f"Succès: {len(success)} | Déjà: {len(already)} | Échecs: {len(failed)}\n\n")
        if success:
            f.write("=== SUCCÈS ===\n")
            for s in success:
                f.write(f"{s}\n")
        if already:
            f.write("\n=== DÉJÀ FOLLOWÉS ===\n")
            for s in already:
                f.write(f"{s}\n")
        if failed:
            f.write("\n=== ÉCHECS ===\n")
            for item in failed:
                f.write(f"{item['slug']} → {item['reason']}\n")
    print(f"  ✓ Rapport sauvegardé : {report}")

    input("\n  Appuie sur ENTRÉE pour fermer Chrome > ")
    try:
        driver.quit()
    except Exception:
        pass

if __name__ == "__main__":
    main()
