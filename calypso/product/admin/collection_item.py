from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from product.models import CollectionItem


@admin.register(CollectionItem)
class CollectionItemAdmin(OrderedModelAdmin):
    list_display = (
        'item',
        'collection_name',
        'move_up_down_links',
    )
    save_as = True
