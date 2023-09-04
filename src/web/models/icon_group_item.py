from django.core.validators import FileExtensionValidator
from django.db import models

from web.models import IconGroup


class IconGroupItem(models.Model):
    icon_group = models.ForeignKey(
        to=IconGroup,
        on_delete=models.CASCADE,
        related_name='items',
    )

    icon = models.ImageField(
        upload_to='icon-groups/',
        max_length=512,
        blank=True,
        null=True,
    )

    svg_icon = models.FileField(
        upload_to='svg-icon-groups/',
        max_length=512,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['svg'])],
    )

    url = models.URLField(
        max_length=256,
        blank=True,
    )

    is_active = models.BooleanField()

    position = models.IntegerField()
