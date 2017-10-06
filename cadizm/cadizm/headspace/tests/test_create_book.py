# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cadizm.headspace.models import Book
from cadizm.headspace.tests import BaseTestCase


class CreateBookTestCase(BaseTestCase):
    def setUp(self, *args, **kwargs):
        self.url = '/headspace/books/'
        super(CreateBookTestCase, self).setUp(*args, **kwargs)

    def test_valid_title_author(self):
        self.assertEquals(0, Book.objects.count())
        title = "A Midsummer Night's Dream"
        author = "William Shakespeare"

        response = self.post(self.url, dict(title=title, author=author))
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, Book.objects.count())
        self.assertEquals(title, response.json()['result']['title'])
        self.assertEquals(author, response.json()['result']['author'])

    def test_title_empty(self):
        response = self.post(self.url, dict(title='', author='Shakespeare'))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Missing or empty title/author', response.json()['meta']['reason'])

    def test_title_missing(self):
        response = self.post(self.url, dict(author='Shakespeare'))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Missing or empty title/author', response.json()['meta']['reason'])

    def test_author_empty(self):
        response = self.post(self.url, dict(title="A Midsummer Night's Dream", author=''))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Missing or empty title/author', response.json()['meta']['reason'])

    def test_author_missing(self):
        response = self.post(self.url, dict(title="A Midsummer Night's Dream"))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Missing or empty title/author', response.json()['meta']['reason'])

    def test_invalid_lengths(self):
        response = self.post(self.url, dict(title='a', author=('b' * 129)))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid title/author length', response.json()['meta']['reason'])

        response = self.post(self.url, dict(title=('a' * 129), author='b'))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid title/author length', response.json()['meta']['reason'])

    def test_title_already_exists(self):
        title = "A Midsummer Night's Dream"
        author = "William Shakespeare"

        response = self.post(self.url, dict(title=title, author=author))
        self.assertEquals(201, response.status_code)
        response = self.post(self.url, dict(title=title, author=author))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Book already exists', response.json()['meta']['reason'])
