import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField

from rest.models import *

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interface = (graphene.Node, )
        use_connection = True
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains"]
        }

class PropertyNode(DjangoObjectType):
    class Meta:
        model = Property
        interface = (graphene.Node, )
        use_connection = True
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains"]
        }

class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        interface = (graphene.Node, )
        use_connection = True
        filter_fields = {
            "id": ["exact"],
            "name": ["exact", "icontains"],
            "description": ["icontains"],
            "price": ["lt", "lte", "gt", "gte", "range"],
            "properties__id": ["exact", "in"]
        }

class PictureNode(DjangoObjectType):
    class Meta:
        model = Picture
        interface = (graphene.Node, )
        use_connection = True
        filter_fields = {
            "product__id": ["exact"],
        }

class ProductPropertyNode(DjangoObjectType):
    class Meta:
        model = ProductProperty
        interface = (graphene.Node, )
        use_connection = True
        filter_fields = {
            "product__id": ["exact"],
            "property__id": ["exact"],
            "num_value": ["exact", "lt", "lte", "gt", "gte", "range"],
            "string_value": ["exact", "icontains"]
        }

class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        interface = (graphene.Node, )
        use_connection = True
        filter_fields = {
            "products__id": ["exact", "in"],
            "status": ["exact"]
        }

class OrderItemNode(DjangoObjectType):
    class Meta:
        model = OrderItem
        interface = (graphene.Node, )
        use_connection = True
        filter_fields = {
            "order__id": ["exact"],
            "product__id": ["exact"],
            "quantity": ["exact", "lt", "lte", "gt", "gte", "range"],
        }

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")

    categories = DjangoFilterConnectionField(CategoryNode)
    properties = DjangoFilterConnectionField(PropertyNode)
    products = DjangoFilterConnectionField(ProductNode)
    pictures = DjangoFilterConnectionField(PictureNode)
    product_properties = DjangoFilterConnectionField(ProductPropertyNode)
    orders = DjangoFilterConnectionField(OrderNode)
    order_items = DjangoFilterConnectionField(OrderItemNode)

schema = graphene.Schema(query=Query)
