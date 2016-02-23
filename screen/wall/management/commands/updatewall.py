from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic
from logging import getLogger
from screen.wall.models import Search, StreamUser, StreamItem
from screen.wall.tasks import research


class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **options):
        from screen.wall.models import Event

        logger = getLogger('screen.wall')
        for search in Search.objects.all():
            for prov, items in research(search.term, search.favourites_only):
                logger.debug(
                    'Looking for new %s %s with search term "%s"' % (
                        search.favourites_only and 'favourites' or 'items',
                        prov, search.term
                    )
                )

                with atomic():
                    for item in items:
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
