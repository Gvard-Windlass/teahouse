from django.test import TestCase
from account.forms import CustomerRegistrationForm
from django.contrib.auth.models import User


class TestRegistrationForm(TestCase):
    def test_register_customer(self):
        form_data = {
            'username': 'gvard',
            'first_name': 'Gvard',
            'last_name': 'Windlass',
            'birthday': '2000-1-1',
            'email': 'test@example.com',
            'password1': 'Bk7^31&3LDXt',
            'password2': 'Bk7^31&3LDXt'
        }
        form = CustomerRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        user = User.objects.get(username='gvard')
        self.assertEqual(str(user.customer.birthday), '2000-01-01')
