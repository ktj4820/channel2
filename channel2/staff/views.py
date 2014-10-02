from channel2.core.views import StaffTemplateView


class StaffUserAddView(StaffTemplateView):

    template_name = 'staff/staff-user-add.html'

    def get(self, request):
        return self.render_to_response({})

    def post(self, request):
        return self.render_to_response({})
