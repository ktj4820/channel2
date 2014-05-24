from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from channel2.core.views import StaffTemplateView
from channel2.staff.forms import StaffAccountCreateForm


class StaffUserAddView(StaffTemplateView):

    template_name = 'staff/staff-user-add.html'

    def get(self, request):
        return self.render_to_response({
            'form': StaffAccountCreateForm()
        })

    def post(self, request):
        form = StaffAccountCreateForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, _('An activation email has been sent to {}').format(user.email))
            return redirect('staff.user.add')

        return self.render_to_response({
            'form': form,
        })
