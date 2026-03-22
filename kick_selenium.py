"""
============================================================
  KICK FOLLOW IMPORTER — Selenium (vrai navigateur Chrome)
============================================================
  Installation :
      pip install selenium webdriver-manager
  Lancement :
      python kick_selenium.py

  Le script ouvre Chrome, tu te connectes manuellement,
  puis il follow toutes les chaînes automatiquement.
============================================================
"""

import time
import os
import sys
import random
from datetime import datetime

FOLLOWS_FILE = "kick_follows.txt"
DELAY_MIN    = 3.0   # secondes entre chaque follow
DELAY_MAX    = 6.0
BASE_URL     = "https://kick.com"

# ─────────────────────────────────────────────
def load_slugs(path):
    if not os.path.exists(path):
        print(f"  ✗ Fichier introuvable : {path}")
        return []
    slugs = [l.strip() for l in open(path, encoding="utf-8")
             if l.strip() and not l.strip().startswith("#")]
    print(f"  ✓ {len(slugs)} chaînes chargées depuis {path}")
    return slugs

# ─────────────────────────────────────────────
def setup_driver():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    opts = Options()
    # Pas de headless → vrai navigateur visible pour se connecter
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    # Garder le profil Chrome ouvert entre les runs (optionnel)
    # opts.add_argument("--user-data-dir=C:/kick_chrome_profile")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)

    # Cacher que c'est Selenium
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver

# ─────────────────────────────────────────────
def wait_for_login(driver):
    """Ouvre kick.com et attend que l'utilisateur soit connecté."""
    print("\n  → Ouverture de kick.com...")
    driver.get(BASE_URL)
    time.sleep(2)

    print("""
  ╔══════════════════════════════════════════════════╗
  ║  CONNECTE-TOI À KICK DANS LE NAVIGATEUR          ║
  ║  Puis reviens ici et appuie sur ENTRÉE            ║
  ╚══════════════════════════════════════════════════╝
""")
    input("  Appuie sur ENTRÉE une fois connecté > ")

    # Vérifier que la session est active
    driver.get(f"{BASE_URL}/following")
    time.sleep(2)
    if "following" in driver.current_url or "kick.com" in driver.current_url:
        print("  ✓ Session détectée, on commence !")
        return True
    print("  ⚠ Impossible de vérifier la session, on continue quand même.")
    return True

# ─────────────────────────────────────────────
def follow_channel(driver, slug):
    """
    Navigue sur la page du channel et clique sur Follow.
    Retourne (True, raison) ou (False, raison).
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException

    url = f"{BASE_URL}/{slug}"
    try:
        driver.get(url)
        time.sleep(random.uniform(1.5, 2.5))

        # Sélecteurs possibles pour le bouton Follow sur Kick
        selectors = [
            "//button[contains(translate(text(),'FOLLOW','follow'),'follow') and not(contains(translate(text(),'FOLLOWING','following'),'following'))]",
            "//button[contains(@class,'follow') and not(contains(@class,'following'))]",
            "//*[@data-testid='follow-button']",
            "//button[normalize-space()='Follow']",
            "//button[normalize-space()='follow']",
        ]

        button = None
        for sel in selectors:
            try:
                elements = driver.find_elements(By.XPATH, sel)
                for el in elements:
                    txt = el.text.strip().lower()
                    if txt in ("follow", "suivre", "s'abonner") or "follow" in el.get_attribute("class").lower():
                        button = el
                        break
                if button:
                    break
            except Exception:
                continue

        if not button:
            # Vérifier si déjà suivi
            try:
                following_indicators = driver.find_elements(
                    By.XPATH,
                    "//button[contains(translate(text(),'FOLLOWING','following'),'following') or contains(translate(text(),'UNFOLLOW','unfollow'),'unfollow')]"
                )
                if following_indicators:
                    return True, "Déjà followé"
            except Exception:
                pass
            return False, "Bouton Follow introuvable"

        # Scroll et clic
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        time.sleep(0.5)
        try:
            button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", button)

        time.sleep(1)
        return True, "OK"

    except Exception as e:
        err = str(e)[:80]
        if "no such window" in err.lower():
            return False, "FENETRE_FERMEE"
        return False, f"Erreur: {err}"

# ─────────────────────────────────────────────
def main():
    print("""
╔══════════════════════════════════════════════════╗
║     KICK FOLLOW IMPORTER — Selenium v1.0         ║
║     Vrai Chrome, vrais clics, zéro token         ║
╚══════════════════════════════════════════════════╝
""")

    # Vérif dépendances
    try:
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        print("  ❌ Lance d'abord :")
        print("       pip install selenium webdriver-manager")
        sys.exit(1)

    # Charger la liste
    path = input(f"  Fichier [{FOLLOWS_FILE}] (Entrée = défaut) : ").strip() or FOLLOWS_FILE
    slugs = load_slugs(path)
    if not slugs:
        return

    # Lancer Chrome
    print("\n  Lancement de Chrome...")
    try:
        driver = setup_driver()
    except Exception as e:
        print(f"  ✗ Impossible de lancer Chrome : {e}")
        print("  Assure-toi que Chrome est installé.")
        sys.exit(1)

    # Connexion manuelle
    if not wait_for_login(driver):
        driver.quit()
        return

    avg = (DELAY_MIN + DELAY_MAX) / 2
    total = len(slugs)
    print(f"\n  ► {total} chaînes à follow")
    print(f"  ► Durée estimée : ~{int(total*avg/60)} min")
    print(f"  ► Tu peux laisser tourner et revenir\n")
    input("  Appuie sur ENTRÉE pour démarrer > ")

    # Import
    print(f"\n{'─'*52}\n  IMPORT EN COURS\n{'─'*52}")
    success, already, failed = [], [], []

    for i, slug in enumerate(slugs, 1):
        prefix = f"[{i:>4}/{total}]"
        ok, reason = follow_channel(driver, slug)

        if reason == "FENETRE_FERMEE":
            print(f"  ✗ Fenêtre Chrome fermée. Arrêt.")
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
            wait = round(random.uniform(DELAY_MIN, DELAY_MAX), 1)
            time.sleep(wait)

    # Résumé
    print(f"\n{'─'*52}\n  RÉSUMÉ\n{'─'*52}")
    print(f"  ✓ Followés : {len(success)}")
    print(f"  → Déjà     : {len(already)}")
    print(f"  ✗ Échecs   : {len(failed)}")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = f"kick_report_{ts}.txt"
    with open(report, "w", encoding="utf-8") as f:
        f.write(f"KICK SELENIUM REPORT — {datetime.now()}\n")
        f.write(f"Succès: {len(success)} | Déjà: {len(already)} | Échecs: {len(failed)}\n\n")
        if failed:
            f.write("=== ÉCHECS ===\n")
            for item in failed:
                f.write(f"{item['slug']} → {item['reason']}\n")
    print(f"  ✓ Rapport : {report}")

    input("\n  Appuie sur ENTRÉE pour fermer Chrome > ")
    driver.quit()

if __name__ == "__main__":
    main()
