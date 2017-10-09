# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.core.exceptions import ValidationError
from django.db import models

from inflection import parameterize


class UserManager(models.Manager):
    def create(self, **kwargs):
        username = kwargs['username']
        match = re.match(r'^([a-zA-Z0-9\-_]+)$', username)

        if len(username) < 0 or len(username) > 32 or not match:
            raise ValidationError('Invalid username length/format')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')

        return super(UserManager, self).create(**kwargs)


class User(models.Model):
    objects = UserManager()
    username = models.CharField(max_length=32, unique=True)
    created = models.DateTimeField(auto_now_add=True)


class BookManager(models.Manager):
    def create(self, **kwargs):
        slug = parameterize("%s %s" % (kwargs['author'], kwargs['title']))
        kwargs.update(slug=slug)

        length = max(len(kwargs['title']), len(kwargs['author']))
        if length < 0 or length > 128:
            raise ValidationError('Invalid title/author length')
        if Book.objects.filter(slug=slug).exists():
            raise ValidationError('Book already exists')

        return super(BookManager, self).create(**kwargs)


class Book(models.Model):
    objects = BookManager()
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    slug = models.SlugField(max_length=512, unique=True)
    created = models.DateTimeField(auto_now_add=True)


class LibraryManager(models.Manager):
    def create(self, **kwargs):
        user, book = kwargs['user'], kwargs['book']

        if Library.objects.filter(user=user, book=book).exists():
            raise ValidationError('Book already added')

        return super(LibraryManager, self).create(**kwargs)


class Library(models.Model):
    objects = LibraryManager()
    user = models.ForeignKey(User, to_field='username', on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')
        indexes = [
            models.Index(fields=['user', 'book'], name='user_book_idx'),
        ]
