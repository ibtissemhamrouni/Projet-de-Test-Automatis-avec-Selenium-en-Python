from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os

# Ajout du dossier parent au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Importation de la configuration
from pages import config

# Service ChromeDriver
service = Service(config.CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)  # Aucune option spécifique pour gérer le mot de passe
driver.implicitly_wait(5)  # Attente implicite

try:
    # Ouvrir la page de connexion
    driver.get(config.BASE_URL)

    # Vérifier que la page se charge
    assert "Swag Labs" in driver.title, "Le titre de la page est incorrect"

    # Remplir le formulaire de connexion avec username et password
    username = driver.find_element(By.NAME, "user-name")
    password = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.ID, "login-button")

    username.clear()
    password.clear()

    # Utilisation des valeurs d'identification du fichier config
    username.send_keys(config.USERNAME)
    password.send_keys(config.PASSWORD)

    login_button.click()  # Cliquer sur le bouton de connexion
    time.sleep(3)  # Attendre le chargement de la page

    # Vérification après connexion
    assert "inventory.html" in driver.current_url, "Échec de la connexion"
    assert driver.find_element(By.CLASS_NAME, "inventory_list"), "La liste des produits ne s'affiche pas"

    print("✅ Connexion réussie !")

    # Trouver le bouton de menu et l'ouvrir
    menu_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    )
    menu_button.click()
    time.sleep(2)  # Attendre l'ouverture du menu

    # Vérifier que le menu est bien ouvert
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "about_sidebar_link"))
    )

    print("✅ Menu ouvert avec succès !")

    # Trouver le lien "About" dans le menu et cliquer dessus
    about_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "about_sidebar_link"))
    )
    
    about_link.click()

    # Attendre que la page de Saucelabs soit complètement chargée
    WebDriverWait(driver, 10).until(
        EC.url_contains("saucelabs.com")
    )

    # Vérification de la redirection vers la page de Saucelabs
    assert "saucelabs.com" in driver.current_url, "La redirection vers la page 'About' a échoué"

    print("✅ Redirection vers la page Saucelabs réussie !")

except Exception as e:
    print(f"Erreur lors du test : {str(e)}")

finally:
    driver.quit()  # Fermer le navigateur
