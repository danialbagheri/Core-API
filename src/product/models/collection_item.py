from django.db import models
from ordered_model.models import OrderedModel

from product.models import Product, Collection


class CollectionItem(OrderedModel):
    item = models.ForeignKey(
        to=Product,
        blank=True,
        related_name="collected_items",
        on_delete=models.CASCADE
    )

    collection_name = models.ForeignKey(
        to=Collection,
        blank=True,
        related_name="collection_items",
        on_delete=models.CASCADE
    )

    order_with_respect_to = 'collection_name'

    class Meta:
        index_together = ('item', 'order')
        ordering = ['order']

    def __str__(self):
        return f"{self.item.name}"
