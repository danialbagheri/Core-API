from django.db import models

from product.models import ProductVariant
from user.models import AbandonedCheckout


class CheckoutItem(models.Model):
    checkout = models.ForeignKey(
        to=AbandonedCheckout,
        on_delete=models.CASCADE,
        related_name='items',
    )

    variant = models.ForeignKey(
        to=ProductVariant,
        on_delete=models.CASCADE,
        related_name='checkout_items',
    )

    quantity = models.IntegerField()

    price = models.FloatField()
