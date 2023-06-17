from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# NOTE: flashes page 404 in the beginning of tests, expected behavior
from seleniumlogin import force_login
import re

from django.core import mail
from django.contrib.auth.models import User, AnonymousUser
from django.test import Client
from django.contrib import auth
from django.urls import reverse

from test.factories import UserFactory
from test.selenium_setup import SeleniumWithFirefox


class TestRegistrationPage(SeleniumWithFirefox):
    def test_registration_success(self):
        url = reverse("register")
        self.selenium.get(self.live_server_url + url)
        username_input = self.selenium.find_element(By.ID, "id_username")
        first_name_input = self.selenium.find_element(By.ID, "id_first_name")
        last_name_input = self.selenium.find_element(By.ID, "id_last_name")
        birthday_input = self.selenium.find_element(By.ID, "id_birthday")
        email_input = self.selenium.find_element(By.ID, "id_email")
        password1_input = self.selenium.find_element(By.ID, "id_password1")
        password2_input = self.selenium.find_element(By.ID, "id_password2")
        submit_button = self.selenium.find_element(By.ID, "auth-submit")

        username_input.send_keys("gvard")
        first_name_input.send_keys("Gvard")
        last_name_input.send_keys("Windlass")
        birthday_input.send_keys("2000-01-01")
        email_input.send_keys("test@example.com")
        password1_input.send_keys("Bk7^31&3LDXt")
        password2_input.send_keys("Bk7^31&3LDXt")

        # button.click() results in error, 'cant scroll into view'
        submit_button.send_keys(Keys.RETURN)

        current_url = self.selenium.current_url
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        user = User.objects.get(username="gvard")
        self.assertEqual(str(user.customer.birthday), "2000-01-01")


class TestLoginPage(SeleniumWithFirefox):
    def setUp(self):
        self.client = Client()

    def test_login_success(self):
        UserFactory.create()
        # can't achieve unit tests to be able to actually say if user is logged in or not,
        # despite template react accordingly in screenshots, thus, this line is likely redundant
        self.assertIsInstance(auth.get_user(self.client), AnonymousUser)

        url = reverse("login")
        self.selenium.get(self.live_server_url + url)
        username_input = self.selenium.find_element(By.ID, "id_username")
        password_input = self.selenium.find_element(By.ID, "id_password")
        submit_button = self.selenium.find_element(By.ID, "auth-submit")

        username_input.send_keys("gvard")
        password_input.send_keys("Bk7^31&3LDXt")
        submit_button.send_keys(Keys.RETURN)

        current_url = self.selenium.current_url
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        # correct redirect is seemingly the only way to tell that login is a success
        self.assertEqual(self.selenium.current_url, f"{self.live_server_url}/")


class TestProfilePage(SeleniumWithFirefox):
    def test_user_update(self):
        user = UserFactory.create(email=None)
        user.customer.birthday = "2000-01-01"
        user.save()
        force_login(user, self.selenium, self.live_server_url)

        # test profile
        url = reverse("profile")
        self.selenium.get(self.live_server_url + url)

        username_input = self.selenium.find_element(By.ID, "id_username")
        self.assertEqual(username_input.get_attribute("value"), "gvard")

        first_name_input = self.selenium.find_element(By.ID, "id_first_name")
        last_name_input = self.selenium.find_element(By.ID, "id_last_name")
        email_input = self.selenium.find_element(By.ID, "id_email")
        submit_button = self.selenium.find_element(By.ID, "user-update-submit")

        first_name_input.send_keys("Gvard")
        last_name_input.send_keys("Windlass")
        email_input.send_keys("test@example.com")
        submit_button.send_keys(Keys.RETURN)

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert"))
        )
        alert = self.selenium.find_element(By.CLASS_NAME, "alert")
        self.assertIn("alert-success", alert.get_attribute("class"))

        user = User.objects.get(username="gvard")
        self.assertEqual(user.email, "test@example.com")


class TestPasswordChangePage(SeleniumWithFirefox):
    def test_password_chage(self):
        user = UserFactory.create()
        force_login(user, self.selenium, self.live_server_url)

        # test password change
        url = reverse("password_change")
        self.selenium.get(self.live_server_url + url)
        old_password_input = self.selenium.find_element(By.ID, "id_old_password")
        new_password1_input = self.selenium.find_element(By.ID, "id_new_password1")
        new_password2_input = self.selenium.find_element(By.ID, "id_new_password2")
        submit_button = self.selenium.find_element(By.ID, "password-change-submit")

        old_password_input.send_keys("Bk7^31&3LDXt")
        new_password1_input.send_keys("aA9590Ak$^yo")
        new_password2_input.send_keys("aA9590Ak$^yo")
        submit_button.send_keys(Keys.RETURN)

        current_url = self.selenium.current_url
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))
        self.selenium.save_screenshot(
            "C:\\Dev\\django_dev_1\\selenium_screenshots\\new.png"
        )


class TestPasswordResetPages(SeleniumWithFirefox):
    def test_password_reset(self):
        UserFactory.create()

        # ask for password reset
        url = reverse("password_reset")
        self.selenium.get(self.live_server_url + url)

        reset_email = self.selenium.find_element(By.ID, "id_email")
        reset_butotn = self.selenium.find_element(By.ID, "reset-submit")

        current_url = self.selenium.current_url
        reset_email.send_keys("test@example.com")
        reset_butotn.click()

        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))
        self.assertEqual(
            self.selenium.current_url, f"{self.live_server_url}/password_reset_done/"
        )

        # go to password reset url and submit new password
        reset_link = re.search(
            re.compile("^http.+$", re.MULTILINE), mail.outbox[0].body
        )
        self.assertTrue(reset_link)

        self.selenium.get(reset_link.group())

        new_password_input1 = self.selenium.find_element(By.ID, "id_new_password1")
        new_password_input2 = self.selenium.find_element(By.ID, "id_new_password2")
        submit_button = self.selenium.find_element(By.ID, "submit-button")

        current_url = self.selenium.current_url
        new_password = "aA9590Ak$^yo"
        new_password_input1.send_keys(new_password)
        new_password_input2.send_keys(new_password)
        submit_button.click()

        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))
        self.assertEqual(
            self.selenium.current_url,
            f"{self.live_server_url}/password_reset_complete/",
        )

        # login with new password
        url = reverse("login")
        self.selenium.get(self.live_server_url + url)
        username_input = self.selenium.find_element(By.ID, "id_username")
        password_input = self.selenium.find_element(By.ID, "id_password")
        submit_button = self.selenium.find_element(By.ID, "auth-submit")

        username_input.send_keys("gvard")
        password_input.send_keys(new_password)
        submit_button.send_keys(Keys.RETURN)

        current_url = self.selenium.current_url
        WebDriverWait(self.selenium, 10).until(EC.url_changes(current_url))

        self.assertEqual(self.selenium.current_url, f"{self.live_server_url}/")
