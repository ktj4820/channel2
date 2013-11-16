from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView as DjangoTemplateview


class TemplateView(DjangoTemplateview):
    """
    Any view that extends from BaseTemplateView has {{ TEMPLATE_NAME }}
    available to use.
    """

    def render_to_response(self, context, **response_kwargs):
        context['TEMPLATE_NAME'] = self.template_name.split('/')[-1].split('.')[0]
        return super().render_to_response(context, **response_kwargs)


class ProtectedTemplateView(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class StaffOnlyView(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
