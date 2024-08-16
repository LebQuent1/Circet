import requests
import json
import os

# Configuration de l'URL et du token
base_url = ""
token = ""  # Remplacez par votre token réel
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Chemin vers le fichier JSON transformé (à partir du dossier 'tempo')
current_directory = os.getcwd()
json_file_path = os.path.join(current_directory, 'tempo', 'EXPORT.json')

# Vérification de l'existence du fichier JSON
if not os.path.exists(json_file_path):
    print(f"Le fichier {json_file_path} n'existe pas. Assurez-vous que le fichier est au bon emplacement.")
    exit(1)

# Lecture des données du fichier JSON
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Extraire la liste des interventions à partir des données JSON
interventions = []
for item in data["data"]:
    intervention = {
        "cle": item["Reference"],
        "num_intervention": item["Reference"],
        "jeton": item["Jeton"],
        "date_intervention": item["date_intervention"],
        "heure_intervention": item["heure_intervention"],
        "technicien": item["Techniciens"],
        "departement": item["Departement"]
    }
    interventions.append(intervention)

# Fonction pour envoyer une requête POST
def send_post_request(url, data):
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors de l'envoi de la requête: {e}")
        return None

# Envoi de la requête
response = send_post_request(base_url, interventions)

if response is not None:
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)
else:
    print("Erreur: La requête POST n'a pas pu être envoyée.")

if response and response.status_code == 200:
    print("Les données ont été envoyées avec succès.")
else:
    print("Erreur lors de l'envoi des données.")
