# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic.base import TemplateView, View

import stripe

from cadizm.tees.models import Tee, Order, StripeCharge

import logging
logger = logging.getLogger(__name__)


class TeesView(TemplateView):
    template_name = 'tees/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TeesView, self).get_context_data(*args, **kwargs)

        context.update(
            now=str(datetime.date.today()),
        )

        return context


class TeeMixin(object):
    def dispatch(self, *args, **kwargs):
        try:
            self.tee = Tee.find(kwargs['tee'])
        except:
            raise Http404("TeeNotFound: %s" % kwargs['tee'])
        return super(TeeMixin, self).dispatch(*args, **kwargs)


class TeeView(TeeMixin, TemplateView):
    template_name = 'tee/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TeeView, self).get_context_data(*args, **kwargs)

        context.update(
            tee=self.tee,
            year=datetime.datetime.now().year,
            stripe_pub_key=settings.CADIZM_STRIPE_PUB_KEY,
        )

        return context


class TeesCheckoutView(TeeMixin, View):
    def post(self, *args, **kwargs):
        kwargs = self.request.POST.dict()

        kwargs.update(
            tee_slug=self.tee.slug,
            amount=self.tee.price_cents,
        )

        try:
            order = Order.objects.create(**kwargs)
            charge = StripeCharge.objects.create(order, self.tee)
        except Exception as e:
            logger.exception(e)
            return HttpResponseRedirect(reverse('checkout_error'))

        kwargs = dict(number=charge.order.number)
        return HttpResponseRedirect(reverse('confirmation', kwargs=kwargs))


class CheckoutConfirmationView(TemplateView):
    template_name = 'checkout/confirmation.html'

    def dispatch(self, *args, **kwargs):
        try:
            self.order = Order.objects.get(number=kwargs['number'])
            self.tee = Tee.find(self.order.tee_slug)
        except:
            raise Http404("Order Not Found: %s" % kwargs['tee'])
        return super(CheckoutConfirmationView, self).dispatch(*args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutConfirmationView, self).get_context_data(*args, **kwargs)

        context.update(
            order=self.order,
            tee=self.tee,
            year=datetime.datetime.now().year,
        )

        return context


class CheckoutErrorView(TemplateView):
    template_name = 'checkout/error.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutErrorView, self).get_context_data(*args, **kwargs)

        context.update(
            year=datetime.datetime.now().year,
        )

        return context
