from urllib.parse import urlencode

try:
    from django_filters.widgets import LinkWidget
except ImportError:
    raise ImportError("Filter widgets requires Django-Filter to be installed")

from django.db.models import BLANK_CHOICE_DASH
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe

__all__ = ("DSLinkWidget",)


class DSLinkWidget(LinkWidget):
    """
    The django_filters LinkWidget doesn't allow iterating over choices in the template layer
    to change the HTML wrapping the widget.

    This breaks the way that Django *should* work, so we have to subclass
    and alter the HTML in Python :/

    https://github.com/carltongibson/django-filter/issues/880
    """

    def render(self, name, value, attrs=None, choices=(), renderer=None):
        if not hasattr(self, "data"):
            self.data = {}
        if value is None:
            value = ""
        self.build_attrs(self.attrs, extra_attrs=attrs)
        output = []
        options = self.render_options(choices, [value], name)
        if options:
            output.append(options)
        # output.append('</ul>')
        return mark_safe("\n".join(output))

    def render_option(self, name, selected_choices, option_value, option_label):
        option_value = force_str(option_value)
        if option_label == BLANK_CHOICE_DASH[0][1]:
            option_label = "All"
        data = self.data.copy()
        data[name] = option_value
        selected = data == self.data or option_value in selected_choices
        try:
            url = data.urlencode()
        except AttributeError:
            url = urlencode(data)
        return self.option_string() % {
            "attrs": selected and ' aria-current="true"' or "",
            "query_string": url,
            "label": force_str(option_label),
        }
