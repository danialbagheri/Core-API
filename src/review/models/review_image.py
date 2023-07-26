from django.db import models

from review.models import Review


class ReviewImage(models.Model):
    review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='images',
    )

    image = models.ImageField(
        upload_to='reviews/',
        max_length=None,
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )
