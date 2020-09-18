from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class ProductCategoryAdmin(SummernoteModelAdmin):

    # filter_horizontal = ('tags', 'product_types')
    summernote_fields = ('__all__')
    list_filter = ('types',)
    list_display = [
        "name",
        "slug",
    ]
    search_fields = ['name']


class ProductAdmin(admin.ModelAdmin):

    # filter_horizontal = ('tags', 'product_types')
    list_filter = ('product_category',)
    list_display = [
        "product_code",
        "product_category",
        "option_name",
        "option_value",
        "size",
    ]
    search_fields = ['product_code', ]

class ProductImageAdmin(admin.ModelAdmin):

    readonly_fields = ["image_preview"]
    list_display = [
        "product",
        "image_preview",
        "image_type",
        "image_angle",
        "alternate_text",
    ]
    search_fields = ['product__product_code', 'product__option_value']

admin.site.register(ProductCategory,ProductCategoryAdmin)
admin.site.register(Tag)
admin.site.register(ProductType)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Stockist)
admin.site.register(WhereToBuy)
admin.site.register(Ingredient)