from asyncio import mixins
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import status

from graphene_django.views import GraphQLView as OriginalGraphQLView

from rest_registration import signals
from rest_registration.api.views.login import perform_login
from rest_registration.api.views.register import VerifyRegistrationSerializer
from rest_registration.api.views.register_email import VerifyEmailSerializer
from rest_registration.api.views.register import process_verify_registration_data
from rest_registration.api.views.register_email import process_verify_email_data
from rest_registration.decorators import api_view_serializer_class
from rest_registration.utils.responses import get_ok_response
from rest_registration.settings import registration_settings

from rest import serializers
from rest import models

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

@api_view_serializer_class(VerifyRegistrationSerializer)
@api_view(['GET'])
@permission_classes(registration_settings.NOT_AUTHENTICATED_PERMISSION_CLASSES)
def verify_registration(request):
    """
    Verify registration via signature.
    """
    user = process_verify_registration_data(
        request.query_params, serializer_context={'request': request})
    signals.user_activated.send(sender=None, user=user, request=request)
    extra_data = None
    if registration_settings.REGISTER_VERIFICATION_AUTO_LOGIN:
        extra_data = perform_login(request, user)
    # return get_ok_response(_("User verified successfully"), extra_data=extra_data)
    return redirect('index')

@api_view_serializer_class(VerifyEmailSerializer)
@api_view(['GET'])
@permission_classes(registration_settings.NOT_AUTHENTICATED_PERMISSION_CLASSES)
def verify_email(request):
    '''
    Verify email via signature.
    '''
    process_verify_email_data(request.query_params, serializer_context={'request': request})
    return get_ok_response(_("Email verified successfully"))


class CartViewSet(ListModelMixin, GenericViewSet):
    serializer_class = serializers.OrderItemSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'add_items':
            #kwargs['many'] = True
            return serializers.AddOrderItemSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_cart(self):
        if self.request.user.is_authenticated:
            orders = models.Order.objects.filter(
                user=self.request.user, status=str(models.Order.Status.OPEN)
            )
            if orders:
                return orders.first()
            else:
                return models.Order.objects.create(user=self.request.user, status=models.Order.Status.OPEN)
        return None

    def get_queryset(self):
        cart = self.get_cart()
        if cart:
            return cart.order_items
        return models.Product.objects.none()

    @action(detail=False, methods=['POST'], url_path='add_items')
    def add_items(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            cart = self.get_cart()
            for order_item in serializer.validated_data:
                product = order_item['product_id']
                quantity = order_item['quantity']

                if cart.products.contains(product):
                    raise ParseError('product already in cart (change quantity instead)')
                else:
                    cart.products.add(product, through_defaults={'quantity': quantity})
        return Response(status=status.HTTP_204_NO_CONTENT)
