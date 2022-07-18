from django.forms import fields

from rest.widgets import ReadOnlyOneImagePreviewWidget

class ReadOnlyImageField(fields.Field):
    widget = ReadOnlyOneImagePreviewWidget

    def __init__(self, *args, **kwargs):
        kwargs['disabled'] = True
        kwargs['required'] = False
        super().__init__(*args, **kwargs)
