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

    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
    )

    class Meta:
        model = Video
        fields = ('file', 'name', 'label',)
