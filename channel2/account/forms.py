from django import forms
from django.contrib.auth import authenticate
from django.forms.widgets import EmailInput
from django.utils.translation import ugettext as _


class AccountLoginForm(forms.Form):

    email = forms.EmailField(
        label=_('Email'),
        widget=EmailInput(attrs={
            'placeholder': 'Email',
            'autocomplete': 'off',
            'class': 'account-input',
        })
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'account-input',
        })
    )

    def __init__(self, request=None, *args, **kwargs):
        super(AccountLoginForm, self).__init__(*args, **kwargs)
        self.request = request
        self.user_cache = None
        self.label_suffix = ''

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


class AccountActivateForm(forms.Form):

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'account-input',
        })
    )

    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'account-input',
        })
    )

    error_messages = {
        'password_mismatch': "The two password fields did not match.",
    }

    def __init__(self, user, *args, **kwargs):
        super(AccountActivateForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cd = self.cleaned_data
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return cd

    def save(self):
        raw_password = self.cleaned_data.get('password1')

        self.user.token = None
        self.user.is_active = True
        self.user.set_password(raw_password)
        self.user.save()

        user = authenticate(email=self.user.email, password=raw_password)
        return user
