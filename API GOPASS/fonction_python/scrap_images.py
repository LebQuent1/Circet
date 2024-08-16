from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os
import base64
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from pykeepass import PyKeePass

def log():
    identifiant = ""
    password = ""
    return identifiant, password

def main():
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct paths relative to the script's directory
    csv_path = os.path.join(script_dir, "..", "tempo", "nouveau_fichier.csv")
    download_directory = os.path.join(script_dir, "..", "tempo", "Download_ARD2")
    output_csv_path = os.path.join(script_dir, "..", "tempo", "num_PTO.csv")

    # Charger les numéros d'intervention à partir d'un DataFrame
    df = pd.read_csv(csv_path, sep=';')

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
    

    # Connexion au site
    def login_to_site(driver):
        identifiant, password = log()
        # Ouvrir la page de connexion
        driver.get("")

        # Temps d'attente entre chaque action
        tps = 1

        # Identification
        identifiant_textfield = driver.find_element(By.ID, "")
        password_textfield = driver.find_element(By.ID, "")
        login_button = driver.find_element(By.ID, "")

        time.sleep(tps)
        identifiant_textfield.send_keys(identifiant)
        time.sleep(tps)
        password_textfield.send_keys(password)
        time.sleep(tps)
        login_button.click()
        time.sleep(tps)

    def access_image(driver, inter):
        tps = 1

        # SELECTIONNER LA REF (UNIQUE)
        time.sleep(tps+2)
        driver.find_element(By.XPATH, '').click()
        time.sleep(tps)
        driver.find_element(By.XPATH, '').click()
        time.sleep(tps + tps)
    
        # Trouver la case de texte où entrer la valeur de `inter`
        search_textfield = driver.find_element(By.XPATH, '')
        
        # Effacer tout texte existant dans le champ de texte (facultatif)
        search_textfield.clear()
        
        # Entrer la valeur de `inter` dans la case de texte
        search_textfield.send_keys(inter)
        time.sleep(tps)
        driver.find_element(By.XPATH, '').click()
        time.sleep(tps)
        driver.find_element(By.XPATH, '').click()
        time.sleep(tps)
        driver.find_element(By.XPATH, '').click()
        time.sleep(tps)

    def download_PTO(driver, inter):
        # Récupérer le contenu HTML de la nouvelle page
        html_content = driver.page_source
        
        # Utiliser BeautifulSoup pour analyser le contenu HTML
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Créer un dossier pour le jeton s'il n'existe pas
        jeton_directory = os.path.join(download_directory, str(inter))
        if not os.path.exists(jeton_directory):
            os.makedirs(jeton_directory)

        # Trouver tous les éléments <div> avec la classe "label"
        labels = soup.find_all('div', class_='')

        pto_text = None
        # Parcourir les éléments pour trouver celui contenant "PTO :"
        for label in labels:
            if label.find('b') and label.find('b').text == 'PTO : ':
                pto_text = label.get_text(strip=True).replace('PTO :', '').strip()  
                print(f"Code PTO pour le jeton {inter} est {pto_text}.")
                break
        return pto_text

    def download_images(driver, inter):
        driver.find_element(By.XPATH, '').click()
        time.sleep(1)
        # Récupérer le contenu HTML de la nouvelle page
        html_content = driver.page_source
        
        # Utiliser BeautifulSoup pour analyser le contenu HTML
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Créer un dossier pour le jeton s'il n'existe pas
        jeton_directory = os.path.join(download_directory, str(inter))
        if not os.path.exists(jeton_directory):
            os.makedirs(jeton_directory)
        
        # Trouver toutes les balises <img> contenant les images encodées en base64
        img_tags = soup.find_all("img")
        
        # Parcourir toutes les balises <img> et extraire les images encodées en base64
        for i, img_tag in enumerate(img_tags, start=1):
            # Extraire l'attribut src de la balise <img>
            image_src = img_tag.get("src", "")
        
            # Vérifier si l'attribut src contient une image encodée en base64
            if image_src.startswith("data:image"):
                # Supprimer le préfixe "data:image/jpeg;base64," de la chaîne
                base64_data = image_src.split(",")[1]
        
                # Décoder la chaîne base64 en données binaires
                image_data = base64.b64decode(base64_data)
        
                # Écrire les données binaires dans un fichier
                image_path = os.path.join(jeton_directory, f"image_{i}.jpg")
                with open(image_path, "wb") as file:
                    file.write(image_data)
        
        print(f"Images pour le jeton {inter} a été enregistrée avec succès dans {jeton_directory}.")

    # Script principal
    login_to_site(driver)

    data = []
    # Boucle sur toutes les interventions
    for inter in df['Référence']:
        # Ouvrir une nouvelle fenêtre pour l'intervention
        driver.execute_script(f"")

        # Basculer sur la nouvelle fenêtre
        driver.switch_to.window(driver.window_handles[-1])

        # Accéder à l'image de l'intervention
        access_image(driver, inter)

        # Télécharger les images de l'intervention
        pto_text = download_PTO(driver, inter)

        data.append({'Référence': inter, 'PTO': pto_text})

        download_images(driver, inter)
        # Fermer la fenêtre de l'intervention
        driver.close()

        # Basculer sur la fenêtre principale
        driver.switch_to.window(driver.window_handles[0])

    # Fermer le navigateur
    driver.quit()

    # Convertir les données en DataFrame et enregistrer dans un fichier CSV
    output_df = pd.DataFrame(data)
    output_df.to_csv(output_csv_path, sep=';', index=False)

    print("Process completed and data saved to output_fichier.csv")

if __name__ == "__main__":
    main()
