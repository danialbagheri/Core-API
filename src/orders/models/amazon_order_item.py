from django.db import models

from orders.models import AmazonOrder


class AmazonOrderItem(models.Model):
    ORDER_ITEM_STATUS_UNSHIPPED = 'Unshipped'
    ORDER_ITEM_STATUS_SHIPPED = 'Shipped'
    ORDER_ITEM_STATUS_CHOICES = (
        (ORDER_ITEM_STATUS_UNSHIPPED, 'Unshipped'),
        (ORDER_ITEM_STATUS_SHIPPED, 'Shipped'),
    )

    amazon_order_item_id = models.CharField(
        max_length=128,
    )

    amazon_order = models.ForeignKey(
        to=AmazonOrder,
        on_delete=models.CASCADE,
        related_name='items',
    )

    sku = models.CharField(
        max_length=128,
    )

    order_item_status = models.CharField(
        max_length=128,
        choices=ORDER_ITEM_STATUS_CHOICES,
        blank=True,
    )

    quantity = models.IntegerField()

    is_buyer_requested_cancel = models.NullBooleanField(
        null=True,
        blank=True,
    )
