from django import forms
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.forms.widgets import EmailInput
from django.utils.translation import ugettext_lazy as _
from channel2.account.models import User
from channel2.core.templates import TEMPLATE_ENV
from channel2.settings import SITE_SCHEME, SITE_DOMAIN, EMAIL_HOST_USER


class AccountLoginForm(forms.Form):

    email = forms.EmailField(
        label=_('Email'),
        widget=EmailInput(attrs={
            'autofocus': 'autofocus',
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



class AccountPasswordSetForm(forms.Form):

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
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(_('This email is not registered at Channel2.'))
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


