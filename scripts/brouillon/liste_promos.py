from supabase import create_client, Client

URL = "https://qaalcibonrfizpwbwcyf.supabase.co"
KEY = "sb_publishable_eH3iTHselgi4u01FcK112Q_dPSaSn3b"
supabase: Client = create_client(URL, KEY)

print("--- 🛒 RÉPERTOIRE BONBO PAR MAGASIN ---")

response = supabase.table("promotions").select("*").execute()
promos = response.data

# On crée un dictionnaire pour regrouper par magasin
magasins = {}

for p in promos:
    mag = p['magasin']
    if mag not in magasins:
        magasins[mag] = []
    magasins[mag].append(p['nom'])

# Affichage propre
for mag, produits in magasins.items():
    print(f"\n📍 {mag.upper()} ({len(produits)} promos)")
    print("-" * 30)
    for produit in produits[:15]: # On affiche les 15 premiers de chaque
        print(f"• {produit}")