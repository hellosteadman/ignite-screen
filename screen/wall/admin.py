from django.contrib import admin
from screen.wall.models import Event, Search


class SearchInline(admin.TabularInline):
    model = Search
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    inlines = [SearchInline]

    prepopulated_fields = {
        'slug': ('name',)
    }
