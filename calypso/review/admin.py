from django.contrib import admin

from .models import *


class ReviewAdmin(admin.ModelAdmin):

    # filter_horizontal = ('tags', 'product_types')
    # summernote_fields = ('__all__')
    list_filter = ('score', 'product')
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
    search_fields = ['name']


admin.site.register(Review, ReviewAdmin)
admin.site.register(Reply)
