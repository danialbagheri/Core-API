from django.contrib import admin
from django.utils.safestring import mark_safe

from review.models import ReviewImage


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_review_title', 'image_preview')
    fields = ('image', 'image_preview', 'review')
    readonly_fields = ('review', 'image_preview')
    search_fields = ('review__title',)

    def get_review_title(self, review_image: ReviewImage):
        return review_image.review.title if review_image.review else None

    get_review_title.short_description = 'Review Title'

    def image_preview(self, review_image: ReviewImage):
        image = review_image.image
        if image:
            return mark_safe('<img src="{}" width="100" />'.format(image.url))
        return '-'

    image_preview.short_description = 'Image Preview'
