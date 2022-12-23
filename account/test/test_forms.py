from django.test import TestCase
from account.forms import CustomerRegistrationForm, UserForm, CustomerForm
from django.contrib.auth.models import User
from test.factories import UserFactory
from parameterized import parameterized


class TestRegistrationForm(TestCase):
    @parameterized.expand([
        ('gvard', 'Gvard', 'Windlass', '2000-1-1', 'test@example.com', 'Bk7^31&3LDXt', 'Bk7^31&3LDXt', True),
        ('gvard', '', '', '2000-1-1', 'test@example.com', 'Bk7^31&3LDXt', 'Bk7^31&3LDXt', True),
        # less than min length
        ('g', 'Gvard', 'Windlass', '2000-1-1', 'test@example.com', 'Bk7^31&3LDXt', 'Bk7^31&3LDXt', False),
        ('gvard', 'G', 'Windlass', '2000-1-1', 'test@example.com', 'Bk7^31&3LDXt', 'Bk7^31&3LDXt', False),
        ('gvard', 'Gvard', 'W', '2000-1-1', 'test@example.com', 'Bk7^31&3LDXt', 'Bk7^31&3LDXt', False),
        # password mismatch
        ('gvard', 'Gvard', 'Windlass', '2000-1-1', 'test@example.com', 'Bk7^31&3LDXt', 'Bk731&3LDXt', False),
        # incorrent email format
        ('gvard', 'Gvard', 'Windlass', '2000-1-1', 'test.example.com', 'Bk7^31&3LDXt', 'Bk7^31&3LDXt', False),
        # incorrect date format
        ('gvard', 'Gvard', 'Windlass', '1-1-2000', 'test.example.com', 'Bk7^31&3LDXt', 'Bk7^31&3LDXt', False),
        # weak password
        ('gvard', 'Gvard', 'Windlass', '2000-1-1', 'test@example.com', '123', '123', False),
    ])
    def test_register_customer(self, username, first_name, last_name, birthday, email, pass1, pass2, validity):
        form_data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'birthday': birthday,
            'email': email,
            'password1': pass1,
            'password2': pass2
        }
        form = CustomerRegistrationForm(data=form_data)
        self.assertEqual(form.is_valid(), validity)
        if validity:
            form.save()
            user = User.objects.get(username='gvard')
            self.assertEqual(str(user.customer.birthday), '2000-01-01')


class TestUserForm(TestCase):
    @parameterized.expand([
        ('gvard', 'Gvard', 'Windlass', 'test@example.com', True),
        ('gvard', '', '', 'test@example.com', True),
        ('g', 'Gvard', 'Windlass', 'test@example.com', False),
        ('gvard', 'G', 'Windlass', 'test@example.com', False),
        ('gvard', 'Gvard', 'W', 'test@example.com', False),
    ])
    def test_update_user(self, username, first_name, last_name, email, validity):
        user = UserFactory.create()

        form_data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }

        form = UserForm(data=form_data, instance=user)
        self.assertEqual(form.is_valid(), validity)
        if validity:
            form.save()
            user = User.objects.get(username='gvard')
            self.assertEqual(user.email, 'test@example.com')


class TestCustomerForm(TestCase):
    def test_update_customer(self):
        user = UserFactory.create()
        user.customer.birthday = '2000-01-01'
        user.save()

        form = CustomerForm(data={'birthday': '2000-12-12'}, instance=user.customer)
        self.assertTrue(form.is_valid())
        form.save()
        user = User.objects.get(username='gvard')
        self.assertEqual(str(user.customer.birthday), '2000-12-12')