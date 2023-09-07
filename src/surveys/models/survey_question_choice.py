from django.db import models

from common.model_mixins import AutoSlugifyMixin
from surveys.models import SurveyQuestion


class SurveyQuestionChoice(AutoSlugifyMixin,
                           models.Model):
    question = models.ForeignKey(
        to=SurveyQuestion,
        on_delete=models.CASCADE,
        related_name='choices',
    )

    text = models.CharField(
        max_length=128,
    )
    slug_name_field = 'text'

    slug = models.SlugField(
        max_length=64,
        blank=True,
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

    def __str__(self):
        return self.text
