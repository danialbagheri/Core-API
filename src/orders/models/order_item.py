from django.db import models

from orders.models import Order


class OrderItem(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='items',
    )

    shopify_graphql_id = models.CharField(
        max_length=64,
        db_index=True,
    )

    product_id = models.BigIntegerField(
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=512,
        blank=True,
    )

    variant_id = models.BigIntegerField(
        null=True,
        blank=True,
    )

    sku = models.CharField(
        max_length=128,
        blank=True,
    )

    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    total_discount = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    quantity = models.PositiveSmallIntegerField()
