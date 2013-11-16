from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from channel2.core.views import ProtectedTemplateView
from channel2.label.models import Label


class LabelListView(ProtectedTemplateView):

    template_name = 'label/label-list.html'

    def get(self, request):
        return self.render_to_response({
            'label_list': Label.objects.annotate(count=Count('video')),
        })


class LabelView(ProtectedTemplateView):

    template_name = 'label/label.html'

    def get(self, request, id, slug):
        label = get_object_or_404(Label, id=id)
        return self.render_to_response({
            'label': label,
            'label_list': label.children.annotate(count=Count('video')),
        })
