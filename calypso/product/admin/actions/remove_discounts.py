from django.contrib import messages

from product.services import DiscountApplierService


def remove_discounts(modeladmin, request, queryset):
    discount_applier = DiscountApplierService(queryset, 0)
    discount_applier.apply_discounts()
    variants_failed_to_alter = discount_applier.variants_failed_to_alter
    for variant in variants_failed_to_alter:
        modeladmin.message_user(
            message=f'Failed to remove the discount of variant {variant.sku}',
            request=request,
            level=messages.ERROR,
        )
