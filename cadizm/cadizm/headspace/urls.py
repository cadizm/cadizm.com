# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from cadizm.headspace.views import (
    CreateUserView,
    CreateBookView,
    ListBooksView,
    AddDeleteBookView,
    MarkBookReadView,
    MarkBookUnreadView,
    )


urlpatterns = [
    url(r'^users/$', csrf_exempt(CreateUserView.as_view()), name='create_user'),
    url(r'^books/$', csrf_exempt(CreateBookView.as_view()), name='create_book'),

    url(r'^users/(?P<username>(\w+|(?:-|_)*)+)/books/$', csrf_exempt(ListBooksView.as_view()), name='list_books'),
    url(r'^users/(?P<username>(\w+|(?:-|_)*)+)/books/(?P<book_id>(\d+))/$', csrf_exempt(AddDeleteBookView.as_view()), name='add_delete_book'),

    url(r'^users/(?P<username>(\w+|(?:-|_)*)+)/books/(?P<book_id>(\d+))/read/$', csrf_exempt(MarkBookReadView.as_view()), name='mark_book_read'),
    url(r'^users/(?P<username>(\w+|(?:-|_)*)+)/books/(?P<book_id>(\d+))/unread/$', csrf_exempt(MarkBookUnreadView.as_view()), name='mark_book_unread'),
]
