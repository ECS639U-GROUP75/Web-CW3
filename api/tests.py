from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

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



class Age_Filter_Test(LiveServerTestCase):
    def setUp(self):
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
        
    def test_age_filter(self):
        self.driver.get('http://localhost:5173/login')
        self.driver.find_element(By.ID, 'username').send_keys('testuser')
        self.driver.find_element(By.ID, 'password').send_keys('testpass123')
        self.driver.find_element(By.ID, 'submit').click()
        
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.current_url == 'http://localhost:5173/profile'
        )
        
        self.assertEqual(self.driver.current_url, 'http://localhost:5173/profile')
        self.driver.find_element(By.ID, 'hobbies-link').click()

        print("Current URL:", self.driver.current_url)
        
        
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.current_url == 'http://localhost:5173/Hobbies'
        )
        
        self.assertEqual(self.driver.current_url, 'http://localhost:5173/Hobbies')
        self.driver.find_element(By.ID, 'min-age').send_keys('18')
        self.driver.find_element(By.ID, 'max-age').send_keys('30')
        self.driver.find_element(By.ID, 'apply-filter').click()
        
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'user-table'))
        )
        
        user_rows = self.driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        self.assertGreater(len(user_rows), 0, "No users found in the filtered results")
        for row in user_rows:
            age_cell = row.find_elements(By.TAG_NAME, 'td')[3]  
            age = int(age_cell.text)
            self.assertGreaterEqual(age, 18, f"Found user with age {age} below minimum age 18")
            print(f"Found user with age {age} between 18 and 30")
            self.assertLessEqual(age, 30, f"Found user with age {age} above maximum age 30")


       
class Edit_Test(LiveServerTestCase):
    def setUp(self):
        
        options = webdriver.ChromeOptions()
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
        
    def test_edit(self):
        self.driver.get('http://localhost:5173/login')
        self.driver.find_element(By.ID, 'username').send_keys('newusername')
        self.driver.find_element(By.ID, 'password').send_keys('testpass123')
        self.driver.find_element(By.ID, 'submit').click()
        
        # Wait for redirection to profile page
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.current_url == 'http://localhost:5173/profile'
        )
        
        self.assertEqual(self.driver.current_url, 'http://localhost:5173/profile')
        print("User logged in successfully")

        self.driver.find_element(By.ID, 'edit-button').click()

        WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'ProfileEditModal'))
        )

        self.driver.find_element(By.ID, 'username').clear()
        self.driver.find_element(By.ID, 'username').send_keys('newusername')
        self.driver.find_element(By.ID, 'bio').clear()
        self.driver.find_element(By.ID, 'bio').send_keys('New bio')
        self.driver.find_element(By.ID, 'email').clear()
        self.driver.find_element(By.ID, 'email').send_keys('newemail@example.com')
        self.driver.find_element(By.ID, 'dob').clear()
        self.driver.find_element(By.ID, 'dob').send_keys('2000-01-01')
        self.driver.find_element(By.ID, 'save-button').click()

        # Wait for redirection to profile page
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.current_url == 'http://localhost:5173/profile'
        )

        self.driver.find_element(By.ID, 'add-button').click()

        WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'HobbyAddModal'))
        )

        self.driver.find_element(By.ID, 'hobby-select').click()
        time.sleep(1)  # Wait for dropdown to open
        self.driver.find_element(By.ID, 'Music').click()
        time.sleep(1)  # Wait for selection to register
        
        # Try to click the button using CSS selector
        add_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#HobbyAddModal button.btn-primary'))
        )
        add_button.click()
        
        # Wait for modal to close
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.ID, 'HobbyAddModal'))
        )
        self.assertEqual(self.driver.current_url, 'http://localhost:5173/profile')
        print("User edited successfully")


class Send_Request_Test(LiveServerTestCase):
    def setUp(self):
        
        options = webdriver.ChromeOptions()
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
        
    def test_Request(self):
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

        self.driver.find_element(By.ID, 'hobbies-link').click()

        print("Current URL:", self.driver.current_url)
        
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.current_url == 'http://localhost:5173/Hobbies'
        )
        
        self.assertEqual(self.driver.current_url, 'http://localhost:5173/Hobbies')
        
        # Wait for the table to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'user-table'))
        )
        
        # Get all user rows and click the first send friend request button
        user_rows = self.driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        self.assertGreater(len(user_rows), 0, "No users found in the table")
        
        send_request_button = user_rows[0].find_element(By.ID, 'send-friend-request')
        send_request_button.click()

        time.sleep(2)
        
        print("Request sent successfully")


class Accept_Request_Test(LiveServerTestCase):
    def setUp(self):
        
        options = webdriver.ChromeOptions()
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()
        
    def test_Request(self):
        self.driver.get('http://localhost:5173/login')
        self.driver.find_element(By.ID, 'username').send_keys('MusicVibes09')
        self.driver.find_element(By.ID, 'password').send_keys('M1Us=s5%0A<,')
        self.driver.find_element(By.ID, 'submit').click()
        
        
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.current_url == 'http://localhost:5173/profile'
        )
        
        self.assertEqual(self.driver.current_url, 'http://localhost:5173/profile')
        print("User logged in successfully")

        self.driver.find_element(By.ID, 'friends-link').click()

        print("Current URL:", self.driver.current_url)
        
        WebDriverWait(self.driver, 10).until(
            lambda driver: driver.current_url == 'http://localhost:5173/friends'
        )
        
        self.assertEqual(self.driver.current_url, 'http://localhost:5173/friends')
        
        self.driver.find_element(By.ID, 'accept-friend-request').click()

        time.sleep(2)
        
        print("Request sent successfully")