from django.contrib import admin

from review.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
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
