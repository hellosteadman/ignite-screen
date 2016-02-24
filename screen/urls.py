from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('screen.wall.urls'))
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.static import serve

    urlpatterns += staticfiles_urlpatterns() + [
        url(
            r'^media/(?P<path>.*)$', serve,
            {
                'document_root': settings.MEDIA_ROOT
            }
        )
    ]
