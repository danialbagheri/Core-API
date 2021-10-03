from django.db import models


class Collection(models.Model):
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

    def __str__(self):
        return self.name