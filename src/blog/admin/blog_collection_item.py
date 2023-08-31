from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from blog.models import BlogCollectionItem


@admin.register(BlogCollectionItem)
class BlogCollectionItemAdmin(OrderedModelAdmin):
    list_display = ('item', 'collection_name', 'move_up_down_links')
