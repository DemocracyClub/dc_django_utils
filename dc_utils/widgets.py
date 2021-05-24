import re

from django.forms.widgets import MultiWidget, NumberInput
from django.utils.safestring import mark_safe

__all__ = ('DayMonthYearWidget',)

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')


class DayMonthYearWidget(MultiWidget):

    def __init__(self, attrs=None):
        self.widgets = [
            NumberInput(attrs={'label': 'Day'}),
            NumberInput(attrs={'label': 'Month'}),
            NumberInput(attrs={'label': 'Year'}),
        ]
        super(MultiWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            widget_html = widget.render(name + '_%s' % i,
                                        widget_value, final_attrs)
            html = """
            <div class="form-group form-group-{name}">
                <label for="{name}_{i}">{label}</label>
                {widget_html}
            </div>
            """.format(**{
                    'name': widget.attrs['label'].lower(),
                    'i': i,
                    'widget_html': widget_html,
                    'label': widget.attrs['label'],
                })
            output.append(html)

        try:
            return mark_safe(self.format_output(output))
        except AttributeError:
            return mark_safe(''.join(output))

    def decompress(self, value):
        if not value:
            return []
        return value
