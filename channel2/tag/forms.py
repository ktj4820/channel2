from django import forms
from django.utils.translation import ugettext_lazy as _

from channel2.core.forms import BlankLabelSuffixMixin
from channel2.core.utils import convert_markdown
from channel2.tag.models import Tag


class TagForm(BlankLabelSuffixMixin, forms.ModelForm):

    children = forms.CharField(
        label=_('Tags'),
        required=False,
        help_text=_('Enter a comma separated list of tags.'),
    )

    pinned = forms.BooleanField(required=False)
    order = forms.IntegerField(required=False, label=_('Order'))

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
        fields = ('name', 'pinned', 'order', 'markdown')

    def __init__(self, *args, **kwargs):
        if 'instance' not in kwargs:
            raise RuntimeError('TagForm must be used with an instance.')
        super().__init__(*args, **kwargs)

        tag = kwargs['instance']
        self.fields['children'].initial = ', '.join(sorted(tag.children.values_list('name', flat=True)))
        self.html = ''
        self.children_list = []

    def clean_markdown(self):
        markdown = self.cleaned_data.get('markdown')
        self.html = convert_markdown(markdown)
        return markdown

    def clean_children(self):
        children = self.cleaned_data.get('children')
        self.children_list = filter(None, map(str.strip, children.split(',')))
        return children

    def save(self):
        tag =  super().save(commit=False)
        tag.html = self.html
        tag.save()

        children_list = [Tag.objects.get_or_create(name=name)[0] for name in self.children_list]
        tag.children.clear()
        tag.children.add(*children_list)

        return tag
