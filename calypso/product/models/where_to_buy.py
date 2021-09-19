from django.db import models

from product.models import ProductVariant, Stockist


class WhereToBuy(models.Model):
    variant = models.ForeignKey(
        to=ProductVariant,
        null=True,
        on_delete=models.CASCADE,
        related_name='wheretobuy',
    )

    stockist = models.ForeignKey(
        to=Stockist,
        null=True,
        on_delete=models.CASCADE,
    )

    url = models.CharField(
        max_length=250,
        null=True,
        blank=True,
    )
