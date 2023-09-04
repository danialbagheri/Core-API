from django.db import models
from django.utils.translation import gettext as _

from common.model_mixins import AutoSlugifyMixin


class ProductType(AutoSlugifyMixin,
                  models.Model):
    """
    Product types example:
    sun protection, after sun, skin care etc.
    """
    name = models.CharField(
        max_length=200,
        verbose_name=_('name'),
    )

    slug = models.SlugField(
        max_length=256,
        null=True,
        allow_unicode=True,
    )

    class Meta:
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.name
