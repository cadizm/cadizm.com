# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse

from cadizm.headspace.models import Book


class BaseResponse(JsonResponse):
    def __init__(self, *args, **kwargs):
        self.status_code = kwargs.get('status', 200)
        self.reason = kwargs.get('reason', None)
        super(BaseResponse, self).__init__(self.response(), *args, **kwargs)

    def response(self):
        return dict(result=self.result(), meta=self.meta())

    def result(self):
        raise NotImplementedError

    def meta(self):
        meta = dict(status=self.status_code)
        if self.reason:
            meta.update(reason=self.reason)

        return meta


class ErrorResponse(BaseResponse):
    def __init__(self, *args, **kwargs):
        kwargs.update(status=400)
        super(ErrorResponse, self).__init__(*args, **kwargs)

    def result(self):
        pass


class CreateUserResponse(BaseResponse):
    def __init__(self, user, book_ids=None, invalid_book_ids=None, *args, **kwargs):
        kwargs.update(status=201)
        self.user = user
        self.book_ids, self.invalid_book_ids = self.validate_book_ids(book_ids)
        super(CreateUserResponse, self).__init__(*args, **kwargs)

    def result(self):
        result = dict(username=self.user.username)
        if self.book_ids:
            result.update(book_ids=self.book_ids)
        if self.invalid_book_ids:
            result.update(invalid_book_ids=self.invalid_book_ids)

        return result

    def validate_book_ids(self, book_ids):
        if not book_ids:
            return [], []

        valid_book_ids = set([b.id for b in Book.objects.filter(id__in=book_ids)])
        invalid_book_ids = set(book_ids) - valid_book_ids

        return list(valid_book_ids), list(invalid_book_ids)


class CreateBookResponse(BaseResponse):
    def __init__(self, book, *args, **kwargs):
        kwargs.update(status=201)
        self.book = book
        super(CreateBookResponse, self).__init__(*args, **kwargs)

    def result(self):
        return dict(title=self.book.title, author=self.book.author, book_id=self.book.id)
