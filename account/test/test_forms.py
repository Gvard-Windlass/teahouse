from django.test import TestCase
from account.forms import CustomerRegistrationForm, UserForm, CustomerForm
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


class TestUserForm(TestCase):
    def test_update_user(self):
        user = User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')

        form_data = {
            'username': 'gvard',
            'first_name': 'Gvard',
            'last_name': 'Windlass',
            'email': 'test@example.com'
        }

        form = UserForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        user = User.objects.get(username='gvard')
        self.assertEqual(user.email, 'test@example.com')


class TestCustomerForm(TestCase):
    def test_update_customer(self):
        user = User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        user.customer.birthday = '2000-01-01'
        user.save()

        form = CustomerForm(data={'birthday': '2000-12-12'}, instance=user.customer)
        self.assertTrue(form.is_valid())
        form.save()
        user = User.objects.get(username='gvard')
        self.assertEqual(str(user.customer.birthday), '2000-12-12')