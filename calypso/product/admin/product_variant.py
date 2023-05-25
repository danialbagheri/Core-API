from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME

from common.admin_mixins import ExportableAdminMixin
from product.admin.actions import apply_discounts, remove_discounts
from product.models import ProductVariant


@admin.register(ProductVariant)
class ProductVariantAdmin(ExportableAdminMixin,
                          admin.ModelAdmin):
    list_filter = ('is_public', 'product',)
    list_display = [
        'sku',
        'product',
        'name',
        'size',
        'price',
        'compare_at_price',
        'is_public',
    ]
    filter_horizontal = ('ingredients',)
    search_fields = ('sku', )
    ordering = ('-date_last_modified',)
    actions = (apply_discounts, remove_discounts,)
    save_as = True

    def changelist_view(self, request, extra_context=None):
        if (
            'action' not in request.POST or
            request.POST['action'] not in ['apply_discounts', 'remove_discounts'] or
            request.POST.getlist(ACTION_CHECKBOX_NAME)
        ):
            return super().changelist_view(request, extra_context)

        post = request.POST.copy()
        for variant in ProductVariant.objects.all():
            post.update({ACTION_CHECKBOX_NAME: str(variant.pk)})
        request._set_post(post)
        return super().changelist_view(request, extra_context)
