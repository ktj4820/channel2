from django import forms
from django.contrib.auth import authenticate
from django.forms.widgets import EmailInput
from django.utils.translation import ugettext_lazy as _
from channel2.account.models import User


class AccountLoginForm(forms.Form):

    email = forms.EmailField(
        label=_('Email'),
        widget=EmailInput(attrs={
            'autocomplete': 'off',
            'class': 'account-input',
            'placeholder': 'Email',
            'required': 'required',
        })
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'account-input',
            'placeholder': 'Password',
            'required': 'required',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Please enter a correct email and password. Note that both fields are case-sensitive.')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class AccountCreateForm(forms.Form):

    email = forms.EmailField(
        label=_('Email'),
        widget=EmailInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'Email',
            'required': 'required',
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('That email address is already registered.'))
        return email

    def save(self):
        pass
