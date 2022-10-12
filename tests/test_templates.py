import pytest
from django.template.loader import select_template
from djhtml.modes import DjHTML


@pytest.mark.parametrize(
    "template_name",
    [
        "dc_base.html",
        "dc_base_naked.html",
    ],
)
def test_djhtml(template_name):
    template = select_template([template_name]).template.source
    mode = DjHTML
    updated = mode(template).indent(4)
    assert template == updated


def test_dc_base_template(client):
    req = client.get("/test_dc_base.html")
    assert req.status_code == 200


def test_dc_base_naked_template(client):
    req = client.get("/test_dc_base_naked.html")
    assert req.status_code == 200


def test_form_view(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"id_postcode" in resp.content
    assert b"Heading Field" in resp.content
