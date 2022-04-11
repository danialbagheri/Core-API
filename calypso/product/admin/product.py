from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from calypso.common.admin_mixins import ExportableAdminMixin
from product.models import Product


class ReviewQuestionInlineAdmin(admin.StackedInline):
    model = Product.questions.through
    extra = 0


@admin.register(Product)
class ProductAdmin(ExportableAdminMixin,
                   SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_filter = ('types', 'is_public')
    list_display = [
        'name',
        'slug',
        'is_public',
    ]
    export_fields = (
        'slug', 'name',  'sub_title', 'description', 'direction_of_use', 'variant_sku_list', 'lowest_variant_price',
        'get_total_review_count', 'get_review_average_score', 'keywords_str', 'tags_str', 'types_str',
    )
    filter_vertical = ('keyword', 'tags', 'types')
    search_fields = ['name']
    inlines = (ReviewQuestionInlineAdmin,)
    save_as = True
