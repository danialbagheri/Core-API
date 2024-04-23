from django.core.validators import FileExtensionValidator
from django.db import models


class Slide(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='name',
    )

    xl_image = models.ImageField(
        upload_to='slide/xl/',
        max_length=None,
        blank=True,
    )

    lg_image = models.ImageField(
        upload_to='slide/lg/',
        max_length=None,
        blank=True,
    )

    md_image = models.ImageField(
        upload_to='slide/md/',
        max_length=None,
        blank=True,
    )

    sm_image = models.ImageField(
        upload_to='slide/sm/',
        max_length=None,
        blank=True,
    )

    xs_image = models.ImageField(
        upload_to='slide/xs/',
        max_length=None,
        blank=True,
    )

    video = models.FileField(
        upload_to='slide/videos/',
        validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])],
        blank=True,
    )

    image_alt_text = models.CharField(
        max_length=200,
        blank=True,
    )

    active = models.BooleanField(
        default=False,
    )

    custom_slide = models.BooleanField(
        default=False,
    )

    custom_code = models.TextField(
        blank=True,
    )

    link = models.URLField(
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
