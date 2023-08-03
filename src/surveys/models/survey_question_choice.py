from django.db import models

from surveys.models import SurveyQuestion


class SurveyQuestionChoice(models.Model):
    question = models.ForeignKey(
        to=SurveyQuestion,
        on_delete=models.CASCADE,
        related_name='choices',
    )

    text = models.CharField(
        max_length=128,
    )

    position = models.PositiveIntegerField(
        default=0,
    )

    next_question = models.ForeignKey(
        to=SurveyQuestion,
        on_delete=models.SET_NULL,
        related_name='source_answers',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('position',)
