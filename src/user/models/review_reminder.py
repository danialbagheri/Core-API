from django.db import models

from product.models import ProductVariant


class ReviewReminder(models.Model):
    order_id = models.BigIntegerField(
        db_index=True,
        unique=True,
    )

    email = models.EmailField(
        max_length=256,
    )

    bought_variants = models.ManyToManyField(
        to=ProductVariant,
    )

    reminder_date = models.DateTimeField()

    email_sent = models.BooleanField(
        default=False,
    )


class ReviewReminderBoughtVariant(models.Model):
    review_reminder = models.ForeignKey(
        to=ReviewReminder,
        on_delete=models.CASCADE,
        db_column='reviewreminder_id',
    )

    variant = models.ForeignKey(
        to=ProductVariant,
        on_delete=models.CASCADE,
        db_column='productvariant_id',
    )

    quantity = models.IntegerField()

    class Meta:
        unique_together = ('review_reminder', 'variant')
