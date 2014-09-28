from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.core.mail import send_mail
from django.forms.widgets import EmailInput
from channel2.account.models import User
from channel2.core.templates import TEMPLATE_ENV

from channel2.core.utils import get_ip_address
from channel2.settings import SITE_SCHEME, SITE_DOMAIN, EMAIL_HOST_USER


class AccountLoginForm(forms.Form):

    LOGIN_KEY = 'login-limit-{ip_address}'
    LOGIN_TIMEOUT = 5 * 60
    LOGIN_ATTEMPT_LIMIT = 5

    email = forms.EmailField(
        label='Email',
        widget=EmailInput(attrs={
            'autofocus': 'autofocus',
            'class': 'account-input',
            'placeholder': 'Email',
            'required': 'required',
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'account-input',
            'placeholder': 'Password',
            'required': 'required',
        })
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


class AccountPasswordSetForm(forms.Form):

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'account-input',
        })
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'account-input',
        })
    )

    error_messages = {
        'password_mismatch': "The two password fields did not match.",
    }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cd = self.cleaned_data
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return cd

    def save(self):
        raw_password = self.cleaned_data.get('password1')

        self.user.token = None
        self.user.set_password(raw_password)
        self.user.save()

        user = authenticate(email=self.user.email, password=raw_password)
        return user


class AccountActivateForm(AccountPasswordSetForm):

    def save(self):
        raw_password = self.cleaned_data.get('password1')

        self.user.token = None
        self.user.is_active = True
        self.user.set_password(raw_password)
        self.user.save()

        user = authenticate(email=self.user.email, password=raw_password)
        return user


class AccountPasswordResetForm(forms.Form):

    email = forms.EmailField(widget=EmailInput(attrs={
        'autofocus': 'autofocus',
        'class': 'account-input',
        'placeholder': 'Email',
        'required': 'required',
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            self.user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise forms.ValidationError('This email is not registered at Channel2.')
        return email

    def reset_password(self):
        self.user.generate_token()
        self.user.save()

        template = TEMPLATE_ENV.get_template('account/account-password-reset-email.txt')
        message = template.render({
            'user': self.user,
            'scheme': SITE_SCHEME,
            'domain': SITE_DOMAIN,
        })
        send_mail(
            subject='[Channel 2] Password Reset',
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[self.user.email]
        )
