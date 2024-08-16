import os
import pandas as pd
import re

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct paths relative to the script's directory
csv_path = os.path.join(script_dir, "..", "tempo", "output_images.csv")
base_path = os.path.join(script_dir, "..", "tempo", "Download_ARD2")

# Charger le fichier CSV
df = pd.read_csv(csv_path, sep=';')

# Print the columns of the dataframe for debugging
print("Columns in CSV file:", df.columns)

# Fonction pour nettoyer les noms de fichiers
def clean_filename(filename):
    # Enlever ou remplacer les caractères invalides
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Fonction pour générer un nom de fichier unique
def get_unique_path(directory, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{base}_{counter}{ext}"
        counter += 1
    return os.path.join(directory, unique_filename)

# Itérer sur chaque ligne du dataframe
for index, row in df.iterrows():
    reference = row['REFERENCE']
    folder_path = os.path.join(base_path, str(reference))
    
    # Vérifier si le dossier existe
    if os.path.exists(folder_path):
        # Boucler sur toutes les colonnes qui commencent par 'document_'
        for i in range(1, len(df.columns)):
            column_name = f'document_{i}'
            if column_name in df.columns:
                image_name = row[column_name]
                
                # Vérifier si image_name est une chaîne valide
                if pd.notna(image_name) and isinstance(image_name, str):
                    old_image_name = f'image_{i}.jpg'  # Correspond à image_1.jpg, image_2.jpg, etc.
                    new_image_name = clean_filename(image_name.strip())  # Nettoyer le nom de la nouvelle image
                    old_image_path = os.path.join(folder_path, old_image_name)
                    new_image_path = get_unique_path(folder_path, new_image_name)
                    
                    # Renommer le fichier s'il existe
                    if os.path.exists(old_image_path):
                        os.rename(old_image_path, new_image_path)
                        print(f"Renamed {old_image_path} to {new_image_path}")
                    else:
                        print(f"File {old_image_path} does not exist")
                else:
                    print(f"Invalid or missing image name in column: {column_name}")
    else:
        print(f"Folder {folder_path} does not exist")
