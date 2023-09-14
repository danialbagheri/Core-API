from django.db import models

from orders.models import AmazonOrder
from product.models import ProductVariant


class AmazonReviewReminder(models.Model):
    amazon_order = models.ForeignKey(
        to=AmazonOrder,
        on_delete=models.CASCADE,
        related_name='review_reminders',
    )

    bought_variants = models.ManyToManyField(
        to=ProductVariant,
        through='orders.AmazonReviewReminderBoughtVariant',
    )

    reminder_date = models.DateTimeField()

    email_sent = models.BooleanField(
        default=False,
    )
