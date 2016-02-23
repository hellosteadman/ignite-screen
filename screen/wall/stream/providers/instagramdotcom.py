from django.conf import settings
from instagram.client import InstagramAPI
from screen.wall.stream.providers import ProviderBase
from pytz import utc
import re


class InstagramProvider(ProviderBase):
    template_name = 'wall/stream/photo.inc.html'
    verbose_name = 'Instagram'

    def __init__(self):
        self.api = InstagramAPI(
            access_token=settings.INSTAGRAM_ACCESS_TOKEN,
            client_secret=settings.INSTAGRAM_CLIENT_SECRET
        )

    def fetch(self, **kwargs):
        options = {
            'count': 100
        }

        if 'term' in kwargs:
            tags = re.findall(r'(?:#([\w]+))', kwargs.pop('term'))
        else:
            tags = []

        kwargs.pop('favourites_only', False)
        for arg in kwargs.keys():
            raise Exception('Unrecognised option %s' % arg)

        for tag in [t.strip() for t in tags if t.strip()]:
            photos, next_ = self.api.tag_recent_media(tag_name=tag, **options)

            for photo in photos:
                yield self.item(
                    remote_id=photo.id,
                    date=photo.created_time.replace(tzinfo=utc),
                    image=self.image(
                        photo.images['standard_resolution'].url,
                        photo.id
                    ),
                    text=photo.caption.text,
                    url=photo.link,
                    user=self.user(
                        remote_id=photo.user.id,
                        username=photo.user.username,
                        display_name=photo.user.full_name,
                        avatar=self.image(
                            photo.user.profile_picture,
                            photo.user.id
                        ),
                        url='https://instagram.com/%s' % photo.user.username
                    )
                )
