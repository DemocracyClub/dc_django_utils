from django import forms, template
from django.template import Context
from django.template.loader import get_template

from dc_utils.forms import DCHeaderField
from dc_utils.widgets import DayMonthYearWidget

register = template.Library()


@register.filter
def add_input_classes(field):
    if (
        not is_checkbox(field)
        and not is_multiple_checkbox(field)
        and not is_radio(field)
        and not is_file(field)
    ):
        field_classes = field.field.widget.attrs.get("class", "")
        # Add additional classes here
        # field_classes += ' '
        field.field.widget.attrs["class"] = field_classes


@register.filter
def dc_form(element):
    if not isinstance(element, forms.BaseForm):
        # if called without a form object, return without rendering
        return
    markup_classes = {"label": "", "value": "", "single_value": ""}
    return render(element, markup_classes)


@register.filter
def render(element, markup_classes):
    element_type = element.__class__.__name__.lower()

    if element_type in ["boundfield"]:
        add_input_classes(element)
        template = get_template("dc_forms/field.html")
        context = Context(
            {"field": element, "classes": markup_classes, "form": element.form}
        )
    else:
        has_management = getattr(element, "management_form", None)
        if has_management:
            for form in element.forms:
                for field in form.visible_fields():
                    add_input_classes(field)

            template = get_template("dc_forms/formset.html")
            context = Context({"formset": element, "classes": markup_classes})
        else:
            for field in element.visible_fields():
                add_input_classes(field)

            template = get_template("dc_forms/form.html")
            context = Context({"form": element, "classes": markup_classes})

        context = context.flatten()

    return template.render(context)


def _is_input_type(input_type, field):
    if not hasattr(field.field.widget, "input_type"):
        return False
    return field.field.widget.input_type == input_type


@register.filter
def is_checkbox(field):
    return _is_input_type("checkbox", field)


@register.filter
def is_multiple_checkbox(field):
    if not _is_input_type("checkbox", field):
        return False
    try:
        return field.field.widget.__class__.__name__ == "CheckboxSelectMultiple"
    except AttributeError:
        return False


@register.filter
def is_radio(field):
    return _is_input_type("radio", field)


@register.filter
def is_file(field):
    return _is_input_type("file", field)


@register.filter
def is_dc_date_field(field):
    return isinstance(field.field.widget, DayMonthYearWidget)


@register.filter
def is_heading(field):
    return isinstance(field.field, DCHeaderField)
