from importlib import import_module

PROVIDERS = (
    'screen.wall.stream.providers.instagramdotcom.InstagramProvider',
    'screen.wall.stream.providers.twitterdotcom.TwitterProvider'
)


def research(search_term, favourites_only=False):
    for provider in PROVIDERS:
        module, klass = provider.rsplit('.', 1)
        module = import_module(module)
        klass = getattr(module, klass)

        yield provider, klass().fetch(
            term=search_term,
            favourites_only=favourites_only
        )
