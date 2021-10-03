from django.db import models

from product.models import Product


class ReviewQuestion(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='questions',
    )

    text = models.TextField()
