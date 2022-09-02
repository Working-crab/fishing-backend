from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from rest_framework import routers

from rest import views

router = routers.DefaultRouter()
router.register('cart', views.CartViewSet, basename='cart')

urlpatterns = [
    path('', views.TestView.as_view(), name='test'),
    path('graphql', csrf_exempt(views.GraphQLView.as_view(graphiql=True))),
    path('csrftoken/', views.CsrfTokenView.as_view()),
    path('accounts/verify-registration/', views.verify_registration, name='verify-registration'),
    path('accounts/verify-email/', views.verify_email, name='verify-email'),
    path('accounts/', include('rest_registration.api.urls')),
    path('', include(router.urls)),
]
