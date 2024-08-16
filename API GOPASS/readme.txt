# Projet d'envois des informations et Images d'interventions vers l'API 

## Description

Ce projet a pour objectif de télécharger, traiter et renommer des images et données associées à des interventions techniques à partir de diverses sources, puis de les envoyer via des requêtes API. Le projet comporte plusieurs scripts Python, chacun ayant une fonction spécifique dans le processus global.

## Structure du Projet

- `main.py` : Script principal qui exécute tous les autres scripts dans un ordre séquentiel. Il coordonne le téléchargement, le traitement et l'envoi des données et images.
- `fonction_python/` : Dossier contenant tous les scripts nécessaires à l'exécution du projet.
- `tempo/` : Dossier contenant les fichiers temporaires, comme les images téléchargées et les fichiers CSV intermédiaires.
-  fichier mémoire 'mémoire.csv', enregistre toutes les interventions traitées par le script.
## Scripts

### 1. `main.py`
**Fonction :**  
Coordonne l'exécution des différents scripts du projet.

**Fonctionnement :**  
- Exécute les scripts dans un ordre spécifique.
- Affiche des messages de débogage pour chaque script lancé.
- À la fin de l'exécution, affiche la date et l'heure de début et de fin du script.

### 2. `all_csvpython.py`
**Fonction :**  
Télécharge les nouvelles données d'intervention à partir des inter présentes sur .

**Fonctionnement :**  
- Se connecte à .
- Remplit les champs de date pour filtrer les interventions.
- Télécharge un fichier CSV contenant les interventions de la journée et les traite ( adaptable dans le code pour limiter la période ou choisir une autre journée).

### 3. `scrap_images.py`
**Fonction :**  
Télécharge les images associées aux interventions.

**Fonctionnement :**  
- Se connecte à  pour récupérer les images liées à chaque intervention.
- Télécharge les images dans un dossier spécifique sous `tempo/Download`.
- Associe chaque image avec son intervention respective en les enregistrants dans des dossiers nommés par le num_inter.
- Récupère les numéros des PTO de chaques inter( à supprimer pour l'API a terme)

### 4. `scrap_nom.py`
**Fonction :**  
Télécharge les noms des images associés aux interventions.

**Fonctionnement :**  
- Se connecte à abborraco pour récupérer les noms des techniciens.
- Met à jour un fichier CSV avec les noms des images pour chaque intervention.

### 5. `rename.py`
**Fonction :**  
Renomme les images téléchargées en fonction des informations contenues dans le fichier CSV précedemment crée.

**Fonctionnement :**  
- Lit le fichier CSV pour obtenir les nouveaux noms des images.
- Renomme les images dans le dossier `tempo/Download` en fonction des informations du CSV.

### 6. `scriptJsonFormat.py`
**Fonction :**  
Convertit les données des interventions de CSV en JSON.

**Fonctionnement :**  
- Lit le fichier CSV contenant les données d'intervention.
- Convertit les données en un format JSON structuré.
- Sauvegarde les données JSON dans un fichier dans le dossier `tempo`.

### 7. `testrequeteINTER.py`
**Fonction :**  
Envoie les informations des interventions à une API via une requête POST.

**Fonctionnement :**  
- Lit le fichier JSON généré par `scriptJsonFormat.py`.
- Envoie les données d'intervention à l'API .


### 8. `testRequeteDonnePhoto.py`
**Fonction :**  
Prépare les données des photos d'intervention puis les envois à l'API.

**Fonctionnement :**  
- Récupère les images associées aux interventions dans `tempo/Download`.
- Envois les données des photos à l'API.

### 9. `testrequetePHOTO.py`
**Fonction :**  
Envoie les photos des interventions à une API via une requête POST (envois des photos 1 par 1, imposé par la requête fournis).

**Fonctionnement :**  
- Parcourt le dossier `tempo/Download` pour trouver les images.
- Envoie chaque image à l'API.
- Supprime les dossiers d'intervention une fois les photos envoyées avec succès pour éviter de trop stocker en local.

## Utilisation

1. **Configurer les scripts** : Assurez-vous que les informations d'authentification (comme les tokens API) et les chemins d'accès sont correctement configurés dans les scripts.
2. **Exécuter le projet** : Lancer le script `main.py` pour démarrer l'ensemble du processus.
3. **Surveiller les logs** : Chaque script imprime des messages de débogage pour suivre l'exécution. Ces logs peuvent être utilisés pour identifier les problèmes ou vérifier le bon déroulement du processus.

## Dépendances

- **Python 3.x**
- **Bibliothèques Python** : pandas, requests, selenium, etc.

Assurez-vous que toutes les dépendances sont installées en exécutant `pip install -r requirements.txt`.

## Auteur
Quentin LEBOUC
