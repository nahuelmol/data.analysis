from rest_framework.views import APIView
from rest_framework import permissions, authentication 
from rest_framework.response import Response

from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

import datetime
from link.api.fs import FileReader

class CreateDataSet(APIView):
    def post(self, request):
        if request.POST:
            data        = request.POST
            username    = data.get('username')
            email       = data.get('email')
            filedata    = data.get('file')
            MSG = "hello " + username
            response = {
                    'msg':MSG,
                    'data':None,
                    'status':status.HTTP_200_OK
            }
            image, worked = FileReader(filedata)
            if worked:
                response['data'] = image
            else:
                response['msg'] = f"File cannot be process"
            return Response(response)
        else:
            response = {
                    'msg':"there's not data to work with"
            }
            return Response(response)
            #return HttpResponse("there's not data to work with", status=200)
    def get(self, request):
        message = {
                'error':'not allowed method GET'
        }
        return Response(message)

class DeleteDataSet(APIView):
    def post(self, request):
        return HttpResponse("not found get method for the link", status=404)
    def get(self, request):
        return HttpResponse("deleting", status=200)


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
