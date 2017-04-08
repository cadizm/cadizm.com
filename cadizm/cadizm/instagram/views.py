
from urllib import urlencode

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView


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

    def get_context_data(self, *args, **kwargs):
        context = super(GetTokenView, self).get_context_data(*args, **kwargs)
        return context
