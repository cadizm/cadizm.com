
from datetime import datetime

from django.views.generic.base import TemplateView


class Theta360View(TemplateView):
    template_name = 'theta360/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Theta360View, self).get_context_data(*args, **kwargs)

        context.update(
            current_year=datetime.now().year,
            )

        return context
