from django.db import models


class Slide(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='name',
    )

    desktop_image = models.ImageField(
        upload_to='slide/desktop/',
        max_length=None,
        blank=True,
    )

    tablet_image = models.ImageField(
        upload_to='slide/tablet/',
        max_length=None,
        blank=True,
    )

    mobile_image = models.ImageField(
        upload_to='slide/mobile/',
        max_length=None,
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
