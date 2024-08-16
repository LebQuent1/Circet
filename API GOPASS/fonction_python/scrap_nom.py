from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
import configparser

def log():
    
    identifiant = ''
    password = ''
    return identifiant, password

def scrap_nom(input_csv_path, download_directory, output_csv_path):
    print("Starting scrap_nom function...")

    # Vérifiez que les chemins sont corrects
    print(f"Input CSV Path: {input_csv_path}")
    print(f"Download Directory: {download_directory}")
    print(f"Output CSV Path: {output_csv_path}")

    df = pd.read_csv(input_csv_path, sep=';')
    chrome_options = Options()
    prefs = {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-search-engine-choice-screen")
    driver = webdriver.Chrome(options=chrome_options)

    def login_to_site(driver):
        print("Logging in to the site...")
        driver.get("")
        identifiant, password = log()
        identifiant_textfield = driver.find_element(By.ID, "")
        password_textfield = driver.find_element(By.ID, "")
        login_button = driver.find_element(By.CLASS_NAME, "")
        time.sleep(3)  # Augmenté à 3 secondes
        identifiant_textfield.send_keys(identifiant)
        time.sleep(3)  # Augmenté à 3 secondes
        password_textfield.send_keys(password)
        time.sleep(3)  # Augmenté à 3 secondes
        login_button.click()
        time.sleep(7)  # Augmenté à 7 secondes
        print("Logged in successfully.")

    def download_document_names(driver, inter):
        print(f"Downloading document names for intervention {inter}...")
        time.sleep(5)  # Temps d'attente pour s'assurer que la page est complètement chargée
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all('div', class_='document-link')
        document_names = []
        for div in divs:
            file_name = div.text.strip()
            document_names.append(file_name)
        print(f"Found {len(document_names)} documents.")
        return document_names

    login_to_site(driver)
    data = []
    for inter in df['Référence']:
        print(f"Processing intervention {inter}...")
        driver.execute_script(f"window.open('")
        time.sleep(5)  # Attente supplémentaire pour l'ouverture de la page
        driver.switch_to.window(driver.window_handles[-1])
        document_names = download_document_names(driver, inter)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        if document_names:
            record = {'REFERENCE': inter}
            for i, doc_name in enumerate(document_names):
                record[f'document_{i + 1}'] = doc_name
            data.append(record)
        time.sleep(3)  # Temps d'attente avant de passer à l'intervention suivante
    driver.quit()
    output_df = pd.DataFrame(data)
    output_df.to_csv(output_csv_path, sep=';', index=False)
    print(f"Process completed and data saved to {output_csv_path}")

if __name__ == "__main__":
    # Définir les chemins d'accès
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_csv_path = os.path.join(script_dir, "..", "tempo", "nouveau_fichier.csv")
    download_directory = os.path.join(script_dir, "..", "tempo", "Download_nom")
    output_csv_path = os.path.join(script_dir, "..", "tempo", "output_images.csv")

    # Appeler la fonction scrap_nom
    scrap_nom(input_csv_path, download_directory, output_csv_path)
