from django.db import models
from django.utils.text import slugify

from common.model_mixins import AutoSlugifyMixin


class Setting(AutoSlugifyMixin,
              models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='name',
    )

    slug = models.SlugField(
        default='',
        editable=False,
        blank=True,
    )

    description = models.CharField(
        max_length=350,
        default='',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
