from django import forms
from channel2.core.forms import BlankLabelSuffixMixin
from channel2.core.utils import convert_markdown
from channel2.tag.models import Tag


class TagForm(BlankLabelSuffixMixin, forms.ModelForm):

    children = forms.CharField(required=False)

    markdown = forms.CharField(
        required=False,
        max_length=1000,
        widget=forms.Textarea(attrs={
            'maxlength': '1000',
            'rows': '6'
        }),
    )

    class Meta:
        model = Tag
        fields = ('name', 'pinned', 'markdown')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.html = ''

    def clean_markdown(self):
        markdown = self.cleaned_data.get('markdown')
        self.html = convert_markdown(markdown)
        return markdown

    def save(self, commit=True):
        tag =  super().save(commit=False)
        tag.html = self.html
        if commit:
            tag.save()
        return tag

