from django.db import models

from surveys.models import Survey
from user.models import User


class SurveySubmission(models.Model):
    survey = models.ForeignKey(
        to=Survey,
        on_delete=models.CASCADE,
        related_name='responses',
    )

    email = models.EmailField(
        blank=True,
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='questionnaire_responses',
        null=True,
        blank=True,
    )

    ip = models.CharField(
        max_length=64,
        blank=True,
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True,
    )
