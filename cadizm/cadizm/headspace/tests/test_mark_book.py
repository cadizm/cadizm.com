# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cadizm.headspace.models import User, Book, Library
from cadizm.headspace.tests import BaseTestCase


class MarkBookReadTestCase(BaseTestCase):
    def setUp(self, *args, **kwargs):
        super(MarkBookReadTestCase, self).setUp(*args, **kwargs)
        self.url = '/headspace/users/{username}/books/{book_id}/read/'
        self.user = User.objects.create(username='foo')
        self.book = Book.objects.create(title='bar', author='baz')
        self.library_book = Library.objects.create(user=self.user, book=self.book)
        self.assertEquals(1, Library.objects.count())

    def test_mark_unread_book_read(self):
        self.assertFalse(self.library_book.read)
        response = self.client.put(self.url.format(username=self.user.username, book_id=self.book.id))
        self.assertEqual(200, response.status_code)
        self.library_book.refresh_from_db()
        self.assertTrue(self.library_book.read)

    def test_mark_read_book_read(self):
        self.library_book.read = True
        self.library_book.save()
        self.assertTrue(self.library_book.read)
        response = self.client.put(self.url.format(username=self.user.username, book_id=self.book.id))
        self.assertEqual(200, response.status_code)
        self.library_book.refresh_from_db()
        self.assertTrue(self.library_book.read)

    def test_invalid_username(self):
        response = self.client.put(self.url.format(username='badusername', book_id=self.book.id))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username/book_id/library book', response.json()['meta']['reason'])

    def test_invalid_book_id(self):
        response = self.client.put(self.url.format(username=self.user.username, book_id=712))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username/book_id/library book', response.json()['meta']['reason'])

    def test_invalid_library_book(self):
        self.library_book.delete()
        response = self.client.put(self.url.format(username=self.user.username, book_id=self.book.id))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username/book_id/library book', response.json()['meta']['reason'])


class MarkBookUnreadTestCase(BaseTestCase):
    def setUp(self, *args, **kwargs):
        super(MarkBookUnreadTestCase, self).setUp(*args, **kwargs)
        self.url = '/headspace/users/{username}/books/{book_id}/unread/'
        self.user = User.objects.create(username='foo')
        self.book = Book.objects.create(title='bar', author='baz')
        self.library_book = Library.objects.create(user=self.user, book=self.book)
        self.assertEquals(1, Library.objects.count())

    def test_mark_unread_book_unread(self):
        self.assertFalse(self.library_book.read)
        response = self.client.put(self.url.format(username=self.user.username, book_id=self.book.id))
        self.assertEqual(200, response.status_code)
        self.library_book.refresh_from_db()
        self.assertFalse(self.library_book.read)

    def test_mark_read_book_unread(self):
        self.library_book.read = True
        self.library_book.save()
        self.assertTrue(self.library_book.read)
        response = self.client.put(self.url.format(username=self.user.username, book_id=self.book.id))
        self.assertEqual(200, response.status_code)
        self.library_book.refresh_from_db()
        self.assertFalse(self.library_book.read)

    def test_invalid_username(self):
        response = self.client.put(self.url.format(username='badusername', book_id=self.book.id))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username/book_id/library book', response.json()['meta']['reason'])

    def test_invalid_book_id(self):
        response = self.client.put(self.url.format(username=self.user.username, book_id=712))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username/book_id/library book', response.json()['meta']['reason'])

    def test_invalid_library_book(self):
        self.library_book.delete()
        response = self.client.put(self.url.format(username=self.user.username, book_id=self.book.id))
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username/book_id/library book', response.json()['meta']['reason'])
