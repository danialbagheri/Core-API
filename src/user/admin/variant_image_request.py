import ast

from django.contrib import admin

from user.models import VariantImageRequest


@admin.register(VariantImageRequest)
class VariantImageRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'sku_list_preview', 'email', 'email_sent')

    def sku_list_preview(self, variant_image_request: VariantImageRequest):
        sku_list = variant_image_request.sku_list
        sku_list = ast.literal_eval(sku_list)
        sku_list = [sku.upper() for sku in sku_list]
        if len(sku_list) <= 5:
            return ', '.join(sku_list)
        return ', '.join(sku_list) + ', ...'

    sku_list_preview.short_description = 'Requested SKUs'
