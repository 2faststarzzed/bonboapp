import requests
from bs4 import BeautifulSoup

# On va tester sur un site fait pour l'entraînement au scraping
url = "https://www.scrapethissite.com/pages/simple/"

print(f"--- 🕸️ TEST DE RÉCUPÉRATION SUR : {url} ---")

# 1. On télécharge la page
reponse = requests.get(url)
# 2. On transforme le code HTML en 'soupe' exploitable
soup = BeautifulSoup(reponse.text, 'html.parser')

# 3. On cherche tous les blocs qui contiennent des pays (pour l'exemple)
pays_blocs = soup.find_all('div', class_='col-md-4 country')

for bloc in pays_blocs[:5]: # On en prend juste 5 pour tester
    nom = bloc.find('h3', class_='country-name').text.strip()
    capitale = bloc.find('span', class_='country-capital').text.strip()
    print(f"Trouvé : {nom} (Capitale : {capitale})")