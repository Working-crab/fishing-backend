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
