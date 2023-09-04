from django.db import models

from common.model_mixins import AutoSlugifyMixin
from web.models import Slider


class Collection(AutoSlugifyMixin,
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

    background_image_alt = models.CharField(
        max_length=128,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    public = models.BooleanField(
        default=True,
    )

    image = models.ImageField(
        upload_to='collections/',
        null=True,
        blank=True,
        max_length=None,
    )

    slider = models.ForeignKey(
        to=Slider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
