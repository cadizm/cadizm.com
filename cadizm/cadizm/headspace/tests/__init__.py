
import json

from django.test import TestCase, Client


class BaseTestCase(TestCase):

    def setUp(self, *args, **kwargs):
        self.client = Client()
        super(BaseTestCase, self).setUp(*args, **kwargs)

    def post(self, url, data=None):
        return self.client.post(url, data=json.dumps(data) if data else None, content_type='application/json')
