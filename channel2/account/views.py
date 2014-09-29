from django.contrib import messages

from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import View

from channel2.account.forms import AccountLoginForm, AccountActivateForm, \
    AccountPasswordResetForm, AccountPasswordSetForm
from channel2.account.models import User
from channel2.core.views import TemplateView, ProtectedTemplateView


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


class AccountLogoutView(View):

    def get(self, request):
        return redirect('home')

    def post(self, request):
        logout(request)
        return redirect('account.login')


class AccountActivateView(TemplateView):

    template_name = 'account/account-activate.html'

    def get(self, request, token):
        user = get_object_or_404(User, token=token, is_active=False)
        messages.warning(request, 'Please set a password')
        return self.render_to_response({
            'form': AccountActivateForm(user=user)
        })

    def post(self, request, token):
        user = get_object_or_404(User, token=token, is_active=False)
        form = AccountActivateForm(user=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

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
            messages.warning(request, 'An email with a link to reset password has been sent to you.')
            return redirect('account.login')

        return self.render_to_response({
            'form': form,
        })


class AccountPasswordSetView(TemplateView):

    template_name = 'account/account-password-set.html'

    def get(self, request, token):
        user = get_object_or_404(User, token=token, is_active=True)
        messages.warning(request, 'Please set a password')
        return self.render_to_response({
            'form': AccountPasswordSetForm(user=user),
        })

    def post(self, request, token):
        user = get_object_or_404(User, token=token, is_active=True)
        form = AccountPasswordSetForm(user=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

        return self.render_to_response({
            'form': form,
        })


class AccountSettingsView(ProtectedTemplateView):

    template_name = 'account/account-settings.html'

    def get(self, request):
        return self.render_to_response({})

    def post(self, request):
        return self.render_to_response({})
