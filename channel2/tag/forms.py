import os

from django import forms
from django.core.files.base import File
from django.forms.formsets import BaseFormSet
import markdown

from channel2.settings import VIDEO_DIR
from channel2.tag.models import Tag
from channel2.video.models import Video


class TagForm(forms.ModelForm):

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
            'required': 'required',
        })
    )

    children = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Children Tags',
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

    error_messages = {
        'name.has.comma': 'The tag name cannot have a comma in it',
        'tag.not.found': 'Unable to find tag "{}"',
    }

    class Meta:
        model = Tag
        fields = ('name', 'markdown', 'pinned', 'order',)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''
        self.user = user
        self.html = ''
        self.children_tag_list = []

        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.fields['children'].initial = ', '.join(Tag.objects.filter(parents=instance).order_by('slug').values_list('name', flat=True))

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if ',' in name:
            raise forms.ValidationError(self.error_messages['name.has.comma'])
        return name

    def clean_children(self):
        children = self.cleaned_data.get('children')
        self.children_tag_list = []
        for tag_name in children.split(','):
            tag_name = tag_name.strip()
            if not tag_name:
                continue
            try:
                tag = Tag.objects.get(name=tag_name)
                self.children_tag_list.append(tag)
            except Tag.DoesNotExist:
                raise forms.ValidationError(self.error_messages['tag.not.found'].format(tag_name))
        return children

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
        tag.children.clear()
        if self.children_tag_list:
            tag.children.add(*self.children_tag_list)

        return tag


class TagVideoForm(forms.Form):

    select = forms.BooleanField(required=False, initial=True)
    filename = forms.CharField(widget=forms.HiddenInput)
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'tag-video-input',
        })
    )


class TagVideoFormSet(BaseFormSet):

    def save(self, tag):
        count = 0
        unlink_list = []

        for form in self.ordered_forms:
            if not form.cleaned_data.get('select'):
                continue

            count += 1
            data = form.cleaned_data
            file_path = os.path.join(VIDEO_DIR, data.get('filename'))
            file = open(file_path, 'rb')
            Video.objects.create(file=File(file), name=data.get('name'), tag=tag)
            file.close()

        for file in unlink_list:
            os.unlink(file)

        return count
