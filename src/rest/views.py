from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from graphene_django.views import GraphQLView as OriginalGraphQLView

from rest import serializers

class TestView(APIView):
    def get(self, request):
        return Response({'response': 'This is a test REST API response'})

class GraphQLView(OriginalGraphQLView):
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == 'options':
            return self.options(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def _allowed_methods(self):
        return ["GET", "POST", "OPTIONS"]

@method_decorator(ensure_csrf_cookie, name='dispatch')
class CsrfTokenView(APIView):
    def get(self, request):
        return Response({'csrftoken': 'set in the cookie'})
