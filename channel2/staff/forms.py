from django import forms
from django.core.mail import send_mail
from django.forms.formsets import BaseFormSet
from django.forms.widgets import EmailInput
from django.utils.translation import ugettext_lazy as _
from channel2.account.models import User
from channel2.core.templates import TEMPLATE_ENV
from channel2.settings import SITE_SCHEME, SITE_DOMAIN, EMAIL_HOST_USER


class StaffAccountCreateForm(forms.Form):

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
        email = self.cleaned_data.get('email')
        user = User(email=email, password='********')
        user.generate_token()
        user.save()

        template = TEMPLATE_ENV.get_template('staff/staff-user-activate-email.txt')
        message = template.render({
            'user': user,
            'scheme': SITE_SCHEME,
            'domain': SITE_DOMAIN,
        })
        send_mail(
            subject='[Channel 2] Activate Your Account',
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return user


class StaffVideoAddForm(forms.Form):

    filename = forms.CharField(widget=forms.HiddenInput)
    name = forms.CharField()
    label = forms.CharField(widget=forms.TextInput(attrs={
        'list': 'tags',
    }))


class StaffVideoAddFormSet(BaseFormSet):
    pass
