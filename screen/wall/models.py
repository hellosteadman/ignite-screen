from django.db import models
from django.utils.timezone import now
from importlib import import_module
from django_rq import get_queue
from screen.wall.tasks import event_research


class Event(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=30, unique=True)
    stream_updated = models.DateTimeField(null=True, editable=False)
    stream_background = models.ImageField(
        max_length=255, null=True, blank=True,
        upload_to='events/stream'
    )

    def __unicode__(self):
        return self.name

    def research(self):
        queue = get_queue()
        a = (self.pk,)

        for job in queue.jobs:
            if not job.result and job.func == event_research:
                if tuple(job.args) == a:
                    return

        event_research.delay(self.pk)

    class Meta:
        ordering = ('slug',)


class Search(models.Model):
    event = models.ForeignKey(Event, related_name='searches')
    term = models.CharField(max_length=255)
    favourites_only = models.BooleanField(default=False)

    def __unicode__(self):
        return self.term

    class Meta:
        verbose_name_plural = 'searches'


class StreamUser(models.Model):
    provider = models.CharField(max_length=255)
    remote_id = models.CharField(max_length=255)
    username = models.CharField(max_length=30)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(
        max_length=255, null=True, blank=True,
        upload_to='events/stream/avatars'
    )

    url = models.URLField(max_length=255)

    def __unicode__(self):
        return self.display_name or self.username

    class Meta:
        unique_together = ('provider', 'remote_id')


class StreamItem(models.Model):
    event = models.ForeignKey(Event, related_name='stream')
    date = models.DateTimeField()
    provider = models.CharField(max_length=255)
    user = models.ForeignKey(StreamUser, related_name='items')
    remote_id = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(
        max_length=255, null=True, blank=True,
        upload_to='events/stream/items'
    )

    url = models.URLField(max_length=255)

    def __unicode__(self):
        return self.text

    def save(self, *args, **kwargs):
        super(StreamItem, self).save(*args, **kwargs)
        self.event.stream_updated = now()
        self.event.save(
            update_fields=('stream_updated',)
        )

    def render(self):
        module, klass = self.provider.rsplit('.', 1)
        module = import_module(module)
        klass = getattr(module, klass)
        return klass().render(self)

    class Meta:
        unique_together = ('provider', 'remote_id')
        ordering = ('-date',)
        get_latest_by = 'date'
