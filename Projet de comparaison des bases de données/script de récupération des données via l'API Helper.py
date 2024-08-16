import requests
import json
from datetime import datetime

# URL de l'API
url = ""

# Token d'authentification (remplacez par votre token réel)
token = ""

# En-têtes de la requête
headers = {
    "Apikey": token,
    "Content-Type": "application/json"
}

# Année de début
start_year = 2018
# Année actuelle
current_year = datetime.now().year

# Liste pour stocker les noms de fichiers JSON téléchargés
json_files = []

# Itérer sur chaque année depuis 2018 jusqu'à l'année en cours
for year in range(start_year, current_year + 1):
    for half in range(2):  # Deux moitiés de l'année
        if half == 0:
            from_date = f"{year}-01-01 00:00:00"
            to_date = f"{year}-06-30 23:59:59"
            half_label = "H1"  # Première moitié de l'année
        else:
            from_date = f"{year}-07-01 00:00:00"
            to_date = f"{year}-12-31 23:59:59"
            half_label = "H2"  # Deuxième moitié de l'année

        # Charge utile de la requête (payload)
        payload = {
            "date": {
                "from": from_date,
                "to": to_date
            },
            "type_date": "creation",  # Spécifier que le filtre est sur la date de création
            "types-ticket": ["Gestion de Litiges", "Malfaçons OI"],  # Liste des types de ticket
            "fields": ["Référence Ticket", "autres_champs"]  # Ajouter les champs nécessaires
        }

        # Faire la requête POST avec le payload JSON et les en-têtes
        response = requests.post(url, json=payload, headers=headers)

        # Vérifier le statut de la réponse
        if response.status_code == 200:
            # Extraire les données au format JSON
            data = response.json()

            # Nom du fichier de sortie
            file_name = f"tickets_response_{year}_{half_label}.json"
            
            # Enregistrer les données dans un fichier JSON
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=4)  # indent=4 pour un formatage lisible

            print(f"Les données pour l'année {year} {half_label} ont été enregistrées dans le fichier '{file_name}'.")

            # Ajouter le nom du fichier à la liste
            json_files.append(file_name)
        else:
            print(f"Échec de la requête pour l'année {year} {half_label} avec le statut {response.status_code}")
            print(response.text)

# Combiner tous les fichiers JSON en un seul fichier JSON
combined_data = []

for file_name in json_files:
    with open(file_name, 'r') as f:
        data = json.load(f)
        # Supposons que les données sont une liste d'éléments
        combined_data.extend(data)

# Enregistrer les données combinées dans un fichier JSON unique
with open('combined_tickets.json', 'w') as f:
    json.dump(combined_data, f, indent=4)  # indent=4 pour un formatage lisible

print("Tous les fichiers JSON ont été combinés dans le fichier 'combined_tickets.json'.")
