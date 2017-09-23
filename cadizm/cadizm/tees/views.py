# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.http import Http404
from django.views.generic.base import TemplateView

from cadizm.tees.models import active_tee


class TeesView(TemplateView):
    template_name = 'tees/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TeesView, self).get_context_data(*args, **kwargs)

        context.update(
            now=str(datetime.date.today()),
        )

        return context


class TeeView(TemplateView):
    template_name = 'tee/index.html'

    def dispatch(self, *args, **kwargs):
        self.tee = kwargs['tee']

        if not active_tee(self.tee):
            raise Http404("Inactive tee: %s" % self.tee)

        return super(TeeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(TeeView, self).get_context_data(*args, **kwargs)

        context.update(
            tee=self.tee,
            year=datetime.datetime.now().year,
        )

        return context
