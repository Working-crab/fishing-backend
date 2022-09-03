from attr import field
from rest_framework import serializers

from rest import models

class LoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

class AccountSerializer(serializers.ModelSerializer):
    is_authenticated = serializers.BooleanField()
    phone = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = models.User
        fields = ['is_authenticated', 'username', 'first_name', 'last_name', 'email', 'phone']

class TestCartSerializer(serializers.Serializer):
    test = serializers.CharField(required=False)

class ProductPropertiesSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source='name')

    class Meta:
        model = models.ProductProperty
        fields = [
            'property_name',
            'num_value', 'string_value']

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Picture
        fields = ['id', 'image']
        extra_kwargs = {'image': {'use_url': False}}

class ProductSerializer(serializers.ModelSerializer):
    formatted_price = serializers.CharField(required=False, read_only=True, source='get_formatted_price')
    main_picture = PictureSerializer(required=False, read_only=True)
    properties = ProductPropertiesSerializer(many=True, read_only=True)
    pictures = PictureSerializer(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = ['id', 'name', 'description', 'price', 'formatted_price', 'main_picture', 'properties', 'pictures']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False, read_only=True)

    class Meta:
        model = models.OrderItem
        fields = ['product', 'quantity']

class AddOrderItemSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=models.Product.objects.all())
    quantity = serializers.IntegerField(min_value=0)

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = ['id', 'status', 'products']
