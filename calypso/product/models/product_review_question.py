from django.db import models

from . import Product


class ProductReviewQuestion(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='questions',
    )

    text = models.TextField()
