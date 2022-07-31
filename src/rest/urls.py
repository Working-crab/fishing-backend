from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from rest import views

from graphene_django.views import GraphQLView

urlpatterns = [
    path('', views.TestView.as_view(), name='test'),
    path('graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('csrftoken/', views.CsrfTokenView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('account/', views.AccountView.as_view()),
    path('accounts/', include('rest_registration.api.urls')),
]
