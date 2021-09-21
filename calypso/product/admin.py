from django.contrib import admin
from rest_framework.fields import ReadOnlyField
from .models import *
from django_summernote.admin import SummernoteModelAdmin
from ordered_model.admin import OrderedTabularInline, OrderedStackedInline, OrderedInlineModelAdminMixin, OrderedModelAdmin
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
    save_as = True

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
    save_as = True

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
    save_as = True


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
    list_filter = ["stockist",]
    actions = ['check_urls']
    save_as = True

    def check_urls(self, request, queryset):
        for obj in queryset:
            print(obj.url)
        pass

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
