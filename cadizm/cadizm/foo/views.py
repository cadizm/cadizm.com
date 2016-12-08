
from django.http import HttpResponse
from django.shortcuts import render


def foo(request):
    return render(request, "index.html")
