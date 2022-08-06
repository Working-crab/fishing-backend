from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from rest import views

urlpatterns = [
    path('', views.TestView.as_view(), name='test'),
    path('graphql', csrf_exempt(views.GraphQLView.as_view(graphiql=True))),
    path('csrftoken/', views.CsrfTokenView.as_view()),
    path('accounts/', include('rest_registration.api.urls')),
]
