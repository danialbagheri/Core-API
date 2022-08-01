from django.contrib import admin

from review.models import ReviewImage


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_review_title']
    search_fields = ('review__title',)
    readonly_fields = ('review',)

    def get_review_title(self, review_image: ReviewImage):
        return review_image.review.title

    get_review_title.short_description = 'Review Title'
