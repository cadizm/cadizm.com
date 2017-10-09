# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import combinations
import random
import string

from faker import Faker

from cadizm.headspace.models import User, Book, Library
from cadizm.headspace.tests import BaseTestCase


class ListBooksTestCase(BaseTestCase):
    def setUp(self, *args, **kwargs):
        super(ListBooksTestCase, self).setUp(*args, **kwargs)
        self.fake = Faker()
        self.user = User.objects.create(username=self.fake.user_name()[:32])
        self.url = '/headspace/users/{username}/books/'.format(username=self.user.username)

    def test_list_has_no_books(self):
        self.assertEqual(0, Library.objects.filter(user=self.user).count())
        response = self.client.get(self.url.format(self.url))
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json()['result']['books'])

    def test_list_has_books(self):
        books = [self._create_random_book() for _ in range(random.randint(1, 100))]
        for book in books:
            self._add_book(book)
        self.assertEqual(len(books), Library.objects.filter(user=self.user).count())
        response = self.client.get(self.url.format(self.url))
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(books), len(response.json()['result']['books']))

    def test_list_add_book(self):
        book = self._create_random_book()
        self._add_book(book)
        self.assertEqual(1, Library.objects.filter(user=self.user).count())
        response = self.client.get(self.url.format(self.url))
        self.assertEqual(200, response.status_code)

        books = response.json()['result']['books']
        self.assertEqual(1, len(books))
        self.assertEqual(book.id, books[0]['book_id'])
        self.assertEqual(book.title, books[0]['title'])
        self.assertEqual(book.author, books[0]['author'])

    def test_list_delete_book(self):
        book = self._create_random_book()
        self._add_book(book)
        self.assertEqual(1, Library.objects.filter(user=self.user).count())
        response = self.client.get(self.url.format(self.url))
        self.assertEqual(200, response.status_code)
        books = response.json()['result']['books']

        self._delete_book(book)
        self.assertEqual(0, Library.objects.filter(user=self.user).count())
        response = self.client.get(self.url.format(self.url))
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json()['result']['books'])

    def test_list_by_author_author_matches(self):
        book = self._create_random_book()
        self._add_book(book)
        self.assertEqual(1, Library.objects.filter(user=self.user).count())

        authors = [ss for ss in self._all_substrings(book.author)]
        authors = random.sample(authors, 10)  # 10 random substrings of author's name

        for author in authors:
            response = self.client.get(self.url.format(self.url), {'author': author})
            self.assertEqual(200, response.status_code)
            self.assertEqual(1, len(response.json()['result']['books']))

    def test_list_by_author_author_doesnt_match(self):
        book = self._create_random_book()
        self._add_book(book)
        self.assertEqual(1, Library.objects.filter(user=self.user).count())

        authors = [ss for ss in self._all_substrings(book.author)]
        authors = random.sample(authors, 10)

        for author in authors:
            if len(author) == 1:
                continue  # single letter still matches
            author = list(author)  # split string into list of char
            random.shuffle(author)  # in-place jumble
            author = ''.join(author) + random.choice(string.digits)  # back to string plus random
            response = self.client.get(self.url.format(self.url), {'author': author})
            self.assertEqual(200, response.status_code)
            self.assertEqual(0, len(response.json()['result']['books']))

    def test_list_all_read_or_unread_books(self):
        books = [self._create_random_book() for _ in range(random.randint(1, 100))]
        for book in books:
            self._add_book(book, read=False)
        self.assertEqual(len(books), Library.objects.filter(user=self.user).count())

        response = self.client.get(self.url.format(self.url), {'read': True})
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json()['result']['books'])

        response = self.client.get(self.url.format(self.url), {'read': False})
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(books), len(response.json()['result']['books']))

    def test_list_some_read_some_unread_books(self):
        unread_books = [self._create_random_book() for _ in range(random.randint(1, 50))]
        for book in unread_books:
            self._add_book(book, read=False)

        read_books = [self._create_random_book() for _ in range(random.randint(1, 50))]
        for book in read_books:
            self._add_book(book, read=True)

        self.assertEqual(len(unread_books), Library.objects.filter(user=self.user, read=False).count())
        self.assertEqual(len(read_books), Library.objects.filter(user=self.user, read=True).count())
        self.assertEqual(len(unread_books+read_books), Library.objects.filter(user=self.user).count())

        response = self.client.get(self.url.format(self.url), {'read': False})
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(unread_books), len(response.json()['result']['books']))

        response = self.client.get(self.url.format(self.url), {'read': True})
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(read_books), len(response.json()['result']['books']))

    def test_invalid_userame(self):
        response = self.client.get('/headspace/users/badusername/books/')
        self.assertEquals(400, response.status_code)
        self.assertEquals('Invalid username', response.json()['meta']['reason'])

    # helper methods
    def _create_random_book(self):
        return Book.objects.create(title=self.fake.catch_phrase()[:128], author=self.fake.name()[:128])

    def _add_book(self, book, read=False):
        Library.objects.create(user=self.user, book=book, read=read)

    def _delete_book(self, book):
        Library.objects.get(user=self.user, book=book).delete()

    def _all_substrings(self, s):
        n = len(s)
        for i in range(n):
            for j in range(i+1, n+1):
                yield s[i:j]
