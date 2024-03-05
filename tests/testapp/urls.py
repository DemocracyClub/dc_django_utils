"""tests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from dc_utils.views import SampleFormView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "test_dc_base.html",
        TemplateView.as_view(template_name="dc_base.html"),
        name="test_dc_base",
    ),
    path(
        "test_dc_base_naked.html",
        TemplateView.as_view(template_name="dc_base_naked.html"),
        name="test_dc_base_naked",
    ),
    path("", SampleFormView.as_view(), name="test_form"),
    path(
        "500.html", TemplateView.as_view(template_name="500.html"), name="500"
    ),
    path(
        "404.html", TemplateView.as_view(template_name="404.html"), name="404"
    ),
]
