from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class Register_Test(LiveServerTestCase):
    def setUp(self):
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_create_account(self):
        self.driver.get('http://localhost:5173/login')      
        toggle_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.toggle-form a'))
        )
        toggle_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'email'))
        )

        self.driver.find_element(By.ID, 'email').send_keys('test@example.com')
        self.driver.find_element(By.ID, 'username').send_keys('testuser')
        self.driver.find_element(By.ID, 'first_name').send_keys('Test')
        self.driver.find_element(By.ID, 'last_name').send_keys('User')
        self.driver.find_element(By.ID, 'date_of_birth').send_keys('1990-01-01')
        self.driver.find_element(By.ID, 'password').send_keys('testpass123')

        # Submit the form
        self.driver.find_element(By.ID, 'submit').click()

        # Verify that the user is redirected to the login page
        self.assertEqual(self.driver.current_url, 'http://localhost:5173/login')
        print("User registered successfully")




class Login_Test(LiveServerTestCase):
    def setUp(self):
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
        
    def test_login(self):
        self.driver.get('http://localhost:5173/login')
        self.driver.find_element(By.ID, 'username').send_keys('testuser')
        self.driver.find_element(By.ID, 'password').send_keys('testpass123')
        self.driver.find_element(By.ID, 'submit').click()
        
        # Wait for redirection to profile page
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.current_url == 'http://localhost:5173/profile'
        )
        
        self.assertEqual(self.driver.current_url, 'http://localhost:5173/profile')
        print("User logged in successfully")
