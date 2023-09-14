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


class AmazonReviewReminderBoughtVariant(models.Model):
    review_reminder = models.ForeignKey(
        to=AmazonReviewReminder,
        on_delete=models.CASCADE,
        db_column='amazonreviewreminder_id',
    )

    variant = models.ForeignKey(
        to=ProductVariant,
        on_delete=models.CASCADE,
        db_column='productvariant_id',
    )

    quantity = models.IntegerField()

    class Meta:
        unique_together = ('review_reminder', 'variant')
