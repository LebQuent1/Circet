import pandas as pd
import json
import os

# Chemin vers le fichier CSV d'origine
input_csv_file_path = os.path.join(os.getcwd(), 'tempo', 'nouveau_fichier.csv')
# Chemin vers le fichier JSON transformé
output_json_file_path = os.path.join(os.getcwd(), 'tempo', 'EXPORT.json')

# Vérification de l'existence du fichier CSV
if not os.path.exists(input_csv_file_path):
    print(f"Le fichier {input_csv_file_path} n'existe pas. Assurez-vous que le fichier est au bon emplacement.")
    exit(1)

# Lecture des données du fichier CSV
df = pd.read_csv(input_csv_file_path, delimiter=';', quotechar='"')

# Conversion des données en dictionnaire
data = df.to_dict(orient='records')

# Transformation des données
transformed_data = {
    "data": []
}

# Renommer les colonnes pour correspondre au format JSON attendu
for item in data:

    date_intervention = item["Date"]
    
    # Remplacer les "/" par des "-" dans la date
    date_intervention = date_intervention.replace('/', '-')
    
    # Réorganiser la date pour avoir le format "YYYY-MM-DD"
    day, month, year = date_intervention.split('-')
    date_intervention = f"{year}-{month}-{day}"
    
    transformed_data["data"].append({
        "Reference": item["Référence"],
        "date_intervention": date_intervention,
        "heure_intervention": item["Heure"],
        "Departement": item["Département"],
        "Jeton": item["Jeton"],
        "Techniciens": item["Techniciens"]
    })

# Écriture des données transformées dans un nouveau fichier JSON
with open(output_json_file_path, 'w') as f:
    json.dump(transformed_data, f, indent=4, ensure_ascii=False)

print("Transformation terminée. Les données transformées ont été enregistrées dans", output_json_file_path)
