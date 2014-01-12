from django import forms
from django.utils.translation import ugettext as _
from channel2.label.models import Label
from channel2.video.models import Video


class VideoAddForm(forms.ModelForm):

    file = forms.FileField(
        label=_('File'),
        widget=forms.FileInput()
    )

    name = forms.CharField(
        label=_('Name'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': _('Name'),
            'maxlength': 100,
        }),
    )

    label = forms.CharField(
        label=_('Label'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': _('Label'),
            'maxlength': 100,
            'list': 'label-list',
        })
    )

    class Meta:
        model = Video
        fields = ('file', 'name',)

    def clean_label(self):
        label = self.cleaned_data.get('label').strip()
        return label

    def save(self, commit=True):
        video = super().save(commit=False)
        video.label = Label.objects.get_or_create(name=self.cleaned_data.get('label'))[0]
        if commit:
            video.save()
        return video
