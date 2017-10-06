# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseNotAllowed
from django.views.generic.base import View

# TODO: remove me
from django.http import HttpResponse

from cadizm.headspace.http import (
    CreateUserResponse,
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

        except (ValidationError, IntegrityError) as e:
            reason = e.message
            if isinstance(e, IntegrityError):
                reason = 'Username already exists'
            return ErrorResponse(reason=reason)


class CreateBookView(BaseView):
    methods = ['POST']

    def post(self, *args, **kwargs):
        return HttpResponse("CreateBookView")


class ListBooksView(BaseView):
    methods = ['GET']

    def get(self, *args, **kwargs):
        return HttpResponse("ListBooksView")


class AddDeleteBookView(BaseView):
    methods = ['POST', 'DELETE']

    def post(self, *args, **kwargs):
        return HttpResponse("AddDeleteBookView")

    def delete(self, *args, **kwargs):
        return HttpResponse("AddDeleteBookView")


class MarkBookReadView(BaseView):
    methods = ['PUT']

    def put(self, *args, **kwargs):
        return HttpResponse("MarkBookReadView")


class MarkBookUnreadView(BaseView):
    methods = ['PUT']

    def put(self, *args, **kwargs):
        return HttpResponse("MarkBookUnreadView")
