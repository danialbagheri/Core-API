from django.core.validators import FileExtensionValidator
from django.db import models

from common.model_mixins import AutoSlugifyMixin


class Menu(AutoSlugifyMixin,
           models.Model):
    slug = models.SlugField(
        blank=True,
    )

    name = models.CharField(
        max_length=32,
    )

    text = models.CharField(
        max_length=128,
        blank=True,
    )

    url = models.URLField(
        blank=True,
    )

    image = models.ImageField(
        upload_to='menu-images/',
        max_length=512,
        null=True,
        blank=True,
    )

    svg_image = models.FileField(
        upload_to='menu-svg-images/',
        max_length=512,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['svg'])],
    )

    parent_menu = models.ForeignKey(
        to='web.Menu',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_menus',
    )

    position = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ('position',)

    def __str__(self):
        return self.name
