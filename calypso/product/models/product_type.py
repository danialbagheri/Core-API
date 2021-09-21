from django.db import models
from django.utils.translation import gettext as _


class ProductType(models.Model):
    """
    Product types example:
    sun protection, after sun, skin care etc.
    """
    name = models.CharField(
        max_length=200,
        verbose_name=_('name'),
    )

    def __str__(self):
        return self.name
