from django.db import models

from product.models import Ingredient, ProductVariant


class VariantIngredientThrough(models.Model):
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
    )

    variant = models.ForeignKey(
        to=ProductVariant,
        on_delete=models.CASCADE,
    )

    priority = models.PositiveIntegerField()
