from django.test import TestCase, Client
from django.contrib.auth.models import User

from catalogue.models import Tea
from cart.models import Cart

class TestCartAddView(TestCase):
    def setUp(self):
        self.client = Client()


    def test_cart_add_view(self):
        User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        Tea.objects.create(
            name='test tea 1',
            price = 300,
            image = 'product_images/black1.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2022,
            amount = 300
        )
        form_data = {
            'amount': 10,
            'productId': 1,
            'nextPage': '/tea/1/'
        }
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))
        
        response = self.client.post('/cart_add/', data=form_data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(1, User.objects.first().cart_set.first().id)


class TestCartView(TestCase):
    def setUp(self):
        self.client = Client()


    def test_cart_view(self):
        User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))

        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)


class TestCartRemoveView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_cart_remove(self):
        user = User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        product = Tea.objects.create(
            name='test tea 1',
            price = 300,
            image = 'product_images/black1.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2022,
            amount = 300
        )
        Cart.objects.create(product=product, user=user, amount=200)

        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))
        
        response = self.client.post('/cart_remove/', data={'productId': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Cart.objects.all()), 0)