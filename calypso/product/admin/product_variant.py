from django.contrib import admin

from calypso.common.admin_mixins import ExportableAdminMixin
from product.models import ProductVariant


@admin.register(ProductVariant)
class ProductVariantAdmin(ExportableAdminMixin,
                          admin.ModelAdmin):
    list_filter = ('is_public', 'product',)
    list_display = [
        'sku',
        'product',
        'name',
        'size',
        'is_public',
    ]
    filter_horizontal = ('ingredients',)
    search_fields = ('sku', )
    ordering = ('-date_last_modified',)
    save_as = True
