
import logging

from django.contrib.gis.geos import Polygon
from django.contrib.gis.geos import LineString

from cadizm.bookmarks.models import Bookmark
from cadizm.bookmarks.ws.util import decode_gpolyline, m2dd


logger = logging.getLogger(__name__)


def items_within(boundingBox):
    try:
        # (xmin, ymin, xmax, ymax)
        bb = (boundingBox['lng_lo'], boundingBox['lat_lo'],
              boundingBox['lng_hi'], boundingBox['lat_hi'])
        geom = Polygon.from_bbox(bb)
        geom.set_srid(4326)
        return Bookmark.objects.filter(geom__within=geom)
    except:
        logger.exception('geo.items_within')


def items_along(polyline, distance_meters):
    try:
        linestring = LineString(decode_gpolyline(polyline))
        dd = m2dd(distance_meters)
        return Bookmark.objects.filter(geom__dwithin=(linestring, dd))
    except:
        logger.exception('geo.items_along')
