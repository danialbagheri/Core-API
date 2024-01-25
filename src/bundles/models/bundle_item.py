from django.db import models

from bundles.models import Bundle
from product.models import Product, ProductVariant


class BundleItem(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    bundle = models.ForeignKey(
        to=Bundle,
        on_delete=models.CASCADE,
        related_name='items',
    )

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='bundle_items',
    )

    quantity = models.PositiveIntegerField()

    excluded_variants = models.ManyToManyField(
        to=ProductVariant,
        related_name='excluded_bundle_items',
    )

    position = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return f'{self.product.name} of bundle {self.bundle.name}'
