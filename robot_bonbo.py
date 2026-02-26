from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from supabase import create_client, Client
import time
import re 

# --- CONNEXION SUPABASE ---
URL = "https://qaalcibonrfizpwbwcyf.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFhYWxjaWJvbnJmaXpwd2J3Y3lmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIxMDMzMTYsImV4cCI6MjA4NzY3OTMxNn0.1BjwjdDn-ONwxD8LnUHFj4xLI-XvWzenBYXP43kLGTU"
supabase: Client = create_client(URL, KEY)

# --- 1. LE CERVEAU ---
def robot_scanner(enseigne, url, selecteur_carte, script_cookies):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new') # Rend Chrome invisible pour le serveur
    options.add_argument('--no-sandbox') # Sécurité pour les serveurs Linux
    options.add_argument('--disable-dev-shm-usage') # Évite les crashs de mémoire
    options.add_argument('window-size=1920x1080') # Simule un grand écran
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10) 

    try:
        supabase.table("promotions").delete().eq("magasin", enseigne).execute()
        print(f"--- 🚀 SCAN : {enseigne} ---")
        driver.get(url)

        # --- 1. COOKIES ---
        if enseigne == "Lidl":
            time.sleep(2)
            try:
                actions = ActionChains(driver)
                for _ in range(6): 
                    actions.send_keys(Keys.TAB).perform()
                    time.sleep(0.1)
                actions.send_keys(Keys.ENTER).perform()
                print("✅ Cookies évacués.")
            except: pass
        elif script_cookies:
            try: driver.execute_script(script_cookies)
            except: pass

        # --- 2. SCROLL & MULTIPLES CLICS ---
        if enseigne == "Lidl":
            print("🖱️ Descente et traque des boutons 'Charger plus'...")
            for i in range(30): 
                driver.execute_script("window.scrollBy(0, 400);")
                time.sleep(1.5) 
                
                try:
                    boutons = driver.find_elements(By.XPATH, "//button[contains(., 'Charger')]")
                    for bouton in boutons:
                        if bouton.is_displayed():
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", bouton)
                            time.sleep(1)
                            driver.execute_script("arguments[0].click();", bouton)
                            print(f"🔄 Bouton cliqué (Saut {i}/30) ! Chargement de la suite...")
                            time.sleep(3) 
                except:
                    pass 
        else:
            print("🖱️ Déroulement de la page Carrefour...")
            driver.execute_script("window.scrollBy(0, 1500);")
            time.sleep(2)

        driver.execute_script("window.scrollBy(0, 300);")

        # --- 3. EXTRACTION JS ---
        print(f"🔍 Analyse profonde du DOM pour {enseigne}...")
        
        script_js = """
        let results = [];
        let elements = document.querySelectorAll('article, .plp-item, [data-qa="product-grid-item"], .n-catalog-grid__item');
        
        if (elements.length === 0) {
            elements = document.querySelectorAll('div');
        }

        elements.forEach(el => {
            let txt = el.innerText;
            if (txt && txt.includes('€') && txt.length > 15 && txt.length < 400) {
                results.push(txt);
            }
        });
        return results;
        """
        raw_items = driver.execute_script(script_js)
        items_valides = list(set(raw_items))
        print(f"📊 {len(items_valides)} données brutes trouvées, début du nettoyage...")

        # --- 4. PARSING (Le super filtre ajusté pour Carrefour & Lidl) ---
        mots_interdits = [
            "avis pour", "note moyenne", "profiter", "cliquer", " / l", " / u", 
            "description", "7 jours", "supermarché", "l'unité", "produit", "manger", "bouger", 
            "charger", "maison", "aménagement", "bricolage", "santé", "le kg", "au kg", "retrouvez",
            "soit la", "soit le", 
            "acheter", "ajouter" # <-- NOUVEAU : On vire les boutons de Carrefour
        ]

        for texte in items_valides:
            try:
                lignes = texte.split('\n')
                nom, promo, prix_unit = "", "PROMO", ""

                for l in lignes:
                    l_c = l.strip()
                    if not l_c: continue
                    
                    if "|" in l_c or l_c.count(".") >= 2: continue
                    if re.match(r'^[\d\s,\./]+(g|kg|ml|l|cl)$', l_c.lower()): continue
                    
                    # NOUVEAU : On capte les promos Carrefour ("PRENEZ EN 2...") et on harmonise la casse
                    l_upper = l_c.upper()
                    if "%" in l_c or "ÈME" in l_upper or "OFFRE" in l_upper or "FLASH" in l_upper or "ÉCONOMIES" in l_upper or "ACHETÉ" in l_upper or "PRENEZ EN 2" in l_upper: 
                        promo = l_c
                    elif "€ /" in l_c.lower() or "/ kg" in l_c.lower(): 
                        prix_unit = l_c
                    elif len(l_c) > 4 and not any(m in l_c.lower() for m in mots_interdits) and "€" not in l_c: 
                        nom = l_c

                if nom and len(nom) < 80:
                    affichage = f"[{promo}] {nom}"
                    if prix_unit: affichage += f" ({prix_unit})"
                    
                    supabase.table("promotions").insert({"nom": affichage, "magasin": enseigne, "prix_apres": 0, "prix_avant": 0}).execute()
                    print(f"✅ {enseigne} -> {affichage[:60]}...") 
            except: continue

    finally:
        driver.quit()

# --- 2. RÉGLAGES POINTUS ---
config_carrefour = {
    "enseigne": "Carrefour City",
    "url": "https://www.carrefour.fr/promotions",
    "selecteur_carte": "",
    "script_cookies": "document.querySelector('#onetrust-accept-btn-handler')?.click();"
}

config_lidl = {
    "enseigne": "Lidl",
    "url": "https://www.lidl.fr/c/manger-boire/s10068374", 
    "selecteur_carte": "", 
    "script_cookies": None 
}

# --- 3. LANCEMENT ---
robot_scanner(**config_carrefour)
robot_scanner(**config_lidl)