import pytest
from django import forms

from dc_utils.templatetags.dc_forms import dc_form


class TestDCForms:
    def test_render_not_called_when_element_not_a_form(self, mocker):
        mock_render = mocker.Mock()
        mocker.patch("dc_utils.templatetags.dc_forms.render", mock_render)

        assert dc_form(element="not_a_form") is None
        mock_render.assert_not_called()

    def test_render_called_when_element_is_a_form(self, mocker):
        mock_render = mocker.Mock(return_value="rendered_form")
        mocker.patch("dc_utils.templatetags.dc_forms.render", mock_render)
        form = forms.Form()
        assert dc_form(element=form) == "rendered_form"
        mock_render.called_once_with(
            form, {"label": "", "value": "", "single_value": ""}
        )
