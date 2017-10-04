# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    created = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
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
