# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time

from django.conf import settings
from django.db import models

from faker import Faker
from stringcase import snakecase
import stripe


class TeeNotFound(Exception):
    pass


class Tee(object):
    def __init__(self, **kwargs):
        self.slug = kwargs.get('slug', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.price_cents = kwargs.get('price_cents', None)

    @property
    def price(self):
        return "$%.2f" % (self.price_cents / 100.0)

    @classmethod
    def find(clazz, name):
        try:
            return ACTIVE_TEES[name]
        except:
            raise TeeNotFound("TeeNotFound: %s" % name)


ACTIVE_TEES = {
    'broken-heart-white': Tee(
        slug='broken-heart-white',
        name='Broken Heart',
        description='White cotton tee with broken-hearted chest logo.',
        price_cents=4200,
        ),

    'broken-heart-black': Tee(
        slug='broken-heart-black',
        name='broken heart',
        description='Black cotton tee with broken-hearted chest logo.',
        price_cents=4200,
        ),
}


class OrderManager(models.Manager):
    fake = Faker()

    def create(self, **kwargs):
        def f(k):
            return snakecase(k.replace('stripe', ''))

        kwargs = {f(k): v for k,v in kwargs.items() if f(k) in self.field_names}
        kwargs.update(number=self.generate_order_number())

        return super(OrderManager, self).create(**kwargs)

    @property
    def field_names(self):
        res = set()
        for field in Order._meta.get_fields():
            if field.name not in ('id', 'created'):
                res.add(field.name)
        return res

    def generate_order_number(self):
        return "%s%s" % (self.fake.word(), int((time.time() % 1 ) * 10000))


class Order(models.Model):
    objects = OrderManager()

    number = models.CharField(max_length=128)
    tee_slug = models.CharField(max_length=128)
    amount = models.PositiveIntegerField()
    email = models.CharField(max_length=128)
    token = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)

    billing_address_city = models.CharField(max_length=128)
    billing_address_country = models.CharField(max_length=128)
    billing_address_country_code = models.CharField(max_length=128)
    billing_address_line1 = models.CharField(max_length=128)
    billing_address_state = models.CharField(max_length=128)
    billing_address_zip = models.CharField(max_length=128)
    billing_name = models.CharField(max_length=128)

    shipping_address_city = models.CharField(max_length=128)
    shipping_address_country = models.CharField(max_length=128)
    shipping_address_country_code = models.CharField(max_length=128)
    shipping_address_line1 = models.CharField(max_length=128)
    shipping_address_state = models.CharField(max_length=128)
    shipping_address_zip = models.CharField(max_length=128)
    shipping_name = models.CharField(max_length=128)


class StripeChargeManager(models.Manager):
    stripe.api_key = settings.CADIZM_STRIPE_SECRET_KEY

    def create(self, order, tee):
        assert isinstance(order, Order)

        metadata = dict(order_number=order.number)

        charge = stripe.Charge.create(
            amount=order.amount,
            currency='usd',
            description=tee.name[:21],  # max len
            metadata=metadata,
            receipt_email=order.email,
            source=order.token,
            statement_descriptor='cadizm.com order',
        )

        if charge.status != 'succeeded':
            raise Exception("Charge failed")

        kwargs = dict(
            order=order,
            amount=charge.amount,
            description=charge.description,
            receipt_email=charge.receipt_email,
            stripe_id=charge.id,
        )

        return super(StripeChargeManager, self).create(**kwargs)

    @property
    def field_names(self):
        res = set()
        for field in Order._meta.get_fields():
            if field.name not in ('id', 'created'):
                res.add(field.name)
        return res

    def generate_order_number(self):
        return "%s%s" % (self.fake.word(), int((time.time() % 1 ) * 10000))


class StripeCharge(models.Model):
    objects = StripeChargeManager()
    created = models.DateTimeField(auto_now_add=True)

    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField()
    description = models.CharField(max_length=128)
    receipt_email = models.CharField(max_length=128)
    stripe_id = models.CharField(max_length=128)
