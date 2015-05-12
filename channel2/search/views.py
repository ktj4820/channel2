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

        filters = Q(name__icontains=query) | Q(markdown__icontains=query) | Q(json__icontains=query)
        tag_list = Tag.objects.filter(filters).order_by('name')
        return self.render_to_response({
            'tag_list': tag_list,
        })
