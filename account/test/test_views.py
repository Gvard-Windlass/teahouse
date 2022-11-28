from django.test import TestCase, Client


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