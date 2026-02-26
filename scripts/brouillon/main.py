import os
from supabase import create_client, Client

# --- TES INFOS DE CONNEXION ---
URL = "https://qaalcibonrfizpwbwcyf.supabase.co"
KEY = "sb_publishable_eH3iTHselgi4u01FcK112Q_dPSaSn3b"

# On initialise la connexion au serveur
supabase: Client = create_client(URL, KEY)

print("--- 🛒 INTERFACE AJOUT PROMO BONBO ---")

# --- ON RÉCUPÈRE TES INFOS DANS WARP ---
nom_pdt = input("Nom du produit (ex: Pâtes) : ")
p_avant = float(input("Prix habituel en € (ex: 1.85) : "))
p_apres = float(input("Prix promo en € (ex: 1.20) : "))
mag = input("Magasin (ex: Leclerc Chartrons) : ")

# --- ON PRÉPARE LE PAQUET POUR LE CLOUD ---
data = {
    "nom": nom_pdt,
    "prix_avant": p_avant,
    "prix_apres": p_apres,
    "magasin": mag
}

# --- ENVOI VERS SUPABASE ---
try:
    response = supabase.table("promotions").insert(data).execute()
    print("\n✅ C'est en ligne ! La promo a été enregistrée sur ton Supabase.")
except Exception as e:
    print(f"\n❌ Erreur lors de l'envoi : {e}")
