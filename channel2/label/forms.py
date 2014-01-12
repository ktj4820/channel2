from django import forms
from django.utils.translation import ugettext as _
from channel2.label.models import Label


class LabelForm(forms.ModelForm):

    parent = forms.CharField(
        label=_('Parent'),
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': _('Parent'),
            'list': 'label-list',
        })
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parent = kwargs['instance'].parent
        if parent:
            self.fields['parent'].initial = parent.name

    def clean_parent(self):
        return self.cleaned_data.get('parent').strip()

    def save(self, commit=True):
        label = super().save(commit=False)
        parent = self.cleaned_data.get('parent')
        if parent:
            label.parent = Label.objects.get_or_create(name=parent)[0]
        if commit:
            label.save()
        return label
