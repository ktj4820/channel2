from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import authenticate
from django.core.cache import cache

from channel2.core.utils import get_ip_address


class AccountLoginForm(forms.Form):

    LOGIN_KEY = 'login-limit-{ip_address}'
    LOGIN_TIMEOUT = 5 * 60
    LOGIN_ATTEMPT_LIMIT = 5

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'autofocus': '',
        }),
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
    )

    error_messages = {
        'invalid_login': 'Please enter a correct email and password. Note that the password field is case-sensitive.',
        'inactive': 'Your account has not been activated yet. An email with a link to activate your account has been sent to your email address.',
    }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.request = request
        self.user_cache = None

        key = self.get_cache_key()
        if cache.get(key, 0) >= self.LOGIN_ATTEMPT_LIMIT:
            self.fields['captcha'] = CaptchaField()

    def get_cache_key(self):
        return self.LOGIN_KEY.format(ip_address=get_ip_address(self.request))

    def update_attempt(self):
        key = self.get_cache_key()
        if cache.get(key) is None:
            cache.set(key, 1, self.LOGIN_TIMEOUT)
        else:
            cache.incr(key)

    def clean(self):
        email = self.cleaned_data.get('email', '').lower()
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                self.update_attempt()
                raise forms.ValidationError(self.error_messages['invalid_login'])
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])

        return self.cleaned_data

    def get_user(self):
        return self.user_cache
