
from django.conf.urls import url

import cadizm.foo.views


urlpatterns = [
    url(r'^foo/', cadizm.foo.views.foo),
]
