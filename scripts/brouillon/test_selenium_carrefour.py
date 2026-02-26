from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from supabase import create_client, Client
import time

# --- CONNEXION SUPABASE ---
URL = "https://qaalcibonrfizpwbwcyf.supabase.co"
KEY = "sb_publishable_eH3iTHselgi4u01FcK112Q_dPSaSn3b"
supabase: Client = create_client(URL, KEY)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    print("--- 🚀 BONBO : NETTOYAGE NUCLÉAIRE ---")
    driver.get("https://www.carrefour.fr/promotions")
    time.sleep(7) 

   # --- LE NETTOYAGE NUCLÉAIRE V2 ---
    nettoyage_ultime = """
    // 1. On supprime par les IDs et classes connues
    var selectors = ['.pwa-footer', '.header-promotion-ribbon', '#onetrust-banner-sdk', '.onboarding-modal'];
    selectors.forEach(s => document.querySelectorAll(s).forEach(el => el.remove()));

    // 2. LA MÉTHODE RADICALE : On cherche tous les éléments qui contiennent "OFFERTS" ou "20€"
    var allDivs = document.querySelectorAll('div, section, aside');
    allDivs.forEach(div => {
        if (div.innerText && (div.innerText.includes('OFFERTS') || div.innerText.includes('20€'))) {
            div.remove();
        }
    });

    // 3. On enlève les fonds grisés (modals)
    document.querySelectorAll('.v-modal, .backdrop').forEach(el => el.remove());
    document.body.style.overflow = 'auto';
    """
    driver.execute_script(nettoyage_ultime)
    print("✅ Bandeau rose pulvérisé.")

    # Défilement
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(2)

    # --- EXTRACTION ET TRI ---
    print("Analyse des produits...")
    elements = driver.find_elements(By.XPATH, "//h2 | //h3 | //strong")
    
    promos_a_sauver = []
    
    # On définit des mots-clés "poubelle" pour nettoyer la liste
    poubelle = ["aide", "contact", "rappel", "bonus", "achat", "description", "catalogue", "communauté", "économies", "remise"]

    for el in elements:
        nom = el.text.strip()
        # On ne garde que ce qui ressemble à un vrai produit
        if 8 < len(nom) < 50 and not any(mot in nom.lower() for mot in poubelle):
            # On vérifie qu'on n'a pas déjà ajouté ce nom
            if nom not in [p['nom'] for p in promos_a_sauver]:
                promos_a_sauver.append({
                    "nom": nom,
                    "magasin": "Carrefour City",
                    "prix_avant": 0, # On pourra extraire les prix après
                    "prix_apres": 0
                })

    print(f"\n--- 📦 ENVOI DE {len(promos_a_sauver)} PRODUITS VERS SUPABASE ---")
    
    for p in promos_a_sauver:
        try:
            supabase.table("promotions").insert(p).execute()
            print(f"✅ Enregistré : {p['nom']}")
        except Exception as e:
            print(f"❌ Erreur pour {p['nom']} : {e}")

except Exception as e:
    print(f"❌ Erreur générale : {e}")

finally:
    print("\n--- OPÉRATION TERMINÉE ---")
    driver.quit()