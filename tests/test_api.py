from django.test import TestCase
from django.urls import reverse, resolve

class APITests(TestCase):
    def test_pushing_data(self):
        response = self.client.post(reverse('linkapp:create-set'))
        self.assertEqual(response.status_code, 200)
    def test_deleting_data(self):
        response = self.client.get(reverse('linkapp:delete-set'))
        self.assertEqual(response.status_code, 200)
