from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.db.models import ImageField
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from rest import models, widgets
from rest import fields

def link_to(field_name, value=None, short_description=None):
    def field_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse(f"admin:rest_{field_name}_change", args=(getattr(obj, field_name).pk, )),
            getattr(obj, value if value is not None else field_name)
        ))
    field_link.short_description = short_description if short_description is not None else field_name
    return field_link

class ReadOnlyPictureForm(forms.ModelForm):
    image = fields.CreatePreviewImageField(label='images')

class PicturesInline(admin.StackedInline):
    template = "rest/pictures_inline.html"
    model = models.Picture
    form = ReadOnlyPictureForm
    extra = 0

    @property
    def media(self):
        result = super().media + forms.Media(css={'all': ['rest/style.css']})
        return result

class ProductPropertiesInline(admin.TabularInline):
    template = "rest/product_properties_inline.html"
    model = models.ProductProperty
    extra = 0
    show_original = False

class PriceField(forms.IntegerField):
    def __init__(self, *args, **kwargs):
        price_field = models.Product.price.field.formfield()
        kwargs['min_value'] = price_field.min_value
        kwargs['max_value'] = price_field.max_value
        kwargs['widget'] = widgets.PriceMilliCentsWidget({'text_label': 'В милликопейках: '})
        kwargs['help_text'] = "Руб., значение хранится в милликопейках (1 руб. = 100000)"
        super().__init__(*args, **kwargs)

class ProductForm(forms.ModelForm):
    price = PriceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['main_picture'].queryset = models.Picture.objects.filter(product_id=self.instance.id)

    @property
    def media(self):
        result = super().media + forms.Media(js=['rest/widgets.js'])
        return result

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'price')
    inlines = [
        PicturesInline,
        ProductPropertiesInline
    ]

    class ImportForm(forms.Form):
        file = forms.FileField()

    def get_urls(self):
        return [
            path(
                "import/",
                self.admin_site.admin_view(self.import_products),
                name="rest_product_import",
            ),
        ] + super().get_urls()

    def import_products(self, request, form_url=""):
        form = ProductAdmin.ImportForm()
        rendered_form = form.render()
        context = {
            "title": _("Import products"),
            #"adminForm": adminForm,
            "form_url": form_url,
            "form": rendered_form,
            #"is_popup": (IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET),
            #"is_popup_var": IS_POPUP_VAR,
            "add": True,
            "change": False,
            "has_delete_permission": False,
            "has_change_permission": True,
            "has_absolute_url": False,
            "opts": models.Product._meta,
            #"original": user,
            "save_as": False,
            "show_save": True,
            **self.admin_site.each_context(request),
        }
        return render(request, "admin/rest/product/import.html", context)

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
