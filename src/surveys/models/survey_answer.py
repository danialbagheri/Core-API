from django.db import models

from surveys.models import SurveyQuestion, SurveySubmission, SurveyQuestionChoice


class SurveyAnswer(models.Model):
    submission = models.ForeignKey(
        to=SurveySubmission,
        on_delete=models.CASCADE,
        related_name='answers',
    )

    question = models.ForeignKey(
        to=SurveyQuestion,
        on_delete=models.CASCADE,
        related_name='answers',
    )

    choices = models.ManyToManyField(
        to=SurveyQuestionChoice,
        related_name='answers',
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True,
    )
