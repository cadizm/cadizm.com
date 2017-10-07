
import json

from django.test import TestCase, Client


class JsonClient(Client):
    def post(self, path, data=None, **kwargs):
        return super(JsonClient, self).post(path, data=json.dumps(data) if data else None, content_type='application/json', **kwargs)


class BaseTestCase(TestCase):
    def setUp(self, *args, **kwargs):
        self.client = JsonClient()
        super(BaseTestCase, self).setUp(*args, **kwargs)
