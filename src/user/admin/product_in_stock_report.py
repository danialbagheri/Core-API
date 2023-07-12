from django.contrib import admin

from user.models import ProductInStockReport


@admin.register(ProductInStockReport)
class ProductInStockReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'variant_name',
        'email',
        'email_sent',
    )
    list_filter = ('email_sent',)
    search_fields = ('email', 'variant__product__title')

    def variant_name(self, product_in_stock_report: ProductInStockReport):
        variant = product_in_stock_report.variant
        product = variant.product
        return f'{product.name} {variant.name}'

    variant_name.short_description = 'Variant Name'
