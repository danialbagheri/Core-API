from django.contrib import admin

from review.models import ReviewImage


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    readonly_fields = ('review',)
