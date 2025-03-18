
import unittest
from selenium import webdriver
from config import BASE_URL, USERNAME, PASSWORD, CHROMEDRIVER_PATH
from pages.login_page import LoginPage

class TestLogin(unittest.TestCase):
    def setUp(self):
        """Initialisation du navigateur"""
        self.driver = webdriver.Chrome(CHROMEDRIVER_PATH)
        self.driver.get(BASE_URL)
        self.login_page = LoginPage(self.driver)

    def test_successful_login(self):
        """Vérifie si la connexion est réussie avec les bonnes informations"""
        self.login_page.login(USERNAME, PASSWORD)
        self.assertTrue(self.login_page.is_login_successful(), "La connexion a échoué !")
        print("✅ Connexion réussie !")

    def tearDown(self):
        """Fermeture du navigateur après le test"""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
