from django.db import models


class Order(models.Model):
    FINANCIAL_STATUS_PAID = 'paid'
    FINANCIAL_STATUS_PARTIALLY_REFUNDED = 'partially_refunded'
    FINANCIAL_STATUS_REFUNDED = 'refunded'
    FINANCIAL_STATUS_CHOICES = (
        (FINANCIAL_STATUS_PAID, 'Paid'),
        (FINANCIAL_STATUS_PARTIALLY_REFUNDED, 'Partially Refunded'),
        (FINANCIAL_STATUS_REFUNDED, 'Refunded'),
    )

    created_at = models.DateTimeField()

    updated_at = models.DateTimeField()

    shopify_graphql_id = models.CharField(
        max_length=64,
        db_index=True,
    )

    order_name = models.CharField(
        max_length=32,
    )

    financial_status = models.CharField(
        max_length=32,
        choices=FINANCIAL_STATUS_CHOICES,
    )

    subtotal_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    total_discounts = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    total_line_items_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    total_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
