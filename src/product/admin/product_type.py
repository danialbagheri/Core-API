from django.contrib import admin

from product.models import ProductType


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
