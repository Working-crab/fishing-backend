from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from rest.views import TestView

from graphene_django.views import GraphQLView

urlpatterns = [
    path('', TestView.as_view(), name='test'),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True)))
]
