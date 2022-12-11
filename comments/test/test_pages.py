from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

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

        self.selenium.get(f'{self.live_server_url}/tea/1/')
        comments = self.selenium.find_elements(By.CLASS_NAME, 'card')
        replies = self.selenium.find_elements(By.CSS_SELECTOR, '.replies .card')

        self.assertEqual(len(comments), 3)
        self.assertEqual(len(replies), 1)