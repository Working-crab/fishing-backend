from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from rest import models

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Category)
admin.site.register(models.Property)
admin.site.register(models.Product)
admin.site.register(models.Picture)
admin.site.register(models.ProductProperty)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
