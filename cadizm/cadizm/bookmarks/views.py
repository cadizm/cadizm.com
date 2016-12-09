
from django.conf import settings
from django.core import serializers
#from django.core.context_processors import csrf
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_list_or_404
from django.views.decorators.csrf import ensure_csrf_cookie



import datetime
import httplib
import json
import logging
import random
import traceback
import urllib

from cadizm.bookmarks.ws import geo


logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("INDEX")


@ensure_csrf_cookie
def bookmarks(request):
    context = {
        'API_KEY': settings.GOOGLE_API_KEY,
    }
#    context.update(csrf(request))
    return render(request, 'index.html', context)


def items_within_bounds(request):
    boundingBox, res = None, {'status': 0}
    try:
        boundingBox = json.loads(request.GET['boundingBox'])
    except:
        logger.error('Invalid JSON: {0}'.format(request.GET['boundingBox']))
    items = geo.items_within(boundingBox)
    res['status'] = 1
    res['items'] = serializers.serialize('json', items)
    return HttpResponse(json.dumps(res), content_type='application/json')


def items_along_polyline(request):
    encodedPolyline, res = None, {'status': 0}
    try:
        encodedPolyline = request.GET['polyline']
        distance_meters = int(request.GET.get('distance_meters', 100))
        items = geo.items_along(encodedPolyline, distance_meters)
        res['status'] = 1
        res['items'] = serializers.serialize('json', items)
        return HttpResponse(json.dumps(res), content_type='application/json')
    except:
        logger.exception('views.items_along_polyline')
        res['status'] = 0
        res['message'] = 'Unable to process requrest'
        return HttpResponse(json.dumps(res), content_type='application/json')
