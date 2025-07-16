import base64
import json
from io import BytesIO
import filetype

from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.request import Request
from django.http import HttpRequest 
from rest_framework.settings import api_settings
from rest_framework.parsers import JSONParser

from link.api.views import CreateDataSet
from link.api.unziper import unzip

def success(msg):
    print(msg + ' -> ' + f"\033[32m Success\033[0m")

def err(msg):
    print(msg + ' -> ' + f"\033[31m Fail\033[0m")

class APITests(TestCase):
    def test_api_dj(self):
        # testing requests
        factory = APIRequestFactory()
        filepath = "tests/Line_301_PSTM_Stack_Enh.segy"
        file = ''
        with open(filepath, 'rb') as f:
            file_data = f.read()
            base64_data = base64.b64encode(file_data).decode('utf-8')
            file = base64_data
        data = {
                'username':'nahuelmol',
                'file':file
                }
        url = reverse('linkapp:create-set')
        request = factory.post(
                url,
                data=json.dumps(data),
                content_type='application/json'
                )
        req = Request(request)
        parser = JSONParser()
        parser_context = {
                'request':req,
                'encoding': 'utf-8'
                }
        msg = f"requesting to {url}"
        #if req.method == 'POST':
        #    req_data = parser.parse(req.stream, parser_context)
        #    if req_data.get('username'):
        #        if req_data.get('file'):
        #            success(msg)
        #else:
        #    err(msg)

        view = CreateDataSet.as_view()
        response = view(request)
        msg = 'CreateDataSet view'
        if(response.status_code == 200):
            msg = f"{msg} : {response.data['msg']}"
            success(msg)
        else:
            err(msg)
            

    def test_push_data(self):
        # testing as a common post
        client = APIClient()
        filepath = "tests/Line_301_PSTM_Stack_Enh.segy"
        file = ''
        with open(filepath, 'rb') as f:
            file_data = f.read()
            base64_data = base64.b64encode(file_data).decode('utf-8')
            file = base64_data
        data = {
                'username':'nahuel',
                'email':'molinahuel44@gmail.com',
                'file':file,
                }
        url = reverse('linkapp:create-set'),
        response = client.post( url,
                                data=data,
                                format='json')
        msg = f"response from  {url}"
        print(response)
        if response.status_code == 200:
            success(msg)
        else:
            msg = f"{msg}:\nstatus code: {response.status_code}"
            err(msg)
    def test_unziper(self):
        filepath = "tests/ninja.zip"
        file = ''
        with open(filepath, 'rb') as f:
            file_data = f.read()
            base64_data = base64.b64encode(file_data).decode('utf-8')
            file = base64_data
        res, cnt = unzip(file)
        if res:
            if (filetype.guess(cnt).extension == 'str'):
                success('correct received file type')
            else:
                err('wrong file type received')
        else:
            err('something went wrong')

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
