
from django.conf.urls import url

import cadizm.bookmarks.views


urlpatterns = [
    url(r'^bookmarks/$', cadizm.bookmarks.views.bookmarks),
    url(r'^bookmarks/ws/items_within_bounds$', cadizm.bookmarks.views.items_within_bounds),
    url(r'^bookmarks/ws/items_along_polyline$', cadizm.bookmarks.views.items_along_polyline),
]
