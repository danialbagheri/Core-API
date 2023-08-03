from django.db import models


class Survey(models.Model):
    name = models.CharField(
        max_length=32,
        unique=True,
    )

    slug = models.SlugField(
        max_length=32,
        unique=True,
    )

    email_required = models.BooleanField()
