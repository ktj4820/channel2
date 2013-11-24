from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404, redirect
from channel2.core.views import ProtectedTemplateView, StaffOnlyView
from channel2.label.forms import LabelForm
from channel2.label.models import Label


class LabelListView(ProtectedTemplateView):

    template_name = 'label/label-list.html'

    def get(self, request):
        return self.render_to_response({
            'label_list': Label.objects.annotate(count=Count('video'), children_count=Count('children')),
        })


class LabelView(ProtectedTemplateView):

    template_name = 'label/label.html'

    def get(self, request, id, slug):
        label = get_object_or_404(Label.objects.select_related('parent'), id=id)
        return self.render_to_response({
            'label': label,
            'label_children_list': label.children.annotate(count=Count('video'), children_count=Count('children')),
            'video_list': label.video_set.order_by('-created_on'),
        })


class LabelEditView(StaffOnlyView):

    template_name = 'label/label-edit.html'

    def get(self, request, id, slug):
        label = get_object_or_404(Label.objects.select_related('parent'), id=id)
        return self.render_to_response({
            'label': label,
            'form': LabelForm(instance=label),
        })

    def post(self, request, id, slug):
        label = get_object_or_404(Label.objects.select_related('parent'), id=id)
        form = LabelForm(instance=label, data=request.POST)
        if form.is_valid():
            label = form.save()
            return redirect('label', id=label.id, slug=label.slug)

        return self.render_to_response({
            'label': label,
            'form': form,
        })
