from django.contrib import admin

from web.models import SearchQuery


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('text', 'count')
    ordering = ('count',)
    search_fields = ('text',)
