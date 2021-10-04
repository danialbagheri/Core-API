from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from product.models import ProductReviewQuestion, Product


class ReviewQuestionInlineAdmin(admin.StackedInline):
    model = ProductReviewQuestion
    extra = 0


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_filter = ('types',)
    list_display = [
        "name",
        "slug",
    ]
    search_fields = ['name']
    inlines = (ReviewQuestionInlineAdmin,)
