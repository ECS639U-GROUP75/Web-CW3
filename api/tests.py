from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from django.test.utils import override_settings
from django.test.runner import DiscoverRunner
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from .models import Hobby
import datetime, time, warnings

TEST_DB = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST': {
            'NAME': None,
        }
    }
}

class CustomTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        return super().setup_databases(**kwargs)
    
    def teardown_databases(self, old_config, **kwargs):
        super().teardown_databases(old_config, **kwargs)

@override_settings(DATABASES=TEST_DB, TEST_RUNNER='api.tests.CustomTestRunner')
class Tests(StaticLiveServerTestCase):
    
    @classmethod
    def setUp(self):
        warnings.filterwarnings(
            'ignore',
            message='Overriding setting DATABASES can lead to unexpected behavior.',
            category=UserWarning
        )
        super().setUpClass()
        self.selenium = webdriver.Chrome(ChromeDriverManager().install())
        self.selenium.implicitly_wait(10)
        self.wait = WebDriverWait(self.selenium, 10)
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')

        self.test_user_1 = {
            'username': 'newuser1',
            'first_name': 'New',
            'last_name': 'One',
            'email': 'newuser1@test.com',
            'date_of_birth': '1990-01-01',
            'password': '%405AQOf)2gA'
        }

        self.test_user_2 = {
            'username': 'newuser2',
            'first_name': 'New',
            'last_name': 'Two',
            'email': 'newuser2@test.com',
            'date_of_birth': '1990-01-01',
            'password': 'yUNH#73^0ds_'
        }
        
    def form_date_formate(self, date):
        new_date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m%d%Y')
        return new_date 
    
    @classmethod
    def tearDown(self):
        User = get_user_model()
        User.objects.all().delete()
        self.selenium.quit()
        super().tearDownClass()

    def test_01_register(self):
        print('\n\n---Register Test---')
        self.selenium.get(f'{self.live_server_url}/register/')
        
        wait = WebDriverWait(self.selenium, 10)
        
        username_field = wait.until(EC.presence_of_element_located((By.ID, 'id_username')))
        username_field.send_keys(self.test_user_1['username'])
        
        first_name_field = wait.until(EC.presence_of_element_located((By.ID, 'id_first_name')))
        first_name_field.send_keys(self.test_user_1['first_name'])
        
        last_name_field = wait.until(EC.presence_of_element_located((By.ID, 'id_last_name')))
        last_name_field.send_keys(self.test_user_1['last_name'])
        
        email_field = wait.until(EC.presence_of_element_located((By.ID, 'id_email')))
        email_field.send_keys(self.test_user_1['email'])
        
        dob_field = wait.until(EC.presence_of_element_located((By.ID, 'id_date_of_birth')))
        dob_field.send_keys(self.form_date_formate(self.test_user_1['date_of_birth']))
        
        password1_field = wait.until(EC.presence_of_element_located((By.ID, 'id_password1')))
        password1_field.send_keys(self.test_user_1['password'])
        
        password2_field = wait.until(EC.presence_of_element_located((By.ID, 'id_password2')))
        password2_field.send_keys(self.test_user_1['password'])
        
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
        submit_button.click()
        print('submit button clicked')
        
        print(self.live_server_url)
        wait.until(EC.url_to_be(self.live_server_url + '/'))
        
        User = get_user_model()
        try:
            new_user = User.objects.get(username=self.test_user_1['username'])
            self.assertEqual(new_user.email, self.test_user_1['email'])
            self.assertEqual(new_user.first_name, self.test_user_1['first_name'])
            self.assertEqual(new_user.last_name, self.test_user_1['last_name'])
            self.assertEqual(new_user.date_of_birth.strftime('%Y-%m-%d'), '1990-01-01')
            print('Register Test Passed')
        except User.DoesNotExist:
            self.fail('User was not created in database')

    def test_02_login(self):
        # Test Setup
        print('\n\n---Login Test---')
        User = get_user_model()
        User.objects.create_user(**self.test_user_1)
        self.selenium.get(f'{self.live_server_url}/login/')
        wait = WebDriverWait(self.selenium, 10)
        
        # Login
        username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        username_field.send_keys(self.test_user_1['username'])
        password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
        password_field.send_keys(self.test_user_1['password'])
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
        submit_button.click()
        
        # Wait for the page to load
        wait.until(EC.url_to_be(self.live_server_url + '/'))

        try:
            self.selenium.find_element(By.CLASS_NAME, 'btn-logout')
            print('Login Test Passed')
        except:
            self.fail('User was not logged in')

    def test_03_edit_profile(self):
        # Test Setup
        print('\n\n---Edit Profile Test---')
        User = get_user_model()
        User.objects.create_user(**self.test_user_1)
        new_data = {
            'username': 'newusername',
            'email': 'newemail@new.com',
            'bio': 'This is my new bio',
            'dob': '2000-01-01',
            'password': 'newpassword'
        }
        self.test_Hobby = Hobby.objects.create(name='Art')
        self.selenium.get(f'{self.live_server_url}/login/')
        wait = WebDriverWait(self.selenium, 10)
        
        # Login
        username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        username_field.send_keys(self.test_user_1['username'])
        password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
        password_field.send_keys(self.test_user_1['password'])
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
        submit_button.click()
        print('Logged in as User 1')
        
        # Wait for the page to load and click the edit button
        wait.until(EC.url_to_be(self.live_server_url + '/'))
        edit_button = wait.until(EC.element_to_be_clickable((By.ID, 'edit-button')))
        edit_button.click()
        wait.until(EC.visibility_of_element_located((By.ID, 'ProfileEditModal')))
        print('Edit Modal Opened')

        # Edit the profile
        edit_username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        edit_username_field.clear()
        edit_username_field.send_keys(new_data['username'])
        edit_email_field = wait.until(EC.presence_of_element_located((By.ID, 'email')))
        edit_email_field.clear()
        edit_email_field.send_keys(new_data['email'])
        edit_bio_field = wait.until(EC.presence_of_element_located((By.ID, 'bio')))
        edit_bio_field.clear()
        edit_bio_field.send_keys(new_data['bio'])
        edit_dob_field = wait.until(EC.presence_of_element_located((By.ID, 'dob')))
        edit_dob_field.clear()
        edit_dob_field.send_keys(self.form_date_formate(new_data['dob']))
        edit_password1_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
        edit_password1_field.clear()
        edit_password1_field.send_keys(new_data['password'])
        edit_password2_field = wait.until(EC.presence_of_element_located((By.ID, 'confirm-password')))
        edit_password2_field.clear()
        edit_password2_field.send_keys(new_data['password'])
        save_button = wait.until(EC.element_to_be_clickable((By.ID, 'save-button')))
        save_button.click()
        print('Profile Edited')

        # Test Visible Changes
        wait.until(EC.invisibility_of_element_located((By.ID, 'ProfileEditModal')))
        updated_user = User.objects.get(username=new_data['username'])
        self.assertEqual(updated_user.username, new_data['username'])
        self.assertEqual(updated_user.email, new_data['email'])
        self.assertEqual(updated_user.bio, new_data['bio'])
        self.assertEqual(updated_user.date_of_birth.strftime('%Y-%m-%d'), new_data['dob'])
        print('Profile Edits Successful')

        # Log out to test password change
        logout_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-logout')))
        logout_button.click()
        wait.until(EC.url_to_be(self.live_server_url + '/login/'))
        username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        username_field.send_keys(new_data['username'])
        password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
        password_field.send_keys(new_data['password'])
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
        submit_button.click()
        wait.until(EC.url_to_be(self.live_server_url + '/'))
        self.selenium.find_element(By.CLASS_NAME, 'btn-logout')
        print('Log in With New Password Successful')

        # Add Hobby Test
        # Click the add hobby button
        add_hobby_button = wait.until(EC.element_to_be_clickable((By.ID, 'add-button')))
        add_hobby_button.click()
        wait.until(EC.visibility_of_element_located((By.ID, 'HobbyAddModal')))

        # Add a new hobby
        hobby_field = wait.until(EC.element_to_be_clickable((By.ID, 'hobby-select')))
        hobby_field.click()
        hobby = wait.until(EC.element_to_be_clickable((By.XPATH, '//option[@value="Other"]')))
        hobby.click()
        new_hobby_field = wait.until(EC.presence_of_element_located((By.ID, 'hobby-name')))
        new_hobby_field.send_keys('Test')
        button_save_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Add Hobby"]')))
        button_save_button.click()
        wait.until(EC.invisibility_of_element_located((By.XPATH, 'HobbyModal')))
        hobby_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Table-Row') and normalize-space()]")))
        hobby_text = hobby_element.text.strip()        
        self.assertIn('Test', hobby_text)
        
        # Wait for modal to completely close first
        wait.until(
            EC.invisibility_of_element_located((By.ID, 'HobbyAddModal'))
        )
        
        # Then try to click delete button
        delete_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".Table-Row .btn-primary"))
        )
        delete_button.click()
        
        # Wait for row to be removed
        wait.until(
            EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'Table-Row')]"))
        )
        self.assertEqual(len(self.selenium.find_elements(By.XPATH, "//div[contains(@class, 'Table-Row')]")), 0)
        print('New Hobby Added and Deleted Sucessfully')

        # Click the add hobby button
        add_hobby_button = wait.until(EC.element_to_be_clickable((By.ID, 'add-button')))
        add_hobby_button.click()
        wait.until(EC.visibility_of_element_located((By.ID, 'HobbyAddModal')))

        # Add an existing hobby
        hobby_field = wait.until(EC.element_to_be_clickable((By.ID, 'hobby-select')))
        hobby_field.click()
        hobby = wait.until(EC.element_to_be_clickable((By.XPATH, '//option[@value="Art"]')))
        hobby.click()
        button_save_button.click()
        wait.until(EC.invisibility_of_element_located((By.XPATH, 'HobbyModal')))
        hobby_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Table-Row') and normalize-space()]")))
        hobby_text = hobby_element.text.strip()        
        self.assertIn('Art', hobby_text)
        
        # Wait for modal to completely close first
        wait.until(
            EC.invisibility_of_element_located((By.ID, 'HobbyAddModal'))
        )
        
        # Then try to click delete button
        delete_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".Table-Row .btn-primary"))
        )
        delete_button.click()
        
        # Wait for row to be removed
        wait.until(
            EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'Table-Row')]"))
        )
        self.assertEqual(len(self.selenium.find_elements(By.XPATH, "//div[contains(@class, 'Table-Row')]")), 0)
        print('Existing Hobby Added and Deleted Sucessfully')
        print('Edit Profile Test Passed')

    def test_04_filter_hobbies(self):
        # Test Setup
        print('\n\n---Filter Hobbies Test---')
        User = get_user_model()
        User.objects.create_user(**self.test_user_1)
        User.objects.create_user(**self.test_user_2)
        self.selenium.get(f'{self.live_server_url}/login/')
        wait = WebDriverWait(self.selenium, 10)
        
        # Login
        username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        username_field.send_keys(self.test_user_1['username'])
        password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
        password_field.send_keys(self.test_user_1['password'])
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
        submit_button.click()
        wait.until(EC.url_to_be(self.live_server_url + '/'))
        print('Logged in as User 1')

        # Navigate to the hobbies page
        hobbies_tab = wait.until(EC.element_to_be_clickable((By.ID, 'hobbies-link')))
        hobbies_tab.click()
        print('Navigated to Hobbies Page')

        # Filter Age Test 1
        min_age_field = wait.until(EC.presence_of_element_located((By.ID, 'min-age')))
        min_age_field.clear()
        min_age_field.send_keys('30')
        max_age_field = wait.until(EC.presence_of_element_located((By.ID, 'max-age')))
        max_age_field.clear()
        max_age_field.send_keys('40')
        filter_button = wait.until(EC.element_to_be_clickable((By.ID, 'apply-filter')))
        filter_button.click()
        print('Filtered Age with 30-40')
        rows = self.selenium.find_elements(By.XPATH, "//table[@id='user-table']//tbody/tr")
        self.assertGreater(len(rows), 0)
        print('Age Filter Successfully Returned 1 Result')

        # Filter Age Test 2
        min_age_field = wait.until(EC.presence_of_element_located((By.ID, 'min-age')))
        min_age_field.clear()
        min_age_field.send_keys('20')
        max_age_field = wait.until(EC.presence_of_element_located((By.ID, 'max-age')))
        max_age_field.clear()
        max_age_field.send_keys('22')
        filter_button = wait.until(EC.element_to_be_clickable((By.ID, 'apply-filter')))
        filter_button.click()
        print('Filtered Age with 20-22')
        rows = self.selenium.find_elements(By.XPATH, "//table[@id='user-table']//tbody/tr")
        self.assertEqual(len(rows), 0)
        print('Age Filter Successfully Returned 0 Results')

        # Filter Clear
        reset_filter_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Reset Filter')]")))
        reset_filter_button.click()
        print('Filter Cleared')
        rows = self.selenium.find_elements(By.XPATH, "//table[@id='user-table']//tbody/tr")
        self.assertEqual(len(rows), 1)
        print('Filter Cleared Successfully Returned All Results')
        print('Filter Hobbies Test Passed')

    def test_05_send_friend_request(self):
        # Test Setup
        print('\n\n---Send Friend Request Test---')
        User = get_user_model()
        User.objects.create_user(**self.test_user_1)
        User.objects.create_user(**self.test_user_2)
        self.selenium.get(f'{self.live_server_url}/login/')
        wait = WebDriverWait(self.selenium, 10)
        
        # Login
        username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        username_field.send_keys(self.test_user_1['username'])
        password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
        password_field.send_keys(self.test_user_1['password'])
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
        submit_button.click()
        wait.until(EC.url_to_be(self.live_server_url + '/'))
        print('Logged in as User 1')

        # Navigate to the hobbies page
        hobbies_tab = wait.until(EC.element_to_be_clickable((By.ID, 'hobbies-link')))
        hobbies_tab.click()
        print('Navigated to Hobbies Page')

        # Send Friend Request
        friend_button = wait.until(EC.element_to_be_clickable((By.ID, 'send-friend-request')))
        friend_button.click()
        wait.until(EC.invisibility_of_element_located((By.ID, 'send-friend-request')))
        span_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'span')))
        self.assertEqual(span_element.text, 'Friend request sent')
        print('Friend Request Sent')
        print('Send Friend Request Test Passed')

    def test_06_accept_friend_request(self):
        # Test Setup
        print('\n\n---Accept Friend Request Test---')
        User = get_user_model()
        User.objects.create_user(**self.test_user_1)
        User.objects.create_user(**self.test_user_2)
        self.selenium.get(f'{self.live_server_url}/login/')
        wait = WebDriverWait(self.selenium, 10)
        
        # Login
        username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        username_field.send_keys(self.test_user_1['username'])
        password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
        password_field.send_keys(self.test_user_1['password'])
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
        submit_button.click()
        wait.until(EC.url_to_be(self.live_server_url + '/'))
        print('Logged in as User 1')

        # Navigate to the hobbies page
        hobbies_tab = wait.until(EC.element_to_be_clickable((By.ID, 'hobbies-link')))
        hobbies_tab.click()
        print('Navigated to Hobbies Page')

        # Send Friend Request
        friend_button = wait.until(EC.element_to_be_clickable((By.ID, 'send-friend-request')))
        friend_button.click()
        wait.until(EC.invisibility_of_element_located((By.ID, 'send-friend-request')))
        span_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'span')))
        self.assertEqual(span_element.text, 'Friend request sent')
        print('Friend Request Sent')

        # Log out
        logout_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-logout')))
        logout_button.click()
        wait.until(EC.url_to_be(self.live_server_url + '/login/'))
        print('Logged out as User 1')

        # Login as User 2
        username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        username_field.send_keys(self.test_user_2['username'])
        password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
        password_field.send_keys(self.test_user_2['password'])
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
        submit_button.click()
        wait.until(EC.url_to_be(self.live_server_url + '/'))
        print('Logged in as User 2')

        # Navigate to the friends page
        friends_tab = wait.until(EC.element_to_be_clickable((By.ID, 'friends-link')))
        friends_tab.click()
        print('Navigated to Friends Page')

        # Accept Friend Request
        accept_button = wait.until(EC.element_to_be_clickable((By.ID, 'accept-friend-request')))
        accept_button.click()
        wait.until(EC.invisibility_of_element_located((By.XPATH, f"//td[contains(text(), '{self.test_user_1['username']}')]")))
        print('Friend Request Accepted')

        friend_row = wait.until(EC.presence_of_element_located((By.XPATH, f"//td[contains(text(), '{self.test_user_1['username']}')]")))
        self.assertIsNotNone(friend_row)
        print('User1 now appears in current friends table')
