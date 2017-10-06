# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import Client

from cadizm.headspace.models import User, Book
from cadizm.headspace.tests import BaseTestCase


class CreateUserTestCase(BaseTestCase):
    def setUp(self, *args, **kwargs):
        self.url = '/headspace/users/'
        super(CreateUserTestCase, self).setUp(*args, **kwargs)

    def test_valid_username_no_books(self):
        self.assertEquals(0, User.objects.count())
        response = self.post(self.url, {'username': 'foo'})
        self.assertEquals(201, response.status_code)
        self.assertEquals(1, User.objects.count())
        self.assertEquals('foo', response.json()['result']['username'])

    def test_username_empty(self):
        response = self.post(self.url, {'username': ''})
        self.assertEquals(400, response.status_code)
        self.assertEquals('Missing or empty username', response.json()['meta']['reason'])

    def test_username_missing(self):
        response = self.post(self.url, {})
        self.assertEquals(400, response.status_code)
        self.assertEquals('Missing or empty username', response.json()['meta']['reason'])

    def test_bad_json(self):
        # manually create client in order to send bad json
        response = Client().post(self.url, data='{invalid json}}', content_type='application/json')
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid JSON body', response.json()['meta']['reason'])

    def test_username_already_exists(self):
        response = self.post(self.url, {'username': 'baz'})
        self.assertEquals(201, response.status_code)
        response = self.post(self.url, {'username': 'baz'})
        self.assertEquals(400, response.status_code)

    def test_valid_username_all_valid_book_ids(self):
        book_ids = [
            Book.objects.create(title='yoyo', author='ma').id,
            Book.objects.create(title='siegfried', author='roy').id,
        ]
        response = self.post(self.url, {'username': 'baz', 'book_ids': book_ids})
        result = response.json()['result']
        self.assertEqual(set(book_ids), set(result['book_ids']))

    def test_valid_username_all_invalid_book_ids(self):
        invalid_book_ids = [2, 17]
        response = self.post(self.url, {'username': 'baz', 'book_ids': invalid_book_ids})
        result = response.json()['result']
        self.assertEqual(set(invalid_book_ids), set(result['invalid_book_ids']))

    def test_valid_username_mixed_valid_invalid_book_ids(self):
        invalid_book_ids = [2, 17]
        book_ids = [
            Book.objects.create(title='yoyo', author='ma').id,
            Book.objects.create(title='siegfried', author='roy').id,
        ]
        response = self.post(self.url, {'username': 'baz', 'book_ids': book_ids + invalid_book_ids})
        result = response.json()['result']
        self.assertEqual(set(book_ids), set(result['book_ids']))
        self.assertEqual(set(invalid_book_ids), set(result['invalid_book_ids']))

    def test_username_format(self):
        # nominal
        self.assertEqual(201, self.post(self.url, {'username': 'roys2017'}).status_code)

        # max username length
        username = 'foobarbazbammabzabraboof_123-456'
        self.assertEqual(32, len(username))
        self.assertEqual(201, self.post(self.url, {'username': username}).status_code)

        # invalid username length
        username += 'z'
        self.assertEqual(33, len(username))
        self.assertEqual(400, self.post(self.url, {'username': username}).status_code)

        # invalid username characters
        self.assertEqual(400, self.post(self.url, {'username': 'e{M(({TS'}).status_code)
