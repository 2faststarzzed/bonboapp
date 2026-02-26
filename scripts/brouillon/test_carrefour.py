import requests
from bs4 import BeautifulSoup

# URL des promos Carrefour
url = "https://www.carrefour.fr/promotions"

# On ajoute un "User-Agent" : on fait croire au site qu'on est un vrai navigateur (Chrome)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

print(f"--- 🛒 TENTATIVE SUR CARREFOUR ---")

try:
    reponse = requests.get(url, headers=headers)
    if reponse.status_code == 200:
        print("✅ Accès autorisé !")
        soup = BeautifulSoup(reponse.text, 'html.parser')
        print("Titre de la page :", soup.title.text)
    else:
        print(f"❌ Accès refusé (Code d'erreur : {reponse.status_code})")
except Exception as e:
    print(f"❌ Erreur : {e}")