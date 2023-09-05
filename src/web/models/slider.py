from django.db import models
from ordered_model.models import OrderedModel

from common.model_mixins import AutoSlugifyMixin


class Slider(AutoSlugifyMixin,
             models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='name',
    )

    slug = models.SlugField(
        blank=True,
    )

    slides = models.ManyToManyField(
        to='web.Slide',
        blank=True,
        related_name='slider',
        verbose_name='slides',
    )

    def __str__(self):
        return self.name


class SliderSlidesThroughModel(OrderedModel):
    slider = models.ForeignKey(
        to=Slider,
        on_delete=models.CASCADE,
        related_name='slider_slides',
    )

    slide = models.ForeignKey(
        to='web.Slide',
        on_delete=models.CASCADE,
    )

    order_with_respect_to = 'slider'

    class Meta:
        ordering = ('slider', 'order')

