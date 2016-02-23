from bambu_pages.models import Page
from django.conf import settings

def pages(request):
    return {
        'root_pages': Page.objects.filter(parent__isnull = True),
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID
    }
