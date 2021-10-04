from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin, OrderedModelAdmin

from .models import *


class ReviewQuestionInlineAdmin(admin.StackedInline):
    model = ProductReviewQuestion
    extra = 0


class ProductAdmin(SummernoteModelAdmin):

    # filter_horizontal = ('tags', 'product_types')
    summernote_fields = '__all__'
    list_filter = ('types',)
    list_display = [
        "name",
        "slug",
    ]
    search_fields = ['name']
    inlines = (ReviewQuestionInlineAdmin,)


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


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = [
        "name",
        "slug",
    ]
    ReadOnlyField = ['slug']


class KeywordAdmin(admin.ModelAdmin):
    search_fields = ['name']


class ProductTypeAdmin(admin.ModelAdmin):
    search_fields = ['name']


class CollectionItemsthroughOrderedStackedInline(OrderedTabularInline):
    model = CollectionItem
    fields = ("item", "order", 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)
    extra = 1
    ordering = ("order", )


class CollectionAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    search_fields = ['name']
    list_display = [
        "name",
        "slug",
        "collection_count"
    ]
    inlines = (CollectionItemsthroughOrderedStackedInline,)

    def collection_count(self, obj, *args, **kwargs):
        return obj.collection_items.count()


class CollectionItemAdmin(OrderedModelAdmin):
    list_display = ("item", 'collection_name',
                    'move_up_down_links')


class StockistAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_display = [
        "name",
        "logo",
    ]


class WhereToBuyAdmin(admin.ModelAdmin):
    list_display = [
        "variant",
        "stockist",
        "url",
    ]
    search_fields = ['variant__sku', 'variant__name', 'stockist__name']
    list_filter = ["stockist"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Stockist,StockistAdmin)
admin.site.register(WhereToBuy, WhereToBuyAdmin)
admin.site.register(Ingredient)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionItem, CollectionItemAdmin)
