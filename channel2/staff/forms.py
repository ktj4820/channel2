from django import forms
from django.core.mail import send_mail

from channel2.account.models import User
from channel2.core.templates import TEMPLATE_ENV
from channel2.settings import SITE_SCHEME, SITE_DOMAIN, EMAIL_HOST_USER


class StaffUserAddForm(forms.ModelForm):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'Email',
        })
    )

    error_messages = {
        'email_exists': 'That email address is already registered.',
    }

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages['email_exists'])
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
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
