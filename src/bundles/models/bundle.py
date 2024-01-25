from django.db import models


class Bundle(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    name = models.CharField(
        max_length=128,
    )

    slug = models.SlugField(
        max_length=128,
        unique=True,
    )

    description = models.TextField()

    base_discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10,
    )

    extra_discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.name
