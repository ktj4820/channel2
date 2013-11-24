from django import forms
from django.utils.translation import ugettext as _
from channel2.label.models import Label


class LabelForm(forms.ModelForm):

    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Name'),
            'required': 'required',
        })
    )

    markdown = forms.CharField(
        label=_('Markdown'),
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Please enter markdown here.'),
            'rows': '10',
            'data-bind': 'value: markdown, valueUpdate: "afterkeydown"',
        })
    )

    class Meta:
        model = Label
        fields = ('name', 'markdown', 'html')
