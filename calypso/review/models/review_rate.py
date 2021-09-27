from django.db import models

from review.models import Review


class ReviewRate(models.Model):
    review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
    )

    rate_type = models.CharField(
        max_length=64,
    )

    user_cookie = models.CharField(
        max_length=64,
    )
