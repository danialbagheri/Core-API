from django.contrib import admin

from product.models import ReviewQuestion, QuestionChoice


class QuestionChoiceInlineAdmin(admin.StackedInline):
    model = QuestionChoice
    extra = 0


@admin.register(ReviewQuestion)
class ReviewQuestionAdmin(admin.ModelAdmin):
    inlines = (QuestionChoiceInlineAdmin,)

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js',
            'product/js/review_question.js',
        )
