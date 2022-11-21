from django.test import TestCase, Client


class TestTeaListView(TestCase):
    def setUp(self):
        self.client = Client()

    
    def test_tea_list_view_specific(self):
        response = self.client.get('/tea/Black/')
        self.assertEqual(response.status_code, 200)


    def test_tea_list_view_all(self):
        response = self.client.get('/tea/')
        self.assertEqual(response.status_code, 200)