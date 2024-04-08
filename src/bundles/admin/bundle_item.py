from django.contrib import admin

from bundles.models import BundleItem
from product.models import ProductVariant


@admin.register(BundleItem)
class BundleItemAdmin(admin.ModelAdmin):
    fields = ('bundle', 'product', 'quantity', 'variants')
    readonly_fields = ('bundle', 'product')
    list_display = ('bundle', 'product', 'quantity')
    list_filter = ('bundle',)
    search_fields = ('bundle__name', 'product__name')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if 'variants' not in db_field.name:
            return super().formfield_for_manytomany(db_field, request, **kwargs)

        bundle_item_id = request.resolver_match.kwargs['object_id']
        product_id = BundleItem.objects.get(id=bundle_item_id).product_id
        kwargs['queryset'] = ProductVariant.objects.filter(product_id=product_id)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
