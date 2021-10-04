from django.contrib import admin

from product.models import Keyword


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    search_fields = ('name',)
