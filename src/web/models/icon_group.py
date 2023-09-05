from django.db import models

from common.model_mixins import AutoSlugifyMixin


class IconGroup(AutoSlugifyMixin,
                models.Model):
    name = models.CharField(
        max_length=128,
    )

    slug = models.SlugField(
        max_length=64,
        blank=True,
    )

    is_active = models.BooleanField()
