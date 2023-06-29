from django.db import models
from django.utils.translation import gettext as _


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name=_('name'),
        unique=True,
    )

    def __str__(self):
        return self.name
