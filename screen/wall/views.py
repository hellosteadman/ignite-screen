from datetime import datetime
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.timezone import now, utc
from screen.wall.models import Event
from django.views.decorators.cache import cache_page


@atomic
@cache_page(5)
def stream(request, slug):
    event = get_object_or_404(Event, slug=slug)

    if event.searches.exists():
        if not event.stream_updated:
            event.research()
        elif (now() - event.stream_updated).total_seconds > 60:
            event.research()

    items = event.stream.all()
    if 'since' in request.GET:
        items = items.filter(
            date__gte=datetime.utcfromtimestamp(
                int(request.GET['since'])
            ).replace(
                tzinfo=utc
            )
        )
    else:
        items = items[:20]

    if request.is_ajax():
        templates = (
            'wall/stream.inc.html',
            'wall/events/%s/stream.inc.html' % event.slug
        )
    else:
        templates = (
            'wall/stream.html',
            'wall/events/%s/stream.html' % event.slug
        )

    return TemplateResponse(
        request,
        templates,
        {
            'event': event,
            'stream': reversed(list(items))
        }
    )
