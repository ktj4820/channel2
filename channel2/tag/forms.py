from django import forms
import markdown

from channel2.tag.models import Tag


class TagForm(forms.ModelForm):

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'autofocus': 'autofocus',
            'placeholder': 'Name',
            'required': 'required',
        })
    )

    markdown = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Markdown',
        })
    )

    pinned = forms.BooleanField(
        required=False
    )

    order = forms.IntegerField(
        required=False,
        min_value=0,
    )

    class Meta:
        model = Tag
        fields = ('name', 'markdown', 'pinned', 'order',)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.user = user
        self.html = ''
        self.tag_parent = None

    def clean_markdown(self):
        md = self.cleaned_data.get('markdown')
        self.html = markdown.markdown(md)
        return md

    def save(self):
        tag = super().save(commit=False)
        tag.html = self.html
        tag.updated_by = self.user

        if not tag.created_by:
            tag.created_by = self.user

        tag.save()
        if self.tag_parent:
            tag.parents.add(self.tag_parent)

        return tag
