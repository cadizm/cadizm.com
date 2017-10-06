# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cadizm.headspace.models import User, Book, Library
from cadizm.headspace.tests import BaseTestCase


class AddBookTestCase(BaseTestCase):
    def setUp(self, *args, **kwargs):
        self.url = '/headspace/users/{username}/books/{book_id}/'
        super(AddBookTestCase, self).setUp(*args, **kwargs)

    def test_valid_username_book_id(self):
        self.assertEquals(0, Library.objects.count())
        kwargs = {
            'username': User.objects.create(username='foo').username,
            'book_id': Book.objects.create(title='bar', author='baz').id,
        }

        response = self.post(self.url.format(**kwargs))
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, Library.objects.count())

    def test_book_unread(self):
        self.assertEquals(0, Library.objects.count())
        kwargs = {
            'username': User.objects.create(username='foo').username,
            'book_id': Book.objects.create(title='bar', author='baz').id,
        }
        response = self.post(self.url.format(**kwargs))
        self.assertEquals(1, Library.objects.count())
        library_book = Library.objects.first()
        self.assertFalse(library_book.read)

    def test_book_already_added(self):
        kwargs = {
            'username': User.objects.create(username='foo').username,
            'book_id': Book.objects.create(title='bar', author='baz').id,
        }
        response = self.post(self.url.format(**kwargs))
        self.assertEquals(200, response.status_code)
        response = self.post(self.url.format(**kwargs))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Book already added', response.json()['meta']['reason'])

    def test_invalid_username(self):
        kwargs = {
            'username': 'badname',
            'book_id': Book.objects.create(title='bar', author='baz').id,
        }
        response = self.post(self.url.format(**kwargs))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username/book_id', response.json()['meta']['reason'])

    def test_invalid_book_id(self):
        kwargs = {
            'username': User.objects.create(username='foo').username,
            'book_id': 23,
        }
        response = self.post(self.url.format(**kwargs))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username/book_id', response.json()['meta']['reason'])
