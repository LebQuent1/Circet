import pandas as pd
import json
import pandas as pd
import json
import os

# Utiliser le dossier actuel comme chemin
folder_path = os.getcwd()

# Chemins des fichiers CSV et JSON
csv_file_1 = os.path.join(folder_path, "Exporter_litiges_FREE_-_CAN.csv")
csv_file_2 = os.path.join(folder_path, "Exporter_Malfaçons_-_CAN.csv")
json_file = os.path.join(folder_path, "combined_tickets.json")

# Lire les fichiers CSV en utilisant des guillemets pour délimiter les champs et en ignorant les lignes incorrectes
df_csv_1 = pd.read_csv(csv_file_1, delimiter=';', quotechar='"', skipinitialspace=True, encoding='utf-8', on_bad_lines='skip')
df_csv_2 = pd.read_csv(csv_file_2, delimiter=';', quotechar='"', skipinitialspace=True, encoding='utf-8', on_bad_lines='skip')

# Combiner les deux DataFrames
df_csv = pd.concat([df_csv_1, df_csv_2], ignore_index=True)

# Lire le fichier JSON
with open(json_file, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# Filtrer les tickets JSON par type
filtered_json_data = [item for item in json_data if item['type'] in ['Gestion de litiges', 'Malfaçons OI']]

# Extraire les valeurs de "hlp" des tickets filtrés et les nettoyer
json_hlp_values = {item['hlp'].strip().lower() for item in filtered_json_data if 'hlp' in item}

# Vérifier les colonnes disponibles dans le CSV combiné
print("Colonnes disponibles dans le CSV combiné:", df_csv.columns)

# Utiliser le nom exact de la colonne
csv_references_column_name = 'reference_ticket'
csv_references = df_csv[csv_references_column_name].str.strip().str.lower().tolist()

# Obtenir les valeurs uniques
unique_csv_references = set(csv_references)

# Afficher les 5 premières valeurs de chaque liste pour vérification
print("5 premières valeurs de 'reference_ticket' du CSV combiné:", list(unique_csv_references)[:5])
print("5 premières valeurs de 'hlp' du JSON filtré:", list(json_hlp_values)[:5])

# Comparer les valeurs et identifier les non correspondances
non_matching_csv_references = unique_csv_references - json_hlp_values
non_matching_json_hlp_values = json_hlp_values - unique_csv_references

# Compter les valeurs uniques
total_unique_csv_references = len(unique_csv_references)
total_unique_json_hlp_values = len(json_hlp_values)
total_non_matching_csv = len(non_matching_csv_references)
total_non_matching_json = len(non_matching_json_hlp_values)

# Créer des DataFrames pour les valeurs non correspondantes
non_matching_csv_df = pd.DataFrame(list(non_matching_csv_references), columns=['Non_Matching_CSV_References'])
non_matching_json_df = pd.DataFrame(list(non_matching_json_hlp_values), columns=['Non_Matching_JSON_HLP_Values'])

# Enregistrer les DataFrames dans des fichiers CSV
non_matching_GoPass_file = os.path.join(folder_path, "non_matching_csv_references.csv")
non_matching_helper_file = os.path.join(folder_path, "non_matching_json_hlp_values.csv")
non_matching_csv_df.to_csv(non_matching_GoPass_file, index=False)
non_matching_json_df.to_csv(non_matching_helper_file, index=False)

# Afficher les résultats
print(f"Nombre de tickets hlp dans bdd helper filtré: {total_unique_json_hlp_values}")
print(f"Nombre de références tickets dans les exports GoPass: {total_unique_csv_references}")
print(f"Nombre de valeurs references_tickets présente sur GoPass  non retrouvées dans la bdd Helper: {total_non_matching_csv}")
print(f"Nombre de tickets hlp filtrées présents sur Helper non retrouvées dans les exports GoPass: {total_non_matching_json}")
print(f"Les références de GoPass non retouvées dans helper ont été enregistrées dans {non_matching_GoPass_file}.")
print(f"Les références de helper non retouvées dans GoPass ont été enregistrées dans {non_matching_helper_file}.")
