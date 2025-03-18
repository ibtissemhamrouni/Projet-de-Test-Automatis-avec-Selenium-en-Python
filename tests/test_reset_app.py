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
driver.implicitly_wait(10)  # Attente implicite

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
    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory.html")
    )
    print("✅ Connexion réussie !")

    # Ajouter des articles au panier (ici, exemple d'ajout de deux articles)
    add_to_cart_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn_inventory")
    
    # Ajouter les deux premiers articles au panier
    add_to_cart_buttons[0].click()  # Ajouter le premier article
    add_to_cart_buttons[1].click()  # Ajouter le deuxième article
    print("✅ Articles ajoutés au panier.")

    # Vérifier que les articles sont dans le panier (badge)
    shopping_cart_badge = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.shopping_cart_badge"))
    )
    assert shopping_cart_badge.text == "2", f"Erreur : le badge montre {shopping_cart_badge.text} articles"
    print(f"✅ Badge du panier vérifié avec {shopping_cart_badge.text} article(s).")

    # Cliquer sur l'icône du panier pour accéder au menu du panier
    shopping_cart_link = driver.find_element(By.CSS_SELECTOR, "a.shopping_cart_link")
    shopping_cart_link.click()
    print("✅ Accès au panier.")

    # Cliquer sur le bouton "Continue Shopping" pour retourner à la page des produits
    continue_shopping_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='continue-shopping']"))
    )
    continue_shopping_button.click()
 

    # Vérifier que l'URL de la page des produits est correcte
    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory.html")
    )
    print("✅ Retour sur la page des produits.")

    # Trouver le bouton de menu et l'ouvrir
    menu_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))
    )
    menu_button.click()
    time.sleep(2)  # Attendre l'ouverture du menu

    # Vérifier que le menu est bien ouvert
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "reset_sidebar_link"))
    )
    
    # Trouver et cliquer sur le bouton "Reset"
    reset_button = driver.find_element(By.ID, "reset_sidebar_link")
    reset_button.click()
    print("✅ Panier réinitialisé.")

    # Retourner au panier pour vérifier qu'il est vide
 
    shopping_cart_link = driver.find_element(By.CSS_SELECTOR, "a.shopping_cart_link")
    shopping_cart_link.click()
    WebDriverWait(driver, 20).until(
        EC.url_contains("cart.html")
    )

    # Vérifier que le panier est vide (pas de badge)
    shopping_cart_badge = driver.find_elements(By.CSS_SELECTOR, "span.shopping_cart_badge")
    assert len(shopping_cart_badge) == 0, "Erreur : Le panier n'est pas vide."
    print("✅ Le panier est vide après réinitialisation.")


    # Cliquer sur le bouton "Back to Products" pour retourner à `inventory.html`
    back_to_products_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn_secondary"))
    )
    back_to_products_button.click()
    print("✅ Retour vers la page des produits.")

    # Vérifier que l'URL `inventory.html` est bien chargée
    WebDriverWait(driver, 20).until(
        EC.url_contains("inventory.html")
    )
except Exception as e:
    print(f"Erreur lors du test : {str(e)}")

finally:
    driver.quit()  # Fermer le navigateur
