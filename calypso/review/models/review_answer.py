from django.db import models

from product.models import ReviewQuestion
from review.models import Review


class ReviewAnswer(models.Model):
    review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        related_name='answers',
    )

    question = models.ForeignKey(
        to=ReviewQuestion,
        on_delete=models.CASCADE,
    )

    text = models.TextField()
