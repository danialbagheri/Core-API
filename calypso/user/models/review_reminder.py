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
