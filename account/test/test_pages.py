from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# NOTE: flashes page 404 in the beginning of tests, expected behavior
from seleniumlogin import force_login

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User, AnonymousUser
from django.test import Client
from django.contrib import auth

firefox_dev_binary = FirefoxBinary('C:\Program Files\Firefox Developer Edition\\firefox.exe')
driver_path = 'C:\Dev\django_dev_1\geckodriver.exe'

class TestRegistrationPage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=firefox_dev_binary, executable_path=driver_path)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    
    def test_registration_success(self):
        self.selenium.get(f'{self.live_server_url}/register')
        username_input = self.selenium.find_element(By.ID, 'id_username')
        first_name_input = self.selenium.find_element(By.ID, 'id_first_name')
        last_name_input = self.selenium.find_element(By.ID, 'id_last_name')
        birthday_input = self.selenium.find_element(By.ID, 'id_birthday')
        email_input = self.selenium.find_element(By.ID, 'id_email')
        password1_input = self.selenium.find_element(By.ID, 'id_password1')
        password2_input = self.selenium.find_element(By.ID, 'id_password2')
        submit_button = self.selenium.find_element(By.ID, 'auth-submit')

        username_input.send_keys('gvard')
        first_name_input.send_keys('Gvard')
        last_name_input.send_keys('Windlass')
        birthday_input.send_keys('2000-1-1')
        email_input.send_keys('test@example.com')
        password1_input.send_keys('Bk7^31&3LDXt')
        password2_input.send_keys('Bk7^31&3LDXt')

        # button.click() results in error, 'cant scroll into view'
        submit_button.send_keys(Keys.RETURN)

        current_url = self.selenium.current_url
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))
       
        user = User.objects.get(username='gvard')
        self.assertEqual(str(user.customer.birthday), '2000-01-01')


class TestLoginPage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=firefox_dev_binary, executable_path=driver_path)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self): 
        self.client = Client()

    
    def test_login_success(self):
        User.objects.create_user(username='gvard', password='Bk7^31&3LDXt').save()
        # can't achieve unit tests to be able to actually say if user is logged in or not,
        # despite template react accordingly in screenshots, thus, this line is likely redundant
        self.assertIsInstance(auth.get_user(self.client), AnonymousUser)

        self.selenium.get(f'{self.live_server_url}/login')
        username_input = self.selenium.find_element(By.ID, 'id_username')
        password_input = self.selenium.find_element(By.ID, 'id_password')
        submit_button = self.selenium.find_element(By.ID, 'auth-submit')

        username_input.send_keys('gvard')
        password_input.send_keys('Bk7^31&3LDXt')
        submit_button.send_keys(Keys.RETURN)

        current_url = self.selenium.current_url
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        # correct redirect is seemingly the only way to tell that login is a success
        self.assertEqual(self.selenium.current_url, f'{self.live_server_url}/')


class TestProfilePage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=firefox_dev_binary, executable_path=driver_path)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_user_update(self):
        user = User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        user.customer.birthday = '2000-01-01'
        user.save()
        force_login(user, self.selenium, self.live_server_url)

        # test profile
        self.selenium.get(f'{self.live_server_url}/profile')
        
        username_input = self.selenium.find_element(By.ID, 'id_username')
        self.assertEqual(username_input.get_attribute('value'), 'gvard')

        first_name_input = self.selenium.find_element(By.ID, 'id_first_name')
        last_name_input = self.selenium.find_element(By.ID, 'id_last_name')
        email_input = self.selenium.find_element(By.ID, 'id_email')
        submit_button = self.selenium.find_element(By.ID, 'user-update-submit')

        first_name_input.send_keys('Gvard')
        last_name_input.send_keys('Windlass')
        email_input.send_keys('test@example.com')
        submit_button.send_keys(Keys.RETURN)

        current_url = self.selenium.current_url
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        user = User.objects.get(username='gvard')
        self.assertEqual(user.email, 'test@example.com')


class TestPasswordChangePage(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=firefox_dev_binary, executable_path=driver_path)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_password_chage(self):
        user = User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        force_login(user, self.selenium, self.live_server_url)

        # test password change
        self.selenium.get(f'{self.live_server_url}/profile/password')
        old_password_input = self.selenium.find_element(By.ID, 'id_old_password')
        new_password1_input = self.selenium.find_element(By.ID, 'id_new_password1')
        new_password2_input = self.selenium.find_element(By.ID, 'id_new_password2')
        submit_button = self.selenium.find_element(By.ID, 'password-change-submit')

        old_password_input.send_keys('Bk7^31&3LDXt')
        new_password1_input.send_keys('aA9590Ak$^yo')
        new_password2_input.send_keys('aA9590Ak$^yo')
        submit_button.send_keys(Keys.RETURN)

        current_url = self.selenium.current_url
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))
        self.selenium.save_screenshot('C:\Dev\django_dev_1\selenium_screenshots\\new.png')
