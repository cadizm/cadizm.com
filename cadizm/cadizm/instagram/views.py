
from urllib import urlencode

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView

import requests


import logging
logger = logging.getLogger(__name__)


class AccessTokenView(TemplateView):
    instagram_authorize_uri = 'https://api.instagram.com/oauth/authorize'

    def dispatch(self, *args, **kwargs):
        params = dict(
            client_id=settings.FCKCO_CLIENT_ID,
            redirect_uri='https://%s%s' % (settings.HOST_NAME, reverse('get_token')),
            response_type='code',
            )
        url = '%s/?%s' % (self.instagram_authorize_uri, urlencode(params))
        return HttpResponseRedirect(url)


class GetTokenView(TemplateView):
    template_name = 'get_token.html'

    instagram_access_token_uri = 'https://api.instagram.com/oauth/access_token'

    def get_context_data(self, *args, **kwargs):
        context = super(GetTokenView, self).get_context_data(*args, **kwargs)

        payload = dict(
            client_id=settings.FCKCO_CLIENT_ID,
            client_secret=settings.FCKCO_CLIENT_SECRET,
            grant_type='authorization_code',
            redirect_uri='https://%s%s' % (settings.HOST_NAME, reverse('get_token')),
            code=self.request.GET['code'],
            )

        response = requests.post(self.instagram_access_token_uri, data=payload)

        logger.info("Requesting access_token: %s" % response.url)

        if response.ok:
            data = response.json()
            context.update(token=data['access_token'])
        else:
            error = '%s %s' % (response.status_code, response.content)
            logger.error(error)
            context.update(error=error)

        return context
