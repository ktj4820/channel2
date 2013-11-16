from channel2.core.views import ProtectedTemplateView


class FlatHelpView(ProtectedTemplateView):

    template_name = 'flat/flat-help.html'
