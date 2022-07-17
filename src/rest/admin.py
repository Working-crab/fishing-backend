from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms

from rest import models

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_picture'].queryset = models.Picture.objects.filter(product_id=self.instance.id)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Category)
admin.site.register(models.Property)
admin.site.register(models.Picture)
admin.site.register(models.ProductProperty)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
