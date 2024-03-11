from django.contrib import admin

from product.models import ProductImage


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    readonly_fields = ('image_preview',)
    list_display = (
        'variant',
        'image_preview',
        'main',
        'image_type',
        'image_angle',
        'is_public',
        'alternate_text',
    )
    search_fields = ('variant__sku', 'variant__name')
    raw_id_fields = ('variant',)
    ordering = ('-updated',)
