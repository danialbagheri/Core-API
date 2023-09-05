from django.db import models

from common.model_mixins import AutoSlugifyMixin


class Survey(AutoSlugifyMixin,
             models.Model):
    name = models.CharField(
        max_length=32,
        unique=True,
    )

    slug = models.SlugField(
        max_length=32,
        unique=True,
        blank=True,
    )

    email_required = models.BooleanField()

    def __str__(self):
        return self.name
