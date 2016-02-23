from django.db.transaction import atomic
from screen.wall.stream import research
from logging import getLogger
from django_rq import job


@job
def event_research(event_id):
    from screen.wall.models import Event, StreamUser, StreamItem, Search

    logger = getLogger('screen.wall')
    for search in Search.objects.filter(event_id=event_id):
        for provider, items in research(search.term, search.favourites_only):
            logger.debug(
                'Looking for new %s %s with search term "%s"' % (
                    search.favourites_only and 'favourites' or 'items',
                    provider, search.term
                )
            )

            with atomic():
                for item in items:
                    try:
                        saved_user = StreamUser.objects.get(
                            provider=provider,
                            remote_id=item['user']['remote_id']
                        )
                    except StreamUser.DoesNotExist:
                        saved_user = StreamUser(
                            provider=provider
                        )

                    for key, value in item['user'].items():
                        setattr(saved_user, key, value)

                    saved_user.save()
                    item['user'] = saved_user

                    try:
                        saved_item = search.event.stream.get(
                            provider=provider,
                            remote_id=item['remote_id']
                        )
                    except StreamItem.DoesNotExist:
                        saved_item = StreamItem(
                            provider=provider,
                            event=search.event
                        )

                    for key, value in item.items():
                        setattr(saved_item, key, value)

                    if not saved_item.pk:
                        logger.debug(provider, saved_item.remote_id)

                    saved_item.save()
