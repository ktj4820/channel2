from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from channel2.account.forms import AccountLoginForm
from channel2.core.views import TemplateView


class AccountLoginView(TemplateView):

    template_name = 'account/account-login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return self.render_to_response({'form': AccountLoginForm(request)})

    def post(self, request):
        form = AccountLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.POST.get('next', reverse('home')))

        return self.render_to_response({'form': form})
