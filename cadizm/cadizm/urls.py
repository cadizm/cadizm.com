
from django.conf.urls import url

import cadizm.bookmarks.views
from cadizm.theta360.views import Theta360View
from cadizm.about.views import PrivacyView
from cadizm.instagram.views import AccessTokenView, GetTokenView
from cadizm.tees.views import (
    TeesView,
    TeeView,
    TeesCheckoutView,
    CheckoutConfirmationView,
    CheckoutErrorView,
    )


urlpatterns = [
    url(r'^bookmarks/$', cadizm.bookmarks.views.bookmarks),
    url(r'^bookmarks/ws/items_within_bounds$', cadizm.bookmarks.views.items_within_bounds),
    url(r'^bookmarks/ws/items_along_polyline$', cadizm.bookmarks.views.items_along_polyline),

    url(r'^360/$', Theta360View.as_view(), name='theta360'),
    url(r'^privacy/$', PrivacyView.as_view(), name='privacy'),

    url(r'^instagram/access-token/$', AccessTokenView.as_view(), name='access_token'),
    url(r'^instagram/get-token/$', GetTokenView.as_view(), name='get_token'),

    url(r'^tees/$', TeesView.as_view(), name='tees'),

    url(r'^tees/order/(?P<number>\w+)/$', CheckoutConfirmationView.as_view(), name='confirmation'),
    url(r'^tees/error/$', CheckoutErrorView.as_view(), name='checkout_error'),

    url(r'^tees/(?P<tee>(\w+|-*)+)/$', TeeView.as_view(), name='tee'),
    url(r'^tees/(?P<tee>(\w+|-*)+)/checkout/$', TeesCheckoutView.as_view(), name='checkout'),
]
