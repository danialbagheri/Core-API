from django.contrib import admin
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin

from blog.models import BlogCollection, BlogCollectionItem


class CollectionItemsThroughOrderedStackedInline(OrderedTabularInline):
    model = BlogCollectionItem
    fields = ('item', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ('order', )


@admin.register(BlogCollection)
class BlogCollectionAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    search_fields = ('name',)
    list_display = (
        'name',
        'slug',
        'collection_count',
    )
    inlines = (CollectionItemsThroughOrderedStackedInline,)

    def collection_count(self, blog_collection: BlogCollection):
        return blog_collection.blogcollectionitem.count()

    collection_count.short_description = 'Collection Count'
