
from django.conf import settings

import requests


BASE_URL = 'https://slack.com/api/reminders.add'


def add(text, time, **kwargs):
    kwargs.update(text=text, time=time)
    response = requests.post(BASE_URL, headers=_headers(), json=kwargs)

    body = response.json()
    if not body['ok']:
        raise Exception(body['error'])

    return body['reminder']


def _headers():
    return {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': "Bearer %s" % settings.ROYS_SLACK_ACCESS_TOKEN,
    }
