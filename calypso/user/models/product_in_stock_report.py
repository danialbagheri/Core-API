from django.db import models

from product.models import ProductVariant


class ProductInStockReport(models.Model):
    variant = models.ForeignKey(
        to=ProductVariant,
        on_delete=models.CASCADE,
        related_name='in_stock_reports',
    )

    email = models.EmailField(
        max_length=256,
    )

    email_sent = models.BooleanField(
        default=False,
        db_index=True,
    )
