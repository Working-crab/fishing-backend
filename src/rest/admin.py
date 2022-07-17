from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe

from rest import models

def link_to(field_name, value=None, short_description=None):
    def field_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse(f"admin:rest_{field_name}_change", args=(getattr(obj, field_name).pk, )),
            getattr(obj, value if value is not None else field_name)
        ))
    field_link.short_description = short_description if short_description is not None else field_name
    return field_link

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_picture'].queryset = models.Picture.objects.filter(product_id=self.instance.id)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'price')

@admin.register(models.Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'product_link')

    product_link = link_to('product')

@admin.register(models.ProductProperty)
class ProductPropertyAdmin(admin.ModelAdmin):
    list_display = ('property', 'num_value', 'string_value', 'product_link')

    product_link = link_to('product')

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'order_link')

    order_link = link_to('order')

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Category)
admin.site.register(models.Property)
