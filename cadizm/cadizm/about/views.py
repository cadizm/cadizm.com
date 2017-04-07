
from django.views.generic.base import TemplateView


class PrivacyView(TemplateView):
    template_name = 'privacy/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PrivacyView, self).get_context_data(*args, **kwargs)
        return context
