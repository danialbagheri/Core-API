from django.contrib import admin

from calypso.common.admin_mixins import ExportableAdminMixin
from product.models import ProductVariant


@admin.register(ProductVariant)
class ProductVariantAdmin(ExportableAdminMixin,
                          admin.ModelAdmin):
    list_filter = ('product',)
    list_display = [
        'sku',
        'product',
        'name',
        'size',
    ]
    search_fields = ('sku', )
    save_as = True
