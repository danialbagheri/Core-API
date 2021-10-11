from django.db import models

from product.models import ReviewQuestion


class QuestionChoice(models.Model):
    review_question = models.ForeignKey(
        to=ReviewQuestion,
        on_delete=models.CASCADE,
        related_name='answer_choices',
    )

    text = models.TextField()

    def __str__(self):
        return self.text
