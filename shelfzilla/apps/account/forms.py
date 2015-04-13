from django import forms
from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth.forms import (
    PasswordChangeForm as DjangoPasswordChangeForm
)
from django.utils.translation import ugettext_lazy as _

from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=75, label=_('Username'))
    password = forms.CharField(
        max_length=255, widget=forms.PasswordInput, label=_('Password'))

    def authenticate(self):
        result = None

        if self.cleaned_data:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']

            result = authenticate(username=username, password=password)

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


class PasswordChangeForm(DjangoPasswordChangeForm):
    pass


class RegistrationForm(forms.ModelForm):
    """
    Custom for for registering an user
    """
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Repeat password'),
                                widget=forms.PasswordInput)
    access_code = forms.CharField(label=_('Invitation code'), required=True)

    class Meta:
        model = models.User
        fields = ('email', 'username', )

    def get_access_code(self):
        try:
            return models.AccessCode.objects.get(
                code=self.cleaned_data['access_code'])
        except models.AccessCode.DoesNotExist:
            return False

    def clean_access_code(self):
        code = self.get_access_code()
        if not code or (code and not code.usable):
            raise forms.ValidationError(_('Invitation code is not valid'))

        return self.cleaned_data['access_code']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        with transaction.atomic():
            user = super(RegistrationForm, self).save(commit=False)
            access_code = self.get_access_code()
            user.access_code = access_code
            user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            return user
