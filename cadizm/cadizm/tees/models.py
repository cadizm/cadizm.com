# -*- coding: utf-8 -*-
from __future__ import unicode_literals


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
        return ACTIVE_TEES.get(name, None)


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
