# On crée une liste qui contient plusieurs dictionnaires (produits)
promos_du_jour = [
    {"nom": "Pâtes Penne", "prix": 1.20, "reduc": 35, "magasin": "Leclerc"},
    {"nom": "Lait d'avoine", "prix": 1.50, "reduc": 10, "magasin": "Lidl"},
    {"nom": "Steak Haché", "prix": 3.50, "reduc": 50, "magasin": "Carrefour"},
    {"nom": "Pommes 1kg", "prix": 2.10, "reduc": 20, "magasin": "Auchan"},
    {"nom": "Nutella", "prix": 4.50, "reduc": 60, "magasin": "Monoprix"},]

# --- ACTION 1 : Trier par les promos les plus intéressantes ---
# On dit à Python de trier la liste en regardant la clé "reduc"
# 'reverse=True' permet d'avoir la plus grosse réduction en premier
promos_triees = sorted(promos_du_jour, key=lambda x: x['reduc'], reverse=True)

print("--- CLASSEMENT DES MEILLEURES PROMOS BONBO ---")

for p in promos_triees:
    print(f"[{p['reduc']}%] {p['nom']} à {p['prix']}€ ({p['magasin']})")

# --- ACTION 2 : Rechercher un produit ---
recherche = "Pâtes"
print(f"\n--- RÉSULTAT RECHERCHE POUR : '{recherche}' ---")

for p in promos_du_jour:
    if recherche.lower() in p['nom'].lower():
        print(f"Trouvé : {p['nom']} est en promo à -{p['reduc']}% chez {p['magasin']}")

        # --- ÉTAPE 1 : Ta base de données de promos ---
promos_du_jour = [
    {"nom": "Pâtes Penne", "prix": 1.20, "reduc": 35, "magasin": "Leclerc"},
    {"nom": "Lait d'avoine", "prix": 1.50, "reduc": 10, "magasin": "Lidl"},
    {"nom": "Steak Haché", "prix": 3.50, "reduc": 50, "magasin": "Carrefour"},
    {"nom": "Pommes 1kg", "prix": 2.10, "reduc": 20, "magasin": "Auchan"},
    {"nom": "Riz Basmati", "prix": 1.80, "reduc": 40, "magasin": "Leclerc"},
    {"nom": "Oeufs x12", "prix": 2.50, "reduc": 15, "magasin": "Lidl"},
]

# --- ÉTAPE 2 : Créer un Panier Type "Éco-Protéiné" ---
# On va créer une liste vide et y ajouter des produits spécifiques
panier_etudiant = []
budget_max = 5.0
total_actuel = 0.0

# On trie d'abord par meilleure réduction
promos_triees = sorted(promos_du_jour, key=lambda x: x['reduc'], reverse=True)

print(f"--- GÉNÉRATION D'UN PANIER TYPE (Budget: {budget_max}€) ---")

for p in promos_triees:
    # Si on a encore assez de budget pour ajouter ce produit
    if total_actuel + p['prix'] <= budget_max:
        panier_etudiant.append(p)
        total_actuel += p['prix']

# --- ÉTAPE 3 : Affichage du résultat ---
for item in panier_etudiant:
    print(f"✅ AJOUTÉ : {item['nom']} ({item['prix']}€) - Promo de {item['reduc']}%")

print(f"\nTOTAL DU PANIER : {total_actuel:.2f}€")
print(f"ARGENT RESTANT : {(budget_max - total_actuel):.2f}€")
