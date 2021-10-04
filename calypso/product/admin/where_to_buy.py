from django.contrib import admin

from product.models import WhereToBuy


@admin.register(WhereToBuy)
class WhereToBuyAdmin(admin.ModelAdmin):
    list_display = (
        'variant',
        'stockist',
        'url',
    )
    search_fields = ('variant__sku', 'variant__name', 'stockist__name')
    list_filter = ('stockist',)
