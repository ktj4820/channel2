from django import forms
from django.forms.widgets import EmailInput
from django.utils.translation import ugettext_lazy as _
from channel2.account.models import User


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
        return user
