from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from rest import serializers

class TestView(APIView):
    def get(self, request):
        return Response({'response': 'This is a test REST API response'})

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CsrfTokenView(APIView):
    def get(self, request):
        return Response({'csrftoken': 'set in the cookie'})

@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        username = data['login']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'result': 'success'})

        raise ParseError("invalid credentials")

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'result': 'success'})

class AccountView(RetrieveAPIView):
    serializer_class = serializers.AccountSerializer

    def get_object(self):
        return self.request.user
