from django.db import models

from common.model_mixins import AutoSlugifyMixin


class TopBar(AutoSlugifyMixin,
             models.Model):
    name = models.CharField(
        max_length=256,
    )

    slug = models.SlugField(
        blank=True,
    )

    is_active = models.BooleanField()

    position = models.IntegerField()
