from django.contrib import admin
from nested_admin.forms import SortableHiddenMixin
from nested_admin.nested import NestedModelAdmin, NestedTabularInline

from bundles.models import Bundle, BundleItem, BundleImage


class BundleItemInlineAdmin(SortableHiddenMixin,
                            NestedTabularInline):
    model = BundleItem
    fields = ('product', 'quantity', 'position')
    show_change_link = True

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return 1


class BundleImageInlineAdmin(SortableHiddenMixin,
                             NestedTabularInline):
    model = BundleImage
    fields = ('image', 'alternate_text', 'image_type', 'image_angle', 'main', 'position')
    extra = 0


@admin.register(Bundle)
class BundleAdmin(NestedModelAdmin):
    list_display = (
        'name',
        'price',
        'extra_discount_percentage',
        'is_active',
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'name',
        'product__name',
    )

    inlines = (BundleItemInlineAdmin, BundleImageInlineAdmin,)
