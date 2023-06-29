from django.contrib import admin

from user.models import VariantImageRequest


@admin.register(VariantImageRequest)
class VariantImageRequestAdmin(admin.ModelAdmin):
    pass
