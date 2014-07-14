from django import forms
from django.core.files.base import File
from django.core.mail import send_mail
from django.forms.formsets import BaseFormSet
from django.forms.widgets import EmailInput
from django.utils.translation import ugettext_lazy as _
import os
from channel2.account.models import User
from channel2.core.templates import TEMPLATE_ENV
from channel2.localsettings import VIDEO_DIR
from channel2.settings import SITE_SCHEME, SITE_DOMAIN, EMAIL_HOST_USER
from channel2.tag.models import Tag
from channel2.video.models import Video


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


class StaffVideoImportForm(forms.Form):

    select = forms.BooleanField(required=False, initial=True)
    filename = forms.CharField(widget=forms.HiddenInput)
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'staff-input',
    }))
    tag = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'staff-input',
        'list': 'tags'
    }))


class StaffVideoImportFormSet(BaseFormSet):

    def save(self):
        count = 0
        for form in self.ordered_forms:
            if not form.cleaned_data.get('select'):
                continue

            count += 1
            data = form.cleaned_data
            file_path = os.path.join(VIDEO_DIR, data.get('filename'))
            file = open(file_path, 'rb')
            Video.objects.create(
                file=File(file),
                name=data.get('name'),
                tag=Tag.objects.get_or_create(name=data.get('tag'))[0]
            )
            os.remove(file_path)

        return count
