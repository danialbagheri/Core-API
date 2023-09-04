from django.db import models

from common.model_mixins import AutoSlugifyMixin
from web.models import Slider


class BlogCollection(AutoSlugifyMixin,
                     models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        allow_unicode=True,
    )

    description = models.TextField(
        blank=True,
    )

    image = models.ImageField(
        upload_to='blog_collections/',
        max_length=None,
        null=True,
        blank=True,
    )

    slider = models.ForeignKey(
        to=Slider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
