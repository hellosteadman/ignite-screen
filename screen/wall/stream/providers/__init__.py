from dateutil import parser
from django.core.files import File
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from os import path, write, close
from tempfile import mkstemp
from urlparse import urlsplit
from datetime import datetime
from pytz import utc
import requests


class ProviderBase(object):
    template_name = 'wall/stream/item.inc.html'
    verbose_name = 'Provider'

    def fetch(self, **kwargs):
        raise NotImplementedError('Method not implemented.')

    def item(self, **kwargs):
        if 'date' in kwargs:
            if isinstance(kwargs['date'], (str, unicode)):
                parsed_date = parser.parse(kwargs['date'])
            else:
                parsed_date = kwargs['date']
        elif 'timestamp' in kwargs:
            parsed_date = datetime.utcfromtimestamp(
                kwargs['timestamp']
            ).replace(
                tzinfo=utc
            )
        else:
            raise Exception('Either specify date string, or Unix timestamp')

        return {
            'date': parsed_date,
            'text': kwargs.get('text'),
            'image': kwargs.get('image'),
            'remote_id': kwargs.get('remote_id'),
            'url': kwargs.get('url'),
            'user': kwargs.get('user')
        }

    def user(self, **kwargs):
        return {
            'remote_id': kwargs.get('remote_id'),
            'username': kwargs.get('username'),
            'display_name': kwargs.get('display_name'),
            'avatar': kwargs.get('avatar'),
            'url': kwargs.get('url')
        }

    def image(self, url, name):
        if not url:
            return None

        scheme, netloc, imgpath, qs, anchor = urlsplit(url)
        imgname = path.split(imgpath)[-1]
        imgname, imgext = path.splitext(imgname)
        response = requests.get(url)

        if response.status_code == 200:
            handle, filename = mkstemp(imgext)
            write(handle, response.content)
            close(handle)

            return File(
                open(filename, 'rb'),
                name='%s%s' % (name, imgext)
            )
        else:
            raise Exception(response.status_code)

    def render(self, item):
        return render_to_string(
            self.template_name,
            {
                'remote_id': item.remote_id,
                'date': item.date,
                'text': item.text,
                'image': item.image,
                'url': item.url,
                'user': {
                    'remote_id': item.user.remote_id,
                    'username': item.user.username,
                    'display_name': item.user.display_name,
                    'url': item.user.url,
                    'avatar': item.user.avatar
                }
            }
        )
