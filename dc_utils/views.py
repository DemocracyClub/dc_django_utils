from django.views.generic import FormView

from dc_utils.forms import SampleForm


class SampleFormView(FormView):
    form_class = SampleForm
    template_name = "html_tester/sample_form.html"
