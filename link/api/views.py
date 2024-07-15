from rest_framework.views import APIView
from rest_framework import permissions, authentication

from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

import datetime

class CreateDataSet(APIView):
    def post(self, request):
        if request.POST:
            data        = request.POST
            username    = data.get('username')
            email       = data.get('email')

            return HttpResponse('accessed', status=200)
        else:
            return HttpResponse("there's not data", status=200)

class DeleteDataSet(APIView):
    def post(self, request):
        return HttpResponse("not found get method for the link", status=404)
    def get(self, request):
        return HttpResponse("deleting", status=200)
    
