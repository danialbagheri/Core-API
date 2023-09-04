from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext as _

from common.model_mixins import AutoSlugifyMixin
from product.utils import icons_directory_path, get_slug


class Tag(AutoSlugifyMixin,
          models.Model):
    """
    Tags to be used for tagging products with different benefits
    example: paraben-free, sensitive lotion etc
    """

    icon = models.ImageField(
        upload_to=icons_directory_path,
        blank=True,
    )

    svg_icon = models.FileField(
        upload_to='tag-svg-icons',
        max_length=512,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['svg'])],
    )

    name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('name'),
    )

    slug = models.SlugField(
        default=get_slug,
        unique=True,
        verbose_name=_('slug'),
    )

    def __str__(self):
        return self.name
