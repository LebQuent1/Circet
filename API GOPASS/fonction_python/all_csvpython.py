import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time
import traceback

def create_new_csv(file_path):
    df = pd.DataFrame(columns=["Référence", "Client", "Date", "Heure", "Département", "Jeton", "Techniciens"])
    df.to_csv(file_path, index=False, sep=';')
    print(f"New file {file_path} created successfully.")

def check_and_recreate_csv(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, sep=';')
            if df.empty:
                print(f"{file_path} is empty, recreating the file.")
                os.remove(file_path)
                create_new_csv(file_path)
        except pd.errors.EmptyDataError:
            print(f"No columns to parse from file {file_path}, recreating the file.")
            os.remove(file_path)
            create_new_csv(file_path)
    else:
        create_new_csv(file_path)

def update_memory_file(memory_file_path, new_references):
    if os.path.exists(memory_file_path):
        memory_df = pd.read_csv(memory_file_path, sep=';')
    else:
        memory_df = pd.DataFrame(columns=["Référence"])

    # Ajouter les nouvelles références à mémoire.csv
    new_references_df = pd.DataFrame(new_references, columns=["Référence"])
    updated_memory_df = pd.concat([memory_df, new_references_df]).drop_duplicates().reset_index(drop=True)

    updated_memory_df.to_csv(memory_file_path, index=False, sep=';')
    print(f"Updated memory file: {memory_file_path}")

def remove_processed_references(new_csv_path, memory_file_path):
    # Charger les fichiers CSV
    if os.path.exists(new_csv_path):
        new_df = pd.read_csv(new_csv_path, sep=';')
    else:
        print(f"File {new_csv_path} does not exist.")
        return

    if os.path.exists(memory_file_path):
        memory_df = pd.read_csv(memory_file_path, sep=';')
        processed_references = memory_df['Référence'].tolist()
    else:
        processed_references = []

    # Supprimer les lignes de nouveau_fichier.csv où la référence est déjà dans mémoire.csv
    filtered_df = new_df[~new_df['Référence'].isin(processed_references)]

    # Sauvegarder le nouveau fichier CSV sans les références traitées
    filtered_df.to_csv(new_csv_path, index=False, sep=';')

    # Retourner les références restant dans le fichier nouveau_fichier.csv
    return filtered_df['Référence'].tolist()

def connect_and_fill_date(url, identifiant, password, adresse, adresse2):
    driver = None
    try:
        # Chemin du fichier CSV existant
        existing_csv_path = os.path.join(adresse2, "nouveau_fichier.csv")
        check_and_recreate_csv(existing_csv_path)

        memory_file_path = os.path.join(adresse2, "mémoire.csv")

        chrome_options = Options()
        chrome_options.add_argument("--disable-search-engine-choice-screen")
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)

        tps = 1
        wait = WebDriverWait(driver, 10)

        identifiant_textfield = wait.until(EC.presence_of_element_located((By.ID, "11")))
        password_textfield = driver.find_element(By.ID, "12")
        login_button = driver.find_element(By.ID, "13")

        identifiant_textfield.send_keys(identifiant)
        password_textfield.send_keys(password)
        login_button.click()
        time.sleep(10)

        wait.until(EC.element_to_be_clickable((By.XPATH, 

        # Obtenir la date et l'heure actuelles, puis soustraire 1 jour et 360 minutes
        # date_veille = datetime.now() - timedelta(days=1)

        # Formater la date au format souhaité
        # today = date_veille.strftime("%d/%m/%Y")


        today = datetime.now().strftime("%d/%m/%Y")

        date_input = wait.until(EC.presence_of_element_located((By.XPATH, '')))
        date_input.send_keys(today)
        date_input.send_keys(Keys.ENTER)
        time.sleep(tps)

        try:
            submit_button = driver.find_element(By.XPATH, '')
            if submit_button.is_displayed() and submit_button.is_enabled():
                submit_button.click()
            else:
                driver.execute_script("arguments[0].click();", submit_button)
        except Exception as e:
            print("Erreur lors du clic sur le bouton : ", e)
            driver.execute_script("arguments[0].click();", submit_button)

        time.sleep(5)

        wait.until(EC.element_to_be_clickable((By.XPATH, ''))).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, ''))).click()
        select = Select(driver.find_element(By.ID, ''))
        select.select_by_visible_text('<')
        heure_actuel_moins_temps = datetime.now() #- timedelta(days=0, minutes=00)
        heure_actuel_moins_temps_str = heure_actuel_moins_temps.strftime('%d/%m/%Y %H:%M:%S')
        driver.find_element(By.XPATH, '').send_keys(heure_actuel_moins_temps_str)
        driver.find_element(By.XPATH, '').send_keys(Keys.ENTER)
        time.sleep(tps)
        
        submit_button_2 = driver.find_element(By.XPATH, '')
        if submit_button_2.is_displayed() and submit_button_2.is_enabled():
            submit_button_2.click()
        else:
            print("Le bouton de soumission n'est pas interactable.")
        time.sleep(5)

        print("Dates remplies et soumises avec succès")

        wait.until(EC.element_to_be_clickable((By.XPATH, ''))).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, ''))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, ''))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, ''))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, ''))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, ''))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, ''))).click()

        wait.until(EC.element_to_be_clickable((By.XPATH, ''))).click()
        time.sleep(tps)
        seconds = 0
        start=time.time()
        dl_wait = True
        while dl_wait and seconds < 600: #10mins max pour le telechargement
            time.sleep(tps)
            dl_wait = False
            for fname in os.listdir(adresse):
                if fname.endswith('.crdownload'):
                    dl_wait = True
            seconds=time.time()-start

        name = "fichier_scraping_free_data_" + datetime.now().strftime("%d_%m_%Y") + ".csv"
        new_file_path = os.path.join(adresse2, name)

        for fname in os.listdir(adresse):
            if fname.endswith('export_ftthintervention.csv'):
                # Supprimer le fichier existant s'il y a lieu
                if os.path.exists(new_file_path):
                    os.remove(new_file_path)
                os.rename(os.path.join(adresse, fname), new_file_path)

        # Charger le CSV dans un DataFrame
        new_df = pd.read_csv(new_file_path, delimiter=';')

        # Séparation de la colonne "Date du rendez-vous" en deux colonnes "Date" et "Heure"
        new_df[['Date', 'Heure']] = new_df['Date du rendez-vous'].str.split(' ', expand=True)

        # Suppression de l'ancienne colonne "Date du rendez-vous"
        new_df.drop(columns=['Date du rendez-vous'], inplace=True)

        # Réorganisation des colonnes pour avoir "Date" et "Heure" aux bonnes positions
        cols = ['Référence', 'Client', 'Date', 'Heure', 'Département', 'Jeton', 'Techniciens']
        new_df = new_df[cols]

        # Charger le CSV existant s'il y a lieu
        if os.path.exists(existing_csv_path):
            existing_df = pd.read_csv(existing_csv_path, sep=';')
            # Concaténer les nouvelles données avec les anciennes
            combined_df = pd.concat([existing_df, new_df]).drop_duplicates().reset_index(drop=True)
        else:
            combined_df = new_df

        # Sauvegarder le DataFrame combiné dans le fichier CSV
        combined_df.to_csv(existing_csv_path, index=False, sep=';')

        # Supprimer les lignes déjà présentes dans mémoire.csv
        remaining_references = remove_processed_references(existing_csv_path, memory_file_path)

        # Mettre à jour le fichier mémoire avec les nouvelles références
        update_memory_file(memory_file_path, remaining_references)

        print("Les fichiers CSV 'nouveau_fichier.csv' et 'mémoire.csv' ont été mis à jour avec les nouvelles données traitées.")
        
        return driver, existing_csv_path

    except Exception as e:
        print("Une erreur s'est produite :", e)
        traceback.print_exc()
        if driver:
            driver.quit()
        return None, None

def main(adresse2):
    start_time = datetime.now()
    print(f"Début dl new data: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    url = ""
    
    identifiant = ''
    password = ''
    
    
    # Appel unique à connect_and_fill_date
    print("Starting new iteration...")
    driver, new_csv_path = connect_and_fill_date(url, identifiant, password, adresse, adresse2)

    if driver:
        driver.quit()

    if new_csv_path and os.path.exists(new_csv_path):
        print(f"CSV file updated: {new_csv_path}")
    else:
        print("Failed to update the CSV file.")
    
    end_time = datetime.now()
    print(f"Fin dl new data: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    adresse2 = os.path.join(os.getcwd(), "tempo")
    main(adresse2)
