from celery import signature
from django.core.validators import FileExtensionValidator
from django.db import models

from web.models import IconGroup


class IconGroupItem(models.Model):
    icon_group = models.ForeignKey(
        to=IconGroup,
        on_delete=models.CASCADE,
        related_name='items',
    )

    name = models.CharField(
        max_length=128,
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

    svg_icon_text = models.TextField(
        blank=True,
    )

    url = models.URLField(
        max_length=256,
        blank=True,
    )

    is_active = models.BooleanField()

    position = models.IntegerField()

    class Meta:
        ordering = ('position',)

    def save(self, *args, **kwargs):
        old_object = None
        if self.pk:
            old_object = IconGroupItem.objects.get(pk=self.pk)
        super().save(*args, **kwargs)
        if self.svg_icon and self.svg_icon == old_object.svg_icon:
            signature(
                varies='web.tasks.ProcessIconGroupSvgFileTask',
                args=(self.id, 'svg_icon'),
            ).delay()
