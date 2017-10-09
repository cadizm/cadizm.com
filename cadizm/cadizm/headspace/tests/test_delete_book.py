# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cadizm.headspace.models import User, Book, Library
from cadizm.headspace.tests import BaseTestCase


class DeleteBookTestCase(BaseTestCase):
    def setUp(self, *args, **kwargs):
        super(DeleteBookTestCase, self).setUp(*args, **kwargs)
        self.url = '/headspace/users/{username}/books/{book_id}/'

    def test_valid_book_deleted(self):
        user = User.objects.create(username='foo')
        book = Book.objects.create(title='bar', author='baz')
        Library.objects.create(user=user, book=book)
        self.assertEquals(1, Library.objects.count())

        kwargs = {
            'username': user.username,
            'book_id': book.id,
        }
        response = self.client.delete(self.url.format(**kwargs))
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, Library.objects.count())

    def test_book_not_added_to_library(self):
        user = User.objects.create(username='foo')
        book = Book.objects.create(title='bar', author='baz')
        self.assertEquals(0, Library.objects.count())

        kwargs = {
            'username': user.username,
            'book_id': book.id,
        }
        response = self.client.delete(self.url.format(**kwargs))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username/book_id', response.json()['meta']['reason'])

    def test_delete_twice(self):
        user = User.objects.create(username='foo')
        book = Book.objects.create(title='bar', author='baz')
        Library.objects.create(user=user, book=book)
        self.assertEquals(1, Library.objects.count())

        kwargs = {
            'username': user.username,
            'book_id': book.id,
        }
        response = self.client.delete(self.url.format(**kwargs))
        self.assertEquals(200, response.status_code)
        self.assertEquals(0, Library.objects.count())

        response = self.client.delete(self.url.format(**kwargs))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username/book_id', response.json()['meta']['reason'])

    def test_invalid_username(self):
        kwargs = {
            'username': 'badname',
            'book_id': Book.objects.create(title='bar', author='baz').id,
        }
        response = self.client.delete(self.url.format(**kwargs))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username/book_id', response.json()['meta']['reason'])

    def test_invalid_book_id(self):
        kwargs = {
            'username': User.objects.create(username='foo').username,
            'book_id': 23,
        }
        response = self.client.delete(self.url.format(**kwargs))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username/book_id', response.json()['meta']['reason'])
