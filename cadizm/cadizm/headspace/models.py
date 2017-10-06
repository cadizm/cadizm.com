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
            raise ValidationError('Invalid username')
        return super(UserManager, self).create(**kwargs)

class User(models.Model):
    objects = UserManager()
    username = models.CharField(max_length=32, unique=True)
    created = models.DateTimeField(auto_now_add=True)


class BookManager(models.Manager):
    def create(self, **kwargs):
        kwargs.update(slug=parameterize("%s %s" % (kwargs['author'], kwargs['title'])))
        return super(BookManager, self).create(**kwargs)


class Book(models.Model):
    objects = BookManager()
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    slug = models.SlugField(max_length=512, unique=True)
    created = models.DateTimeField(auto_now_add=True)


class Library(models.Model):
    username = models.ForeignKey(User, to_field='username', on_delete=models.PROTECT)
    book_id = models.ForeignKey(Book, on_delete=models.PROTECT)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
