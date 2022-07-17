from django.forms import widgets

class ReadOnlyImagePreviewWidget(widgets.Widget):
    template_name = 'rest/widgets/image_preview.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        return super().render(*args, **kwargs)

class ReadOnlyOneImagePreviewWidget(widgets.Widget):
    template_name = 'rest/widgets/one_image_preview.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        return super().render(*args, **kwargs)

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
