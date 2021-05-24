"""
Examples taken with thanks from
https://github.com/django-crispy-forms/django-crispy-forms/blob/main/crispy_forms/tests/forms.py
"""

from django import forms


class SampleForm(forms.Form):
    is_company = forms.CharField(label="company", required=False, widget=forms.CheckboxInput())
    email = forms.EmailField(
        label="email", max_length=30, required=True, widget=forms.TextInput(), help_text="Insert your email"
    )
    password1 = forms.CharField(label="password", max_length=30, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(label="re-enter password", max_length=30, required=True, widget=forms.PasswordInput())
    first_name = forms.CharField(label="first name", max_length=5, required=True, widget=forms.TextInput())
    last_name = forms.CharField(label="last name", max_length=5, required=True, widget=forms.TextInput())
    datetime_field = forms.SplitDateTimeField(label="date time", widget=forms.SplitDateTimeWidget())

    checkboxes = forms.MultipleChoiceField(
        choices=((1, "Option one"), (2, "Option two"), (3, "Option three")),
        initial=(1,),
        widget=forms.CheckboxSelectMultiple,
    )

    alphacheckboxes = forms.MultipleChoiceField(
        choices=(("option_one", "Option one"), ("option_two", "Option two"), ("option_three", "Option three")),
        initial=("option_two", "option_three"),
        widget=forms.CheckboxSelectMultiple,
    )

    numeric_multiple_checkboxes = forms.MultipleChoiceField(
        choices=((1, "Option one"), (2, "Option two"), (3, "Option three")),
        initial=(1, 2),
        widget=forms.CheckboxSelectMultiple,
    )

    inline_radios = forms.ChoiceField(
        choices=(
            ("option_one", "Option one"),
            ("option_two", "Option two"),
        ),
        widget=forms.RadioSelect,
        initial="option_two",
    )

    file_field = forms.FileField(widget=forms.FileInput)
    clearable_file = forms.FileField(widget=forms.ClearableFileInput, required=False)

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get("password1", None)
        password2 = self.cleaned_data.get("password2", None)
        if not password1 and not password2 or password1 != password2:
            raise forms.ValidationError("Passwords dont match")

        return self.cleaned_data
