from collections import defaultdict
import json
from django.db.models.aggregates import Count
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from channel2.core.views import ProtectedTemplateView, StaffTemplateView
from channel2.tag.forms import TagForm
from channel2.tag.models import Tag, TagChildren


class TagListView(ProtectedTemplateView):

    template_name = 'tag/tag-list.html'

    def get(self, request):
        tag_list = Tag.objects.order_by('slug').annotate(count=Count('video'))
        return self.render_to_response({
            'tag_list': tag_list,
        })


class TagAutocompleteJsonView(ProtectedTemplateView):

    def get(self, request):
        tag_list = Tag.objects.order_by('slug').values_list('name', flat=True)
        content = json.dumps(list(tag_list), ensure_ascii=False)
        return HttpResponse(content=content, content_type='application/json')


class TagView(ProtectedTemplateView):

    template_name = 'tag/tag.html'

    def get(self, request, id, slug):
        tag = get_object_or_404(Tag, id=id)
        tag_children_list = tag.children.all()
        tag_parent_list = tag.parents.order_by('slug').annotate(count=Count('video'))

        # get the children list for each parent, but exclude the current tag
        tpc_dict = defaultdict(list)
        tpc_list = TagChildren.objects.filter(parent__in=tag_parent_list).exclude(child=tag).select_related('child')
        for tpc in tpc_list:
            tpc_dict[tpc.parent_id].append(tpc.child)
        for tag_parent in tag_parent_list:
            tag_parent.children_list = sorted(tpc_dict.get(tag_parent.id, []), key=lambda p: p.slug)

        return self.render_to_response({
            'tag': tag,
            'tag_children_list': tag_children_list,
            'tag_parent_list': tag_parent_list,
            'video_list': tag.video_set.order_by('-created_on'),
        })


class TagEditView(StaffTemplateView):

    template_name = 'tag/tag-edit.html'

    def get(self, request, id, slug):
        tag = get_object_or_404(Tag, id=id)
        return self.render_to_response({
            'form': TagForm(instance=tag),
            'tag': tag,
        })

    def post(self, request, id, slug):
        tag = get_object_or_404(Tag, id=id)

        if tag and request.POST.get('action') == 'delete':
            tag.delete()
            messages.error(request, _('The tag has been successfully deleted.'))
            return redirect('tag.list')


        form = TagForm(instance=tag, data=request.POST, files=request.FILES)
        if form.is_valid():
            tag = form.save()
            messages.success(request, _('Tag has been successfully updated.'))
            return redirect('tag', id=tag.id, slug=tag.slug)

        messages.error(request, _('There was an error with your input, the tag has not been saved.'))
        return self.render_to_response({
            'form': form,
            'tag': tag,
        })
