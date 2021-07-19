from django.conf.urls import url
from django.views.defaults import ERROR_500_TEMPLATE_NAME


def test_dc_server_error(client):
    assert client.get(ERROR_500_TEMPLATE_NAME).context
