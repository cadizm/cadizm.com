
from django.conf.urls import url

import cadizm.bookmarks.views
from cadizm.theta360.views import Theta360View


urlpatterns = [
    url(r'^bookmarks/$', cadizm.bookmarks.views.bookmarks),
    url(r'^bookmarks/ws/items_within_bounds$', cadizm.bookmarks.views.items_within_bounds),
    url(r'^bookmarks/ws/items_along_polyline$', cadizm.bookmarks.views.items_along_polyline),

    url(r'^360/$', Theta360View.as_view(), name='theta360'),
]
