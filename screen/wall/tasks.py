from django.db.transaction import atomic
from django.utils.timezone import now
from screen.wall.stream import research
from logging import getLogger
from django_rq import job


@job
def event_research(event_id):
    from screen.wall.models import Event, StreamUser, StreamItem, Search

    logger = getLogger('screen.wall')
    if Event.objects.filter(pk=event_id, stream_updating=True).exists():
        logger.debug('Exiting as another job is already working')
        return

    Event.objects.filter(
        pk=event_id
    ).update(
        stream_updating=True
    )

    try:
        with atomic():
            for search in Search.objects.filter(event_id=event_id):
                for prov, its in research(search.term, search.favourites_only):
                    logger.debug(
                        'Looking for new %s %s with search term "%s"' % (
                            search.favourites_only and 'favourites' or 'items',
                            prov, search.term
                        )
                    )

                    for item in its:
                        try:
                            saved_user = StreamUser.objects.get(
                                provider=prov,
                                remote_id=item['user']['remote_id']
                            )
                        except StreamUser.DoesNotExist:
                            saved_user = StreamUser(
                                provider=prov
                            )

                        for key, value in item['user'].items():
                            setattr(saved_user, key, value)

                        saved_user.save()
                        item['user'] = saved_user

                        try:
                            saved_item = search.event.stream.get(
                                provider=prov,
                                remote_id=item['remote_id']
                            )
                        except StreamItem.DoesNotExist:
                            saved_item = StreamItem(
                                provider=prov,
                                event=search.event
                            )

                        for key, value in item.items():
                            setattr(saved_item, key, value)

                        if not saved_item.pk:
                            logger.debug(prov, saved_item.remote_id)

                        saved_item.save()
    finally:
        Event.objects.filter(
            pk=event_id
        ).update(
            stream_updated=now(),
            stream_updating=False
        )
