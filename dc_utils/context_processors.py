from django.conf import settings


def dc_django_utils(request):
    return {
        "SITE_LOGO_WIDTH": "100",
        "SITE_TITLE": getattr(settings, "SITE_TITLE", ""),
        "CANONICAL_URL": f"{request.scheme}://{request.get_host()}",
    }
