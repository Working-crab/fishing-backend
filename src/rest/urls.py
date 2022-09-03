from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from rest import views

urlpatterns = [
    path('', views.TestView.as_view(), name='test'),
    path('graphql', csrf_exempt(views.GraphQLView.as_view(graphiql=True))),
    path('csrftoken/', views.CsrfTokenView.as_view()),
    path('accounts/verify-registration/', views.verify_registration, name='verify-registration'),
    path('accounts/verify-email/', views.verify_email, name='verify-email'),
    path('accounts/', include('rest_registration.api.urls')),
    path('cart/', views.CartAPIView.as_view(), name='cart'),
]
