# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from cadizm.headspace.views import (
    UserView,
    BookView,
    AddDeleteBookView,
    MarkBookReadView,
    MarkBookUnreadView,
    ListLibraryView)


urlpatterns = [
    url(r'^users/$', csrf_exempt(UserView.as_view()), name='create_user'),
    url(r'^books/$', csrf_exempt(BookView.as_view()), name='create_book'),
    url(r'^users/(?P<username>(\w+|(?:-|_)*)+)/books/$', csrf_exempt(ListLibraryView.as_view()), name='list_library'),
    url(r'^users/(?P<username>(\w+|(?:-|_)*)+)/books/(?P<book_id>(\d+))/$', csrf_exempt(AddDeleteBookView.as_view()), name='add_delete_book'),
    url(r'^users/(?P<username>(\w+|(?:-|_)*)+)/books/(?P<book_id>(\d+))/read/$', csrf_exempt(MarkBookReadView.as_view()), name='mark_book_read'),
    url(r'^users/(?P<username>(\w+|(?:-|_)*)+)/books/(?P<book_id>(\d+))/unread/$', csrf_exempt(MarkBookUnreadView.as_view()), name='mark_book_unread'),
]
