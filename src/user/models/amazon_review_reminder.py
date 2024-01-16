from django.db import models

from orders.models import AmazonOrder


class AmazonReviewReminder(models.Model):
    amazon_order = models.ForeignKey(
        to=AmazonOrder,
        on_delete=models.CASCADE,
        related_name='review_reminders',
    )

    reminder_date = models.DateTimeField()

    email_sent = models.BooleanField(
        default=False,
    )
