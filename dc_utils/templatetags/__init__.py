import markdown
from dc_utils.forms import DCHeaderField
from dc_utils.widgets import DayMonthYearWidget
from django import forms, template
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe

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
        field_classes += " form-control"
        field.field.widget.attrs["class"] = field_classes


@register.filter
def dc_form(element):
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


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_multiple_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)


@register.filter
def is_radio(field):
    return isinstance(field.field.widget, forms.RadioSelect)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def is_dc_date_field(field):
    return isinstance(field.field.widget, DayMonthYearWidget)


@register.filter
def is_heading(field):
    return isinstance(field.field, DCHeaderField)


@register.filter(name="markdown")
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))


markdown_filter.is_safe = True


@register.tag(name="markdown")
def markdown_tag(parser, token):
    nodelist = parser.parse(("endmarkdown",))
    bits = token.split_contents()
    if len(bits) == 1:
        style = "default"
    elif len(bits) == 2:
        style = bits[1]
    else:
        raise template.TemplateSyntaxError(
            "`markdown` tag requires exactly zero or one arguments"
        )
    parser.delete_first_token()  # consume '{% endmarkdown %}'
    return MarkdownNode(style, nodelist)


class MarkdownNode(template.Node):
    def __init__(self, style, nodelist):
        self.style = style
        self.nodelist = nodelist

    def render(self, context):
        value = self.nodelist.render(context)
        return mark_safe(markdown.markdown(value, self.style))
