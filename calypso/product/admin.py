from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


class ProductAdmin(SummernoteModelAdmin):

    # filter_horizontal = ('tags', 'product_types')
    summernote_fields = ('__all__')
    list_filter = ('types',)
    list_display = [
        "name",
        "slug",
    ]
    search_fields = ['name']


class ProductVariantAdmin(admin.ModelAdmin):

    # filter_horizontal = ('tags', 'product_types')
    list_filter = ('product',)
    list_display = [
        "sku",
        "product",
        "name",
        "size",
    ]
    search_fields = ['sku', ]


class ProductImageAdmin(admin.ModelAdmin):

    readonly_fields = ["image_preview"]
    list_display = [
        "variant",
        "image_preview",
        "image_type",
        "image_angle",
        "alternate_text",
    ]
    search_fields = ['variant__sku', 'variant__name']


admin.site.register(Product, ProductAdmin)
admin.site.register(Tag)
admin.site.register(ProductType)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Stockist)
admin.site.register(WhereToBuy)
admin.site.register(Ingredient)
