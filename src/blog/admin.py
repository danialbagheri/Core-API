from django.contrib import admin
from .models import BlogPost, BlogCollection, BlogCollectionItem
from django_summernote.admin import SummernoteModelAdmin
from ordered_model.admin import OrderedTabularInline, OrderedStackedInline, OrderedInlineModelAdminMixin, OrderedModelAdmin
# Register your models here.
class BlogPostAdmin(SummernoteModelAdmin):
    list_display = ['title', 'slug','published', 'publish_date']
    list_filter = ['category', 'tags', 'publish_date']
    search_fields = ['title', 'slug']
    summernote_fields = ['body']

class CollectionItemsthroughOrderedStackedInline(OrderedTabularInline):
    model = BlogCollectionItem
    fields = ("item", "order", 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ("order", )

class BlogCollectionAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    search_fields = ['name']
    list_display = [
        "name",
        "slug",
        "collection_count"
    ]
    inlines = (CollectionItemsthroughOrderedStackedInline,)

    def collection_count(self, obj, *args, **kwargs):
        return obj.blogcollectionitem.count()


class BlogCollectionItemAdmin(OrderedModelAdmin):
    list_display = ("item", 'collection_name',
                    'move_up_down_links')


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogCollection, BlogCollectionAdmin)
admin.site.register(BlogCollectionItem, BlogCollectionItemAdmin)