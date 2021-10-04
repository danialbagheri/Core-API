from django.contrib import admin

from product.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    ReadOnlyField = ('slug',)
    search_fields = ('name',)
