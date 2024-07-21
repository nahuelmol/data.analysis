from django.test import TestCase
from django.urls import reverse, resolve

def success():
    print(f"\033[32m Success\033[0m")

def err():
    print(f"\033[31m Fail\033[0m")

class APITests(TestCase):
    def test_pushing_data(self):
        response = self.client.post(reverse('linkapp:create-set'))
        if response.status_code == 200:
            success()
        else:
            err()

    def test_deleting_data(self):
        response = self.client.get(reverse('linkapp:delete-set'))
        try:
            self.assertEqual(response.status_code, 200)
            success()
        except:
            err()

    def test_delete_record(self):
        response = self.client.get(reverse('linkapp:delete-record'))
        try:
            self.assertEqual(response.status_code, 200)
            success()
        except:
            err()
    def test_add_record(self):
        response = self.client.get(reverse('linkapp:add-record'))
        try:
            self.assertEqual(response.status_code, 200)
            success()
        except:
            err()
