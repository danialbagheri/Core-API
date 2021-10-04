from django.contrib import admin

from product.models import ProductVariant


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_filter = ('product',)
    list_display = [
        "sku",
        "product",
        "name",
        "size",
    ]
    search_fields = ('sku', )
