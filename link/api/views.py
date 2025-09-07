from rest_framework.views import APIView
from rest_framework import permissions, authentication, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

import datetime
import json
from link.api.fs import File

class CreateDataSet(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        if not ("metadata" in request.data and "file" in request.FILES):
            response = {
                'status':status.HTTP_400_BAD_REQUEST,
            }
            return Response(response)
        meta = request.data.get('metadata')
        data = json.loads(meta)
        file = request.FILES.get('file')

        response = {}
        FILE = File(file, data)
        FILE.write_temp()
        FILE.read_file()

        if FILE.report != {}:
            response['report'] = FILE.report
            response['msg'] = f"File processed"
            response['status'] = status.HTTP_200_OK
        else:
            response['msg'] = f"File cannot be process"
            response['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(response)

    def get(self, request):
        response = {
            'status':status.HTTP_405_METHOD_NOT_ALLOWED,
        }
        return Response(response)

class DeleteDataSet(APIView):
    def post(self, request):
        response = {
            'status':status.HTTP_405_METHOD_NOT_ALLOWED,
        }
        return Response(response)
    def get(self, request):
        response = {
            'status':status.HTTP_200_OK,
        }
        return Response(response)

class AddRecord(APIView):
    def post(self, request):
        return HttpResponse("data accepted", status=200)
    def get(self, request):
        return HttpResponse("adding must be a post request", status=200)

class DeleteRecord(APIView):
    def post(self, request):
        return HttpResponse("this shouldn't be a post method", status=200)
    def get(self, request):
        return HttpResponse("deleting process", status=200)

class RetrieveRecord(APIView):
    def post(self, request):
        return HttpResponseNotAllowed(['GET']) 
    def get(self, request):
        return HttpResponse("retrieving record", status=200)
