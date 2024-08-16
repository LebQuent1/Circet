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





# Chemin du dossier contenant les dossiers d'intervention
current_directory = os.getcwd()
base_directory = os.path.join(current_directory, "tempo", "Download_ARD2")

# Fonction pour générer les données des photos d'intervention
def generate_photo_intervention_data(base_directory):
    interventions = []
    for intervention_cri in os.listdir(base_directory):
        intervention_path = os.path.join(base_directory, intervention_cri)
        if os.path.isdir(intervention_path):
            for i, photo_name in enumerate(os.listdir(intervention_path), start=1):
                intervention = {
                    "cle": f"photo{intervention_cri}_{i}",
                    "intervention_cri": intervention_cri,
                    "photo": photo_name
                }
                interventions.append(intervention)
    return interventions

# Fonction pour envoyer une requête POST
def send_photo_intervention_post_request(url, data):
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

# Génération des données
photo_intervention_data = generate_photo_intervention_data(base_directory)

# Affichage des données générées
print("Données envoyées :")
print(json.dumps(photo_intervention_data, indent=4))

# Envoi de la requête
response = send_photo_intervention_post_request(base_url, photo_intervention_data)
print("Response Status Code:", response.status_code)
print("Response Text:", response.text)
