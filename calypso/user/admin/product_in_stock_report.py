from django.contrib import admin

from user.models import ProductInStockReport


@admin.register(ProductInStockReport)
class ProductInStockReportAdmin(admin.ModelAdmin):
    pass
