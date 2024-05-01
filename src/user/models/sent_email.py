from django.db import models


class SentEmail(models.Model):
    TEMPLATE_IN_STOCK = 'in-stock'
    TEMPLATE_REVIEW_REMINDER = 'review-reminder'
    TEMPLATE_REVIEW_APPROVAL = 'review-approval'
    TEMPLATE_REVIEW_REPLY = 'review-reply'
    TEMPLATE_SURVEY_RESULTS = 'survey-results'
    TEMPLATE_CHOICES = (
        (TEMPLATE_IN_STOCK, 'In Stock'),
        (TEMPLATE_REVIEW_REMINDER, 'Review Reminder'),
        (TEMPLATE_REVIEW_APPROVAL, 'Review Approval'),
        (TEMPLATE_REVIEW_REPLY, 'Review Reply'),
        (TEMPLATE_SURVEY_RESULTS, 'Survey Results'),
    )

    email = models.EmailField()

    template_name = models.CharField(
        max_length=128,
        choices=TEMPLATE_CHOICES,
    )

    sent_date = models.DateTimeField(
        auto_now_add=True,
    )

    email_id = models.BigIntegerField(
        null=True,
        blank=True,
    )

    data = models.TextField(
        null=True,
    )

    class Meta:
        ordering = ('-sent_date',)
