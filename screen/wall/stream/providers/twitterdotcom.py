from django.conf import settings
from screen.wall.stream.providers import ProviderBase
from twitter import Api


class TwitterProvider(ProviderBase):
    template_name = 'wall/stream/tweet.inc.html'
    verbose_name = 'Twitter'

    def __init__(self):
        self.api = Api(
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token_key=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_SECRET
        )

    def fetch(self, **kwargs):
        options = {
            'count': 100
        }

        if 'latest_id' in kwargs:
            options['since_id'] = kwargs.pop('latest_id')

        if 'term' in kwargs:
            options['term'] = kwargs.pop('term')

        favourites_only = kwargs.pop('favourites_only', False)
        for arg in kwargs.keys():
            raise Exception('Unrecognised option %s' % arg)

        for tweet in self.api.GetSearch(**options):
            image = None
            for media in tweet.media:
                if media['type'] == 'photo':
                    image = media['media_url_https']
                    break

            yield self.item(
                remote_id=tweet.id,
                timestamp=tweet.created_at_in_seconds,
                image=self.image(image, tweet.id),
                text=tweet.text,
                url='https://twitter.com/%s/status/%s' % (
                    tweet.user.id,
                    tweet.id
                ),
                user=self.user(
                    remote_id=tweet.user.id,
                    username=tweet.user.screen_name,
                    display_name=tweet.user.name,
                    avatar=self.image(
                        tweet.user.profile_image_url,
                        tweet.user.id
                    ),
                    url=tweet.user.url or 'https://twitter.com/%s' % (
                        tweet.user.screen_name
                    )
                )
            )
