from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from common.admin_mixins import ExportableAdminMixin
from product.models import Product, ProductImage
from .actions import make_public


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
    filter_horizontal = ('keyword', 'tags', 'types')
    search_fields = ['name']
    ordering = ('-updated',)
    actions = (make_public,)
    inlines = (ReviewQuestionInlineAdmin,)
    save_as = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name not in ['main_image', 'secondary_image']:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        product_id = request.resolver_match.kwargs['object_id']
        kwargs['queryset'] = ProductImage.objects.filter(variant__product_id=product_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
