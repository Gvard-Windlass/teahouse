from django.test import TestCase, Client
from django.contrib.auth.models import User

from catalogue.models import Tea
from cart.models import Cart

class TestCartManager(TestCase):
    def setUp(self):
        self.client = Client()

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
        Tea.objects.create(
            name='test tea 2',
            price = 200.5,
            image = 'product_images/black2.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2021,
            tea_amount = 50.5
        )
        self.user = User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        Cart.objects.create(product=product, user=self.user, amount=200)

    
    def test_add_new_to_cart(self):
        Cart.objects.add_to_cart(2, self.user, 100)
        cart = self.user.cart_set.all()
        self.assertEqual(len(cart), 2)


    def test_add_existent_to_cart(self):
        Cart.objects.add_to_cart(1, self.user, 100)
        cart_item = Cart.objects.first()
        self.assertEqual(cart_item.amount, 100)
        
        Cart.objects.add_to_cart(1, self.user, 200, True)
        cart_item = Cart.objects.first()
        self.assertEqual(cart_item.amount, 300)