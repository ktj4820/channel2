from django.contrib.auth import logout, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from channel2.account.forms import AccountLoginForm
from channel2.core.views import TemplateView


class AccountLoginView(TemplateView):

    template_name = 'account/account-login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('video.list')
        return super(AccountLoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return self.render_to_response({
            'form': AccountLoginForm()
        })

    def post(self, request):
        form = AccountLoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get('next', reverse('video.list'))
            return redirect(next_url)
        return self.render_to_response({
            'form': form,
        })
