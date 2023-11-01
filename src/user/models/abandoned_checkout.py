from django.db import models


class AbandonedCheckout(models.Model):
    created_at = models.DateTimeField()

    legacy_id = models.BigIntegerField()

    abandoned_checkout_url = models.URLField(
        max_length=512,
    )

    cart_token = models.CharField(
        max_length=128,
    )

    email = models.EmailField()

    customer_id = models.BigIntegerField(
        null=True,
        blank=True,
    )

    customer_first_name = models.CharField(
        max_length=64,
        blank=True,
    )

    customer_last_name = models.CharField(
        max_length=64,
        blank=True,
    )
