from django.contrib import admin
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin

from product.models import CollectionItem, Collection


class CollectionItemsThroughOrderedStackedInline(OrderedTabularInline):
    model = CollectionItem
    fields = ('item', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order', )


@admin.register(Collection)
class CollectionAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    search_fields = ('name',)
    list_display = [
        'name',
        'slug',
        'collection_count',
    ]
    inlines = (CollectionItemsThroughOrderedStackedInline,)

    @staticmethod
    def collection_count(collection: Collection):
        return collection.collection_items.count()
