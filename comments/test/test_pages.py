from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from seleniumlogin import force_login

from catalogue.models import Tea
from test.factories import TeaFactory
from comments.models import Comment

import test.selenium_setup as setup

class TestCommentsDisplay(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=FirefoxBinary(setup.FIREFOX_BINARY_PATH), executable_path=setup.DRIVER_PATH)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_comments_display(self):
        product = TeaFactory.create()
        product2 = TeaFactory.create()

        alice = User.objects.create_user(username='alice')
        bob = User.objects.create_user(username='bob')
        Comment.objects.create(
            user = alice,
            product = product,
            text = 'comment by alice 1'
        )
        bob_comment = Comment.objects.create(
            user = bob,
            product = product,
            text = 'comment by bob 1'
        )
        Comment.objects.create(
            user = alice,
            product = product,
            text = 'reply by alice 1',
            parent = bob_comment
        )
        Comment.objects.create(
            user = bob,
            product = product2,
            text = 'comment by bob for other product'
        )

        # selenium retains pk increase between different classes?
        self.selenium.get(f'{self.live_server_url}/tea/{product.pk}/')
        comments = self.selenium.find_elements(By.CLASS_NAME, 'card')
        replies = self.selenium.find_elements(By.CSS_SELECTOR, '.replies .card')

        self.assertEqual(len(comments), 3)
        self.assertEqual(len(replies), 1)


class TestAddComment(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=FirefoxBinary(setup.FIREFOX_BINARY_PATH), executable_path=setup.DRIVER_PATH)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self) -> None:
        self.tea = TeaFactory.create()
        self.user = User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')


    def test_comment_post_success(self):
        force_login(self.user, self.selenium, self.live_server_url)

        self.selenium.get(f'{self.live_server_url}/tea/{self.tea.id}/')

        comment_input = self.selenium.find_element(By.ID, 'id_text')
        submit_button = self.selenium.find_element(By.ID, 'add-comment')

        comment_input.send_keys('test comment')
        submit_button.click()        

        WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card')))
        comment = self.selenium.find_element(By.CLASS_NAME, 'card-text')

        self.assertEqual(comment.text, 'test comment')


    def test_add_reply(self):
        bob = User.objects.create_user(username='bob')
        Comment.objects.create(
            user = bob,
            product = self.tea,
            text = 'comment by bob'
        )
        force_login(self.user, self.selenium, self.live_server_url)
        self.selenium.get(f'{self.live_server_url}/tea/{self.tea.id}/')

        comment_card = self.selenium.find_element(By.CLASS_NAME, 'card')
        action = ActionChains(self.selenium)
        action.move_to_element(comment_card).perform()
        WebDriverWait(self.selenium, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-reply')))

        reply_button = self.selenium.find_element(By.CLASS_NAME, 'btn-reply')
        reply_button.click()
        
        reply_input = self.selenium.find_element(By.CSS_SELECTOR, '.reply-form #id_text')
        add_reply_button = self.selenium.find_element(By.CSS_SELECTOR, '.reply-form #add-comment')
        
        reply_input.send_keys('test reply')
        add_reply_button.send_keys(Keys.RETURN)
        WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'replies')))

        self.assertEqual(len(self.selenium.find_elements(By.CLASS_NAME, 'card')), 2)