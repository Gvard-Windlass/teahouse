from django.test import TestCase, Client
from django.contrib.auth.models import User

from catalogue.models import Tea

class TestCartAddView(TestCase):
    def setUp(self):
        self.client = Client()


    def test_cart_add_view(self):
        User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        Tea.objects.create(
            name='test tea 1',
            price = 300.5,
            image = 'product_images/black1.jpg',
            description = 'tea for testing',
            product_type = 'Tea',
            tea_type = 'Black',
            tea_year = 2022,
            tea_amount = 300.5
        )
        form_data = {
            'amount': 10,
            'teaId': 1,
            'nextPage': '/tea/1/'
        }
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))
        
        response = self.client.post('/cart_add/', data=form_data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(1, User.objects.first().cart_set.first().id)
