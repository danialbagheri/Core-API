from django.db import models
from ordered_model.models import OrderedModel

from blog.models import BlogPost, BlogCollection


class BlogCollectionItem(OrderedModel):
    item = models.ForeignKey(
        to=BlogPost,
        on_delete=models.CASCADE,
        related_name='collected_item',
        blank=True,
    )

    collection_name = models.ForeignKey(
        to=BlogCollection,
        on_delete=models.CASCADE,
        related_name='blogcollectionitem',
        blank=True,
    )

    order_with_respect_to = 'collection_name'

    class Meta:
        index_together = ('item', 'order')

    def __str__(self):
        return f'{self.item.title}'
