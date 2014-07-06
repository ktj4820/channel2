from django import forms
from django.utils.translation import ugettext_lazy as _

from channel2.blog.models import BlogPost
from channel2.core.forms import BlankLabelSuffixMixin
from channel2.core.utils import convert_markdown


class BlogPostForm(BlankLabelSuffixMixin, forms.ModelForm):

    title = forms.CharField(
        label=_('Title'),
        max_length=200,
    )

    markdown = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': '6'
        }),
    )

    def clean_markdown(self):
        markdown = self.cleaned_data.get('markdown')
        self.html = convert_markdown(markdown)
        return markdown

    class Meta:
        model = BlogPost
        fields = ('title', 'markdown',)

    def save(self, request, commit=True):
        blog_post = super().save(commit=False)
        blog_post.html = self.html
        blog_post.created_by = request.user

        if commit:
            blog_post.save()
        return blog_post
