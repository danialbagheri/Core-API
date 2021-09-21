from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


class ReviewAdmin(admin.ModelAdmin):

    # filter_horizontal = ('tags', 'product_types')
    # summernote_fields = ('__all__')
    list_filter = ('score', 'approved','product',)
    list_display = [
        "name",
        "title",
        "score",
        'location',
        'product',
        "like",
        "dislike",
        'approved',
        'date_created',
    ]
    search_fields = ['customer_name']


admin.site.register(Review, ReviewAdmin)
admin.site.register(Reply)
