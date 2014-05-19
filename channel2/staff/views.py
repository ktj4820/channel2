from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from channel2.account.models import User
from channel2.core.views import StaffTemplateView
from channel2.staff.forms import StaffAccountCreateForm


class StaffUserListView(StaffTemplateView):

    template_name = 'staff/staff-user-list.html'

    def get_context_data(self):
        return {'user_list': User.objects.order_by('email')}

    def get(self, request):
        context = self.get_context_data()
        context['form'] = StaffAccountCreateForm()
        return self.render_to_response(context)

    def post(self, request):
        form = StaffAccountCreateForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, _('An activation email has been sent to {}').format(user.email))
            return redirect('staff.user.list')

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
