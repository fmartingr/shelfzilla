from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=75)
    password = forms.CharField(
        max_length=255, widget=forms.PasswordInput)

    def authenticate(self):
        result = None

        if self.cleaned_data:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            result = authenticate(username=email, password=password)

        return result

    def clean(self):
        data = self.cleaned_data

        if not self.errors:
            user = self.authenticate()

            if user is not None:
                if not user.is_active:
                    raise forms.ValidationError(
                        _("This account is disabled.")
                    )
            else:
                raise forms.ValidationError(
                    _('User with those credentials was not found.')
                )

        return data
