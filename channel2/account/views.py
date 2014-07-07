from django.contrib import messages
from django.contrib.auth import logout, login
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View

from channel2.account.forms import AccountLoginForm, AccountActivateForm, AccountPasswordResetForm, AccountPasswordSetForm
from channel2.account.models import User
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


class AccountLogoutView(View):

    def get(self, request):
        return redirect('video.list')

    def post(self, request):
        logout(request)
        return redirect('account.login')


class AccountActivateView(TemplateView):

    template_name = 'account/account-activate.html'

    def get(self, request, token):
        user = get_object_or_404(User, token=token)
        messages.warning(request, _('Please set a password'))
        return self.render_to_response({
            'form': AccountActivateForm(user=user)
        })

    def post(self, request, token):
        user = get_object_or_404(User, token=token)
        form = AccountActivateForm(user=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('video.list')

        return self.render_to_response({
            'form': form,
        })


class AccountPasswordResetView(TemplateView):

    template_name = 'account/account-password-reset.html'

    def get(self, request):
        return self.render_to_response({
            'form': AccountPasswordResetForm(),
        })

    def post(self, request):
        form = AccountPasswordResetForm(data=request.POST)
        if form.is_valid():
            form.reset_password()
            messages.warning(request, _('An email with a link to reset password has been sent to you.'))
            return redirect('account.login')

        return self.render_to_response({
            'form': form,
        })


class AccountPasswordSetView(TemplateView):

    template_name = 'account/account-password-set.html'

    def get(self, request, token):
        user = get_object_or_404(User, token=token)
        messages.warning(request, _('Please set a password'))
        return self.render_to_response({
            'form': AccountPasswordSetForm(user=user),
        })

    def post(self, request, token):
        user = get_object_or_404(User, token=token)
        form = AccountPasswordSetForm(user=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('video.list')

        return self.render_to_response({
            'form': form,
        })
