# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.exceptions import ValidationError
from django.http import HttpResponseNotAllowed
from django.views.generic.base import View

from cadizm.headspace.http import (
    CreateUserResponse,
    CreateBookResponse,
    AddBookResponse,
    DeleteBookResponse,
    MarkBookReadResponse,
    MarkBookUnreadResponse,
    ListBooksResponse,
    ErrorResponse)

from cadizm.headspace.models import User, Book, Library


class BaseView(View):
    methods = []
    json = None

    def dispatch(self, *args, **kwargs):
        if self.request.method not in self.methods:
            return HttpResponseNotAllowed(self.methods)

        if self.request.content_type == 'application/json':
            try:
                self.json = json.loads(self.request.body)
            except ValueError:
                return ErrorResponse(reason="Invalid JSON body")

        return super(BaseView, self).dispatch(*args, **kwargs)


class CreateUserView(BaseView):
    methods = ['POST']

    def post(self, *args, **kwargs):
        try:
            username = self.json.get('username', None)
            book_ids = self.json.get('book_ids', None)
            if not username:
                raise ValidationError('Missing or empty username')

            return CreateUserResponse(User.objects.create(username=username), book_ids)

        except ValidationError as e:
            return ErrorResponse(reason=e.message)


class CreateBookView(BaseView):
    methods = ['POST']

    def post(self, *args, **kwargs):
        try:
            title = self.json.get('title', None)
            author = self.json.get('author', None)
            if not title or not author:
                raise ValidationError('Missing or empty title/author')

            return CreateBookResponse(Book.objects.create(title=title, author=author))

        except ValidationError as e:
            return ErrorResponse(reason=e.message)


class AddDeleteBookView(BaseView):
    methods = ['POST', 'DELETE']

    def post(self, *args, **kwargs):
        try:
            user = User.objects.get(username=kwargs['username'])
            book = Book.objects.get(id=kwargs['book_id'])

            return AddBookResponse(Library.objects.create(user=user, book=book))

        except (User.DoesNotExist, Book.DoesNotExist) as e:
            return ErrorResponse(reason='Invalid username/book_id')
        except ValidationError as e:
            return ErrorResponse(reason=e.message)

    def delete(self, *args, **kwargs):
        try:
            user = User.objects.get(username=kwargs['username'])
            book = Book.objects.get(id=kwargs['book_id'])
            library_book = Library.objects.get(user=user, book=book)

            return DeleteBookResponse(library_book.delete())

        except (User.DoesNotExist, Book.DoesNotExist, Library.DoesNotExist) as e:
            return ErrorResponse(reason='Invalid username/book_id/library book')
        except ValidationError as e:
            return ErrorResponse(reason=e.message)


class MarkBookReadView(BaseView):
    methods = ['PUT']

    def put(self, *args, **kwargs):
        try:
            user = User.objects.get(username=kwargs['username'])
            book = Book.objects.get(id=kwargs['book_id'])
            library_book = Library.objects.get(user=user, book=book)
            library_book.read = True
            library_book.save()

            return MarkBookReadResponse()

        except (User.DoesNotExist, Book.DoesNotExist, Library.DoesNotExist) as e:
            return ErrorResponse(reason='Invalid username/book_id/library book')
        except ValidationError as e:
            return ErrorResponse(reason=e.message)


class MarkBookUnreadView(BaseView):
    methods = ['PUT']

    def put(self, *args, **kwargs):
        try:
            user = User.objects.get(username=kwargs['username'])
            book = Book.objects.get(id=kwargs['book_id'])
            library_book = Library.objects.get(user=user, book=book)
            library_book.read = False
            library_book.save()

            return MarkBookUnreadResponse()

        except (User.DoesNotExist, Book.DoesNotExist, Library.DoesNotExist) as e:
            return ErrorResponse(reason='Invalid username/book_id/library book')
        except ValidationError as e:
            return ErrorResponse(reason=e.message)


class ListBooksView(BaseView):
    methods = ['GET']

    def get(self, *args, **kwargs):
        try:
            kwargs = dict(user=User.objects.get(username=kwargs['username']))
            if 'read' in self.request.GET:
                kwargs.update(read=self.request.GET['read'])
            if 'author' in self.request.GET:
                kwargs.update(book__author__icontains=self.request.GET['author'])
            library_books = Library.objects.filter(**kwargs)

            return ListBooksResponse(library_books)

        except User.DoesNotExist as e:
            return ErrorResponse(reason='Invalid username')
        except ValidationError as e:
            return ErrorResponse(reason=e.message)
