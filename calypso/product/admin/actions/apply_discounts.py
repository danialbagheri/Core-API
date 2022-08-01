from django import forms
from django.contrib import messages
from django.shortcuts import render

from product.services import DiscountApplierService


class DiscountForm(forms.Form):
    discount_percentage = forms.FloatField(
        min_value=0,
        max_value=100,
        label='Discount Percentage',
    )


def apply_discounts(modeladmin, request, queryset):
    if 'do_action' not in request.POST:
        form = DiscountForm()
        return render(
            request=request,
            template_name='admin/product/apply_discounts.html',
            context={
                'title': 'Choose discount percentage',
                'objects': queryset,
                'form': form
            }
        )
    form = DiscountForm(request.POST)
    form.is_valid()
    discount_percentage = form.cleaned_data['discount_percentage']
    if not discount_percentage or discount_percentage > 100 or discount_percentage < 0:
        modeladmin.message_user(
            message='Invalid discount percentage.',
            request=request,
            level=messages.ERROR,
        )

    discount_applier = DiscountApplierService(queryset, discount_percentage)
    discount_applier.apply_discounts()
    variants_failed_to_alter = discount_applier.variants_failed_to_alter
    for variant in variants_failed_to_alter:
        modeladmin.message_user(
            message=f'Failed to alter price of the variant {variant.sku}',
            request=request,
            level=messages.ERROR,
        )
