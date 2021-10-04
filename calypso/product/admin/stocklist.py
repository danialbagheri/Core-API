from django.contrib import admin

from product.models import Stockist


@admin.register(Stockist)
class StockistAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = (
        'name',
        'logo',
    )
