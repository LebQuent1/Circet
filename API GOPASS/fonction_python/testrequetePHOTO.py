import requests
import os
import shutil

# Configuration de l'URL et du token
base_url = ""
token = ""  # Assurez-vous de remplacer par votre token réel
headers = {
    "Authorization": f"Bearer {token}"
}

# Chemin du dossier contenant les dossiers d'intervention
current_directory = os.getcwd()
base_directory = os.path.join(current_directory, "tempo", "Download_ARD2")

print(f"Base directory: {base_directory}")

# Fonction pour envoyer une requête POST avec un fichier
def send_file_upload_post_request(url, file_path):
    print(f"Sending file: {file_path}")
    with open(file_path, 'rb') as f:
        files = {'file': f}
        try:
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()  # Raises an error for 4xx/5xx status codes
            return response
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de l'envoi du fichier {file_path}: {e}")
            return None

# Parcourir les dossiers d'intervention et envoyer les fichiers JPG
if os.path.exists(base_directory):
    for intervention_cri in os.listdir(base_directory):
        intervention_path = os.path.join(base_directory, intervention_cri)
        if os.path.isdir(intervention_path):
            all_files_sent = True  # Variable pour suivre si tous les fichiers ont été envoyés
            for photo_name in os.listdir(intervention_path):
                if photo_name.lower().endswith('.jpg'):
                    photo_path = os.path.join(intervention_path, photo_name)
                    print(f"Envoi du fichier : {photo_path}")
                    response = send_file_upload_post_request(base_url, photo_path)
                    if response:
                        print(f"Response Status Code: {response.status_code}")
                        print(f"Response Text: {response.text}")
                        if response.status_code != 200:
                            all_files_sent = False  # Si l'envoi échoue, ne pas supprimer le dossier
                    else:
                        all_files_sent = False  # Si une erreur de requête se produit

            # Si tous les fichiers ont été envoyés avec succès, supprimer le dossier
            if all_files_sent:
                try:
                    shutil.rmtree(intervention_path)
                    print(f"Dossier supprimé : {intervention_path}")
                except OSError as e:
                    print(f"Erreur lors de la suppression du dossier {intervention_path}: {e}")
            else:
                print(f"Dossier non supprimé en raison d'erreurs : {intervention_path}")
else:
    print(f"Le répertoire {base_directory} n'existe pas.")
