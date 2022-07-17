from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    phone = models.CharField(max_length=12, blank=True, default="")

class Category(models.Model):
    name = models.CharField(max_length=80)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Property(models.Model):
    name = models.CharField(max_length=80)

    class Meta:
        verbose_name_plural = "properties"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, default="")
    price = models.PositiveBigIntegerField(help_text="Милликопейки (100000 = 1 руб.)")
    main_picture = models.ForeignKey('Picture', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    properties = models.ManyToManyField(Property, through='ProductProperty', related_name='products')

    def __str__(self):
        return self.name

class Picture(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pictures')

class ProductProperty(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='product_properties')
    num_value = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    string_value = models.CharField(max_length=50, blank=True, default="")  # also works as num_value units

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'property'], name="unique_product_property")
        ]
        verbose_name_plural = "product properties"

    def get_value(self):
        if self.num_value is not None:
            result = str(self.num_value)
            if self.string_value is not None and len(self.string_value) > 0:
                result += f" {self.string_value}"
            return result
        else:
            return self.string_value

    def __str__(self):
        return f"{self.property}: {self.get_value()} ({self.product})"

class Order(models.Model):
    of_user_label = _("of user")

    class Status(models.TextChoices):
        OPEN = 'OPEN', _("Open")
        CLOSED = 'CLOSED', _("Closed")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem', related_name='+')
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.OPEN)

    def __str__(self):
        return f"{self.__class__.__name__} {self.of_user_label} {self.user} ({self.pk})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product} ({self.order})"
