from django import http
from django.conf import settings
from django.template import TemplateDoesNotExist, loader
from django.urls import re_path
from django.views.decorators.csrf import requires_csrf_token
from django.views.defaults import ERROR_500_TEMPLATE_NAME, page_not_found
from django.views.generic import TemplateView

from dc_utils.views import SampleFormView


@requires_csrf_token
def dc_server_error(request, template_name=ERROR_500_TEMPLATE_NAME):
    """
    The same as the Django 500 view but add the site logo.
    """
    context = {
        "site_logo": getattr(settings, "SITE_LOGO", "/images/logo_icon.svg"),
        "site_title": getattr(settings, "SITE_TITLE", "Democracy Club"),
        "STATIC_URL": getattr(settings, "STATIC_URL"),
    }
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        if template_name != ERROR_500_TEMPLATE_NAME:
            # Reraise if it's a missing custom template.
            raise
        return http.HttpResponseServerError(
            "<h1>Server Error (500)</h1>", content_type="text/html"
        )
    return http.HttpResponseServerError(template.render(context, request))


urlpatterns = [
    re_path(r"500.html$", dc_server_error),
    re_path(r"404.html$", page_not_found, {"exception": "Fake problem"}),
]


dc_utils_testing_patterns = [
    re_path(
        r"^all_elements.html$",
        TemplateView.as_view(template_name="html_tester/all_elements.html"),
        name="dc_utils_html_tester",
    ),
    re_path(
        r"^sample_form.html$",
        SampleFormView.as_view(),
        name="dc_utils_sample_form",
    ),
]
