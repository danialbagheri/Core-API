from django.contrib import admin

from review.models import Review, ReviewAnswer, ReviewImage


class ReviewAnswerInlineAdmin(admin.StackedInline):
    model = ReviewAnswer
    fields = (
        'question_text',
        'text',
    )
    readonly_fields = (
        'question_text',
        'text',
    )

    @staticmethod
    def question_text(review_answer: ReviewAnswer):
        return review_answer.question.text

    question_text.short_description = 'Question Text'

    def has_add_permission(self, request, obj):
        return False


class ReviewImageInlineAdmin(admin.StackedInline):
    model = ReviewImage
    fields = ('image',)
    readonly_fields = ('image',)

    def has_add_permission(self, request, obj):
        return False


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
    search_fields = ['customer_name']
    inlines = (ReviewAnswerInlineAdmin, ReviewImageInlineAdmin)
