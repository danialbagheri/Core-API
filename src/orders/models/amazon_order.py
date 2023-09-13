from django.db import models


class AmazonOrder(models.Model):
    purchase_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    amazon_order_id = models.CharField(
        max_length=128
    )

    sellerId = models.CharField(
        max_length=128,
    )

    order_status = models.CharField(
        max_length=128,
    )

    fulfillment_type = models.CharField(
        max_length=128,
    )

    order_type = models.CharField(
        max_length=128,
    )
