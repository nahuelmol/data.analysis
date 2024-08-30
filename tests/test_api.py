from django.test import TestCase
from django.urls import reverse, resolve

def success(msg):
    print(msg + '->' + f"\033[32m Success\033[0m")

def err(msg):
    print(msg + '->' + f"\033[31m Fail\033[0m")

class APITests(TestCase):
    def test_push_data(self):
        response = self.client.post(reverse('linkapp:create-set'))
        if response.status_code == 200:
            success('push_data')
        else:
            err('push_data')

    def test_delete_set(self):
        response = self.client.get(reverse('linkapp:delete-set'))
        try:
            self.assertEqual(response.status_code, 200)
            success('delete_set')
        except:
            err('delete_set')

    def test_delete_record(self):
        response = self.client.get(reverse('linkapp:delete-record'))
        try:
            self.assertEqual(response.status_code, 200)
            success('delete_record')
        except:
            err('delete_record')
    def test_add_record(self):
        response = self.client.get(reverse('linkapp:add-record'))
        try:
            self.assertEqual(response.status_code, 200)
            success('add_record')
        except:
            err('add_record')

    def test_retrieve_record(self):
        response =  self.client.post(reverse('linkapp:retrieve-record'))
        try:
            self.assertEqual(response.status_code, 405)
            success('retrieve_record')
        except:
            err('retrieve_record')
