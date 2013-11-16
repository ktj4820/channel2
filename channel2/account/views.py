from django.contrib.auth import logout, login
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseNotAllowed
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic.base import View
from channel2.account.forms import AccountLoginForm, AccountActivateForm, AccountCreateForm
from channel2.account.models import User
from channel2.core.views import TemplateView, StaffOnlyView


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
        form = AccountLoginForm(request=request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get('next', reverse('video.list'))
            return redirect(next_url)
        return self.render_to_response({
            'form': form,
        })


class AccountLogoutView(View):

    def get(self, request):
        return HttpResponseNotAllowed(permitted_methods=['post'])

    def post(self, request):
        logout(request)
        return redirect('account.login')


class AccountActivateView(TemplateView):

    template_name = 'account/account-activate.html'

    def get(self, request, token):
        target_user = get_object_or_404(User, token=token)
        return self.render_to_response({
            'target_user': target_user,
            'form': AccountActivateForm(user=target_user),
        })

    def post(self, request, token):
        target_user = get_object_or_404(User, token=token)
        form = AccountActivateForm(user=target_user, data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('video.list')

        return self.render_to_response({
            'target_user': target_user,
            'form': form,
        })


class AccountCreateView(StaffOnlyView):

    template_name = 'account/account-create.html'

    def get(self, request):
        return self.render_to_response({
            'form': AccountCreateForm()
        })

    def post(self, request):
        form = AccountCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('An activation email has been sent to the user.'))
            return redirect('account.create')

        return self.render_to_response({
            'form': form,
        })
