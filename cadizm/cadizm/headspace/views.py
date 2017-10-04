# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.views.generic.base import View

from django.http import HttpResponse


from cadizm.headspace.exceptions import MethodNotAllowedError


class BaseView(View):
    methods = []
    json = None

    def dispatch(self, *args, **kwargs):
        if self.request.method not in self.methods:
            return HttpResponseBadRequest("Method Not Allowed", status=405)

        if self.request.content_type == 'application/json':
            try:
                self.json = json.loads(self.request.body)
            except ValueError:
                return HttpResponseBadRequest("Invalid JSON body")

        return super(BaseView, self).dispatch(*args, **kwargs)


class CreateUserView(BaseView):
    methods = ['POST']

    def post(self, *args, **kwargs):
        return HttpResponse("CreateUserView")


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
