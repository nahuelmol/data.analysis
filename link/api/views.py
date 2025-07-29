from rest_framework.views import APIView
from rest_framework import permissions, authentication, status
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
        data        = request.data
        username    = data.get('username')
        email       = data.get('email')
        filedata    = data.get('file')
        filekind    = data.get('filekind')
        pca         = data.get('pca')
        ica         = data.get('ica')
        complete    = data.get('complete')
        basics      = data.get('basics')
        ydata       = data.get('ydata')
        xdata       = data.get('xdata')
        process     = ''
        params      = {}
        params['ydata'] = ydata
        params['xdata'] = xdata
        if(pca == 1):
            process = 'pca'
            params['target'] = data.get('target')
            params['ncomps'] = data.get('ncomps')
            params['process'] = 'pca'
        elif (ica == 1):
            process = 'ica'
            params['target'] = data.get('target')
            params['ncomps'] = data.get('ncomps')
            params['process'] = 'ica'
        elif (complete == 1):
            process = 'complete'
            params['target'] = data.get('target')
            params['ncomps'] = data.get('ncomps')
            params['process'] = 'complete'
        elif (basics == 1):
            process = 'basics'
            params['target']    = data.get('target')
            params['process']   = 'basics'
        else:
            process = ''

        MSG = "hello " + username
        response = {
                'msg':MSG,
                'data':None,
                'status':status.HTTP_200_OK,
                'process':process,
                'filekind':filekind
        }
        worked, report = FileReader(filedata, params)
        print("report:", report)
        if worked:
            response['report'] = report
        else:
            response['msg'] = f"File cannot be process"
        return Response(response)
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
