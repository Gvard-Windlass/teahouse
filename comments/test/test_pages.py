from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from seleniumlogin import force_login

from catalogue.models import Tea
from comments.models import Comment

firefox_dev_binary = FirefoxBinary('C:\Program Files\Firefox Developer Edition\\firefox.exe')
driver_path = 'C:\Dev\django_dev_1\geckodriver.exe'

class TestCommentsDisplay(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver(firefox_binary=firefox_dev_binary, executable_path=driver_path)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_comments_display(self):
        product = Tea.objects.create(
            name='test tea 1',
            price = 300.5,
            image = 'product_images/black1.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2022,
            tea_amount = 300.5
        )
        product2 = Tea.objects.create(
            name='test tea 2',
            price = 200.5,
            image = 'product_images/black2.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2021,
            tea_amount = 50.5
        )

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
        cls.selenium = WebDriver(firefox_binary=firefox_dev_binary, executable_path=driver_path)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_comment_post_success(self):
        tea = Tea.objects.create(
            name='test tea 1',
            price = 300.5,
            image = 'product_images/black1.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2022,
            tea_amount = 300.5
        )
        user = User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        force_login(user, self.selenium, self.live_server_url)

        self.selenium.get(f'{self.live_server_url}/tea/{tea.id}/')

        comment_input = self.selenium.find_element(By.ID, 'id_text')
        submit_button = self.selenium.find_element(By.ID, 'add-comment')

        comment_input.send_keys('test comment')
        submit_button.click()        

        WebDriverWait(self.selenium, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'card')))
        comment = self.selenium.find_element(By.CLASS_NAME, 'card-text')

        self.assertEqual(comment.text, 'test comment')