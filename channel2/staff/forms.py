import datetime

from django import forms

from django.core.mail import send_mail
import requests

from channel2.account.models import User
from channel2.core.templates import TEMPLATE_ENV
from channel2.settings import SITE_SCHEME, SITE_DOMAIN, EMAIL_HOST_USER
from channel2.tag.enums import TagType
from channel2.tag.models import Tag
from channel2.tag.utils import month_to_season, download_cover


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


class StaffAnimeSearchForm(forms.Form):

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Title',
        })
    )


class StaffAnimeAddForm(forms.Form):
    """
    This form takes an "id" parameter. This "id" should be the hummingbird API's
    anime ID.
    """

    hummingbird_id = forms.CharField()

    def clean_hummingbird_id(self):
        hummingbird_id = self.cleaned_data.get('hummingbird_id')

        self.json = requests.get('https://hummingbird.me/api/v1/anime/' + hummingbird_id).json()
        if Tag.objects.filter(name=self.json['title']).exists():
            raise forms.ValidationError('"{}" already exists'.format(self.json['title']))

        return hummingbird_id

    def save(self):
        tag = Tag.objects.create(
            name=self.json['title'],
            type=TagType.ANIME,
            json=self.json,
        )

        tag.cover = download_cover(tag, self.json['cover_image'])
        tag.save()

        children = []
        for genre in self.json.get('genres', []):
            child = Tag.objects.get_or_create(name=genre.get('name'))[0]
            children.append(child)

        if self.json.get('show_type') != 'TV':
            child = Tag.objects.get_or_create(name=self.json.get('show_type'))[0]
            children.append(child)
        elif self.json.get('episode_count') < 30:
            started = self.json.get('started_airing')
            d = datetime.datetime.strptime(started, '%Y-%m-%d')
            name = '{} {}'.format(d.year, month_to_season[d.month])
            child = Tag.objects.get_or_create(name=name)[0]
            children.append(child)

        tag.children.add(*children)
        return tag
