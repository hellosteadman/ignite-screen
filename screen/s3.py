from django.contrib.staticfiles.storage import CachedFilesMixin, \
    ManifestFilesMixin

from django.utils.deconstruct import deconstructible
from storages.backends.s3boto import S3BotoStorage
import urlparse
import urllib


class MediaRootS3BotoStorage(S3BotoStorage):
    location = 'media'

    def url(self, name, *args, **kw):
        s = super(MediaRootS3BotoStorage, self).url(name, *args, **kw)
        if isinstance(s, unicode):
            s = s.encode('utf-8', 'ignore')

        scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
        path = urllib.quote(path, '/%')

        if name.endswith('/') and not path.endswith('/'):
            path += '/'

        return urlparse.urlunsplit(
            (scheme, netloc, path, '', '')
        )


class StaticRootS3BotoStorage(CachedFilesMixin, S3BotoStorage):
    location = 'static'

    def url(self, name, *args, **kw):
        s = super(StaticRootS3BotoStorage, self).url(name, **kw)
        if isinstance(s, unicode):
            s = s.encode('utf-8', 'ignore')

        scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
        path = urllib.quote(path, '/%')

        if name.endswith('/') and not path.endswith('/'):
            path += '/'

        return urlparse.urlunsplit(
            (scheme, netloc, path, '', '')
        )


@deconstructible
class StoreAssetRootS3BotoStorage(S3BotoStorage):
    location = 'store'

    def url(self, name, *args, **kw):
        s = super(MediaRootS3BotoStorage, self).url(name, *args, **kw)
        if isinstance(s, unicode):
            s = s.encode('utf-8', 'ignore')

        scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
        path = urllib.quote(path, '/%')

        if name.endswith('/') and not path.endswith('/'):
            path += '/'

        return urlparse.urlunsplit(
            (scheme, netloc, path, '', '')
        )
