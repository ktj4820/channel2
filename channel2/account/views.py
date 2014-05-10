from channel2.core.views import TemplateView


class AccountLoginView(TemplateView):

    template_name = 'account/account-login.html'

    def get(self, request):
        return self.render_to_response({})

    def post(self, request):
        return self.render_to_response({})
