from venv import create
from django.forms import widgets

class ReadOnlyOneImagePreviewWidget(widgets.Widget):
    template_name = 'rest/widgets/one_image_preview.html'

    def is_initial(self, value):
        """
        Return whether value is considered to be initial value.
        """
        return bool(value and getattr(value, "url", False))

    def format_value(self, value):
        """
        Return the file object if it has a defined url attribute.
        """
        if self.is_initial(value):
            return value

class CreateFileInputPreviewImageWidget(widgets.ClearableFileInput):
    create_widget = widgets.ClearableFileInput
    preview_widget = ReadOnlyOneImagePreviewWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_w = self.create_widget(self.attrs)
        self.preview_w = self.preview_widget(self.attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if not self.create_w.is_initial(value):
            return self.create_w.render(name, value, attrs, renderer)
        else:
            return self.preview_w.render(name, value, attrs, renderer)

class PriceMilliCentsWidget(widgets.NumberInput):
    template_name = 'rest/widgets/price_milli_cents.html'
    text_label = ''

    def __init__(self, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
            self.text_label = attrs.pop("text_label", self.text_label)
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs_without_id'] = dict(
            filter(lambda x: x[0] != 'id', context['widget']['attrs'].items())
        )
        context['widget']['id'] = context['widget']['attrs'].get('id')
        context['widget']['text_label'] = self.text_label
        return context
