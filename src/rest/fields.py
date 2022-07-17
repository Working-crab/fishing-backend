from django.forms import fields

from rest.widgets import ReadOnlyImagePreviewWidget, ReadOnlyOneImagePreviewWidget

class ImageSetField(fields.Field):
    widget = ReadOnlyImagePreviewWidget

class ReadOnlyImageField(fields.Field):
    widget = ReadOnlyOneImagePreviewWidget
