from django.test import TestCase, Client
from django.urls import reverse
from test.factories import UserFactory

class TestRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_register_view(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_register_view(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestLogoutView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_logout_view(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class TestProfileView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('profile')

    
    def test_profile_view_authorized(self):
        UserFactory.create()
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    
    def test_profile_view_anonymous(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class TestPasswordChangeView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_password_change_view(self):
        UserFactory.create()
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))
        
        url = reverse('password_change')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestPasswordChangeDoneView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_password_change_done_view(self):
        UserFactory.create()
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))
        
        form_data = {
            'old_password': 'Bk7^31&3LDXt',
            'new_password1': 'aA9590Ak$^yo',
            'new_password2': 'aA9590Ak$^yo',
        }
        url = reverse('password_change')
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)