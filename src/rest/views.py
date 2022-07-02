from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response


class TestView(APIView):
    def get(self, request):
        return Response({'response': 'This is a test REST API response'})
