# -*- coding: utf-8 -*-
from __future__ import unicode_literals


ACTIVE_TEES = [
    'stock1',
]


def active_tee(tee):
    return tee in ACTIVE_TEES
