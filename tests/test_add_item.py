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
import config

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

    # Cliquer sur un article spécifique (id=4 dans l'URL)
    item = driver.find_element(By.ID, "item_4_title_link")
    item.click()

    # Vérifier que l'on est bien sur la page de l'article spécifique (inventory-item.html?id=4)
    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory-item.html?id=4")
    )

    # Vérifier la présence de l'image avec l'alt text "Sauce Labs Backpack"
    inventory_image = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='Sauce Labs Backpack']"))
    )
    print("✅ L'image du produit est présente !")

    # Cliquer sur le bouton "Add to cart"
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_inventory"))
    )
    add_to_cart_button.click()
    print("✅ Le produit a été ajouté au panier !")

    # Vérifier que l'article a bien été ajouté au panier
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_link"))
    )

    # Accéder au panier
    shopping_cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    shopping_cart_link.click()

    # Cliquer sur le bouton de Checkout
    checkout_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.checkout_button"))
    )
    checkout_button.click()

    # Remplir le formulaire de paiement
    first_name = driver.find_element(By.NAME, "firstName")
    last_name = driver.find_element(By.NAME, "lastName")
    zip_code = driver.find_element(By.NAME, "postalCode")

    # Entrer les informations
    first_name.send_keys("John")
    last_name.send_keys("Doe")
    zip_code.send_keys("12345")

    # Valider le formulaire
    continue_button = driver.find_element(By.CSS_SELECTOR, "input.btn_primary")
    continue_button.click()

    # Vérifier que l'on est sur la page suivante (checkout-step-two.html)
    WebDriverWait(driver, 20).until(
        EC.url_contains("checkout-step-two.html")
    )

    # Passer à la page suivante (checkout complete)
    finish_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn_action.btn_medium.cart_button"))
    )
    finish_button.click()

    # Vérifier que l'on est sur la page de confirmation (checkout-complete.html)
    WebDriverWait(driver, 20).until(
        EC.url_contains("checkout-complete.html")
    )
   # Vérifier que la page de confirmation de commande est bien affichée
    WebDriverWait(driver, 20).until(
        EC.url_contains("checkout-complete.html")
    )
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "checkout_complete_container"))
    )
    # Cliquer  pour retourner à la page d'inventaire
    back_to_products_button = driver.find_element(By.ID, "back-to-products")
    back_to_products_button.click()

    # Vérifier que l'on est de retour sur la page des produits (inventory.html)
    WebDriverWait(driver, 20).until(
        EC.url_contains("inventory.html")
    )

    print("✅ Test réussi ! Retour à la page des produits !")

except Exception as e:
    print(f"Erreur lors du test : {str(e)}")

finally:
    driver.quit()  # Fermer le navigateur
