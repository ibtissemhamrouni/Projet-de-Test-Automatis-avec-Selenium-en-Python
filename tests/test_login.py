
from selenium import webdriver 

from selenium.webdriver.chrome.service import Service 

from selenium.webdriver.chrome.options import Options 

from selenium.webdriver.common.by import By 

import time 

import sys 

import os 

 

# Ajoute le dossier parent au path pour que "pages" soit reconnu 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) 

 

# Maintenant, tu peux importer config 

import config 

 

 

# Configuration du navigateur 

chrome_options = Options() 

chrome_options.binary_location = config.CHROME_PORTABLE_PATH 

service = Service(config.CHROMEDRIVER_PATH) 

driver = webdriver.Chrome(service=service, options=chrome_options) 

driver.implicitly_wait(5)  # Attente implicite 

 

try: 

    # Ouvrir la page de connexion 

    driver.get(config.BASE_URL) 

 

    # Vérifier que la page se charge 

    assert "Swag Labs" in driver.title, "Le titre de la page est incorrect" 

 

    # Remplir le formulaire de connexion 

    username = driver.find_element(By.NAME, "user-name") 

    password = driver.find_element(By.NAME, "password") 

    login_button = driver.find_element(By.ID, "login-button") 

 

    username.clear() 

    username.send_keys(config.USERNAME) 

 

    password.clear() 

    password.send_keys(config.PASSWORD) 

 

    login_button.click()  # Cliquer sur le bouton de connexion 

    time.sleep(3)  # Attendre le chargement de la page 

 

    # Vérification après connexion 

    assert "inventory.html" in driver.current_url, "Échec de la connexion" 

    assert driver.find_element(By.CLASS_NAME, "inventory_list"), "La liste des produits ne s'affiche pas" 

 

    print("✅ Connexion réussie !") 

 

except Exception as e: 

    print(f"❌ Erreur lors du test : {e}") 

 

finally: 

    driver.quit()  # Ferme le navigateur après le test 