from django.db import models


class AmazonOrderItem(models.Model):
    amazon_order_item_id = models.CharField(
        max_length=128,
    )

    sku = models.CharField(
        max_length=128,
    )

    order_item_status = models.CharField(
        max_length=128,
        blank=True,
    )

    quantity = models.IntegerField()

    is_buyer_requested_cancel = models.NullBooleanField(
        null=True,
        blank=True,
    )
