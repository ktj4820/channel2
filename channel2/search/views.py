from django.db.models.query_utils import Q
from django.shortcuts import redirect
from channel2.core.views import ProtectedTemplateView
from channel2.tag.models import Tag


class SearchView(ProtectedTemplateView):

    template_name = 'search/search.html'

    def get(self, request):
        query = request.GET.get('q')
        if not query:
            return redirect('home')

        tag_list = list(Tag.objects.filter(Q(name__icontains=query))) + list(Tag.objects.filter(Q(markdown__icontains=query)))
        return self.render_to_response({
            'tag_list': tag_list
        })
