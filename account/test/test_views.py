from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()

class TestRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_register_view(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)


class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_register_view(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)


class TestLogoutView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_logout_view(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)


class TestProfileView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_profile_view_authorized(self):
        User.objects.create_user(username='gvard', password='Bk7^31&3LDXt')
        self.assertTrue(self.client.login(username='gvard', password='Bk7^31&3LDXt'))
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    
    def test_profile_view_anonymous(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)