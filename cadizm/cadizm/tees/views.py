# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic.base import TemplateView, View

import stripe

from cadizm.tees.models import Tee, Order, StripeCharge

import logging
logger = logging.getLogger(__name__)


class BaseTemplateView(TemplateView):
    def get_context_data(self, *args, **kwargs):
        context = super(BaseTemplateView, self).get_context_data(*args, **kwargs)

        context.update(
            now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            year=datetime.datetime.now().year,
            stripe_pub_key=settings.CADIZM_STRIPE_PUB_KEY,
        )

        return context


class TeeMixin(object):
    order = None

    def dispatch(self, *args, **kwargs):
        try:
            tee_slug = self.order.tee_slug if self.order else kwargs['tee']
            self.tee = Tee.find(tee_slug)
        except:
            raise Http404("TeeNotFound: %s" % kwargs['tee'])
        return super(TeeMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(TeeMixin, self).get_context_data(*args, **kwargs)
        context.update(tee=self.tee)
        return context


class TeesView(BaseTemplateView):
    template_name = 'tees/index.html'


class TeeView(TeeMixin, BaseTemplateView):
    template_name = 'tee/index.html'


class TeesCheckoutView(TeeMixin, View):
    def post(self, *args, **kwargs):
        kwargs = self.request.POST.dict()

        kwargs.update(
            tee_slug=self.tee.slug,
            amount=self.tee.amount,
        )

        try:
            order = Order.objects.create(**kwargs)
            charge = StripeCharge.objects.create(order, self.tee)
        except Exception as e:
            logger.exception(e)
            return HttpResponseRedirect(reverse('checkout_error'))

        self.send_confirmation_email(order)

        kwargs = dict(number=charge.order.number)
        return HttpResponseRedirect(reverse('confirmation', kwargs=kwargs))

    def send_confirmation_email(self, order):
        email = EmailMessage(
            subject="Order# %s Confirmation" % order.number,
            body=order.text_email_body,
            from_email="cadizm.com <%s>" % settings.EMAIL_HOST_USER,
            to=[order.email],
            bcc=[settings.EMAIL_HOST_USER],
        )
        try:
            email.send()
        except Exception as e:
            logger.exception(e)


class CheckoutConfirmationView(TeeMixin, BaseTemplateView):
    template_name = 'checkout/confirmation.html'

    def dispatch(self, *args, **kwargs):
        try:
            self.order = Order.objects.get(number=kwargs['number'])
        except:
            raise Http404("Order Not Found: %s" % kwargs['number'])
        return super(CheckoutConfirmationView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutConfirmationView, self).get_context_data(*args, **kwargs)
        context.update(order=self.order)
        return context


class CheckoutErrorView(BaseTemplateView):
    template_name = 'checkout/error.html'
