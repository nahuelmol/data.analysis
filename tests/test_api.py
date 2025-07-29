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
from link.api.fs import FileReader
from link.api.grapher import do2dGraph

def success(msg):
    print(msg + ' -> ' + f"\033[32m PASSED\033[0m")

def err(msg):
    print(msg + ' -> ' + f"\033[31m FAILED\033[0m")

class APITests(TestCase):
    def test_api_dj(self):
        # testing requests
        factory = APIRequestFactory()
        #filepath = "tests/Line_301_PSTM_Stack_Enh.segy"
        filepath = "tests/NBA_2324_players.csv"
        file = ''
        with open(filepath, 'rb') as f:
            file_data = f.read()
            base64_data = base64.b64encode(file_data).decode('utf-8')
            file = base64_data
        data = {
                'email':'molinahuel44@gmail.com',
                'username':'nahuelmol',
                'file':file,
                'filekind':'csv',
                'target':'RANK',
                'ncomps':2,
                'pca': True,
                'ica': False,
                'complete':False,
                'basics': False,
                'ydata':'PPG',
                'xdata':'AGE',
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
        #filepath = "tests/Line_301_PSTM_Stack_Enh.segy"
        filepath = "tests/NBA_2324_players.csv"
        str_file = ''
        with open(filepath, 'rb') as f:
            file_data = f.read()
            str_file = base64.b64encode(file_data).decode('utf-8')
            with open('data.txt', 'w') as writein:
                writein.write(str_file)
        data = {
                'username':'nahuel',
                'email':'molinahuel44@gmail.com',
                'file':str_file,
                'filekind':'csv',
                'pca': 1,
                'ica': 0,
                'complete':0,
                'basics': 0,
                'target': 'RANK',
                'ncomps': 2
        }
        url = reverse('linkapp:create-set'),
        response = client.post( url,
                                data=data,
                                format='json')
        msg = f"response from  {url}"
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

    def test_file_reader(self):
        filepath = "tests/Line_301_PSTM_Stack_Enh.segy"
        file_str = ''
        with open(filepath, 'rb') as f:
            file_data = f.read()
            file_str = base64.b64encode(file_data).decode('utf-8')
        res, image = FileReader(file_str)
        msg = "FileReader"
        if res:
            ext = type(image)
            success(msg)
        else:
            msg = f"not a file worked"
            err(msg)
    def test_2d_graph(self):
        import pandas as pd
        data = [
                {"lat":-34.6037,    "lon":-58.3816,     "temperature":22.5},
                {"lat":-34.6090,    "lon":-58.3845,     "temperature":28.1},
                {"lat":-34.6123,    "lon":-58.3901,     "temperature":30.2},
                {"lat":-34.6167,    "lon":-58.3932,     "temperature":18.7},
                {"lat":-34.6200,    "lon":-58.3970,     "temperature":20.3}
            ]
        with_progresiva, json_res = do2dGraph(pd.DataFrame(data), 'temperature')
        if(isinstance(with_progresiva['progresiva'], pd.Series)): 
            success('it has a progresiva now')
        else:
            err('some or both datasets are not lists')

        json_dict = json.loads(json_res)
        if(isinstance(json_dict, dict)):
            msg = f"{json_dict['name']} creation"
            if (json_dict['name']):
                if (json_dict['image_base64'] is not None):
                    success(msg)
                else:
                    err(msg)
            else:
                err(msg)

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
